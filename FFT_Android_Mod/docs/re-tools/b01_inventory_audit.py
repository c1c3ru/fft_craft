#!/usr/bin/env python3
"""B01: reproducible, read-only inventory consistency and asset-provenance audit.

This tool checks *declared* inventory ranges, not decoded/executed instructions.
No result certifies semantic equivalence, file reachability, or APK functionality.
"""
import argparse
import csv
import hashlib
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

ELF_SHA256 = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
FIELDS = ("address", "size", "mangled", "demangled", "status", "section_ref")
ADDRESS = re.compile(r"[0-9a-fA-F]{8}\Z")
LFS = b"version https://git-lfs.github.com/spec/v1"
MAX_U32 = 1 << 32


class InventoryError(ValueError):
    pass


def csv_rows(path):
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != list(FIELDS):
            raise InventoryError("Unexpected inventory CSV schema")
        rows = []
        for line, item in enumerate(reader, 2):
            if None in item or any(item.get(f) is None for f in FIELDS):
                raise InventoryError("Malformed CSV row at line %d" % line)
            address = item["address"]
            if not ADDRESS.fullmatch(address):
                raise InventoryError("Invalid entry address at line %d" % line)
            try:
                size = int(item["size"], 10)
            except ValueError:
                raise InventoryError("Non-integer size at line %d" % line) from None
            start = int(address, 16)
            if not 0 < size < MAX_U32 or start + size > MAX_U32:
                raise InventoryError("Out-of-range interval at line %d" % line)
            rows.append({"address": address.lower(), "start": start, "size": size,
                         "mangled": item["mangled"], "status": item["status"]})
    if not rows:
        raise InventoryError("Empty inventory CSV")
    return rows


def canonicalize(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row["address"]].append(row)
    conflicting = []
    for address, duplicates in sorted(groups.items()):
        sizes = {x["size"] for x in duplicates}
        if len(sizes) > 1:
            conflicting.append(address)
    if conflicting:
        raise InventoryError("Conflicting entrypoint sizes: %d" % len(conflicting))
    entries = sorted((items[0] for items in groups.values()),
                     key=lambda x: (x["start"], x["size"]))
    alias_count = len(rows) - len(entries)
    overlaps = []
    # Intervals are not claimed to be disjoint functions: aliases, entrypoints
    # inside a body, and bad sizes all require separate manual classification.
    for i, left in enumerate(entries):
        end = left["start"] + left["size"]
        for right in entries[i + 1:]:
            if right["start"] >= end:
                break
            overlaps.append({
                "first": left["address"], "second": right["address"],
                "overlap_bytes": min(end, right["start"] + right["size"]) - right["start"]
            })
    merged = []
    for row in entries:
        start, end = row["start"], row["start"] + row["size"]
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return {
        "declared_entries": len(rows),
        "unique_entrypoints": len(entries),
        "duplicate_address_entries": alias_count,
        "declared_interval_union_bytes_not_executable_coverage":
            sum(end - start for start, end in merged),
        "overlap_pairs": overlaps,
        "overlap_pair_count": len(overlaps),
        "overlap_addresses_count": len(set(
            x for item in overlaps for x in (item["first"], item["second"]))),
        "interval_groups_count": len(merged),
        "not_semantic_equivalence": True,
    }, entries


def validate_priority(rows, canonical):
    lookup = {x["address"]: x["size"] for x in canonical}
    seen = set()
    missing = []
    size_mismatch = []
    duplicate = []
    for row in rows:
        address = row["address"]
        if address in seen:
            duplicate.append(address)
        seen.add(address)
        if address not in lookup:
            missing.append(address)
        elif lookup[address] != row["size"]:
            size_mismatch.append(address)
    if missing or size_mismatch or duplicate:
        raise InventoryError(
            "Priority inventory inconsistent: missing=%d size_mismatch=%d duplicates=%d"
            % (len(missing), len(size_mismatch), len(duplicate)))
    return {"rows": len(rows), "unique_addresses": len(seen),
            "all_subset_of_canonical": True, "sizes_agree": True}


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def file_state(path):
    if not path.is_file():
        return {"status": "missing"}
    size = path.stat().st_size
    with path.open("rb") as source:
        head = source.read(180)
    if head.startswith(LFS):
        return {"status": "lfs_pointer_not_asset", "tracked_bytes": size}
    return {"status": "materialized", "size_bytes": size}


def git_tracked_paths(repository_root):
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(repository_root), "ls-files", "-z", "--",
             "FFT_Android_Mod/src", "FFT_Android_Mod/original",
             "FFT_Android_Mod/obb-data"],
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        raise InventoryError("Git tracked-file manifest unavailable") from None
    paths = sorted(set(x.decode("utf-8") for x in raw.split(b"\0") if x))
    if not paths:
        raise InventoryError("No tracked Android assets found")
    return paths


def asset_inventory(repository_root, paths):
    native = sorted(p for p in paths if re.fullmatch(
        r"FFT_Android_Mod/src/lib/[^/]+/[^/]+\.so", p))
    smali = sorted(p for p in paths if p.startswith(
        "FFT_Android_Mod/src/smali/") and p.endswith(".smali"))
    obb = sorted(p for p in paths if p.startswith(
        "FFT_Android_Mod/obb-data/") and p.endswith(".obb"))
    apks = sorted(p for p in paths if p.startswith(
        "FFT_Android_Mod/original/") and p.endswith(".apk"))
    original_elf = repository_root / "FFT_Android_Mod/src/lib/armeabi/libgl2jni.so"
    elf = file_state(original_elf)
    if elf["status"] == "materialized":
        elf["sha256"] = sha256_file(original_elf)
        elf["matches_expected_sha256"] = elf["sha256"] == ELF_SHA256
        with original_elf.open("rb") as src:
            header = src.read(20)
        elf["valid_arm_elf32_le_header"] = (len(header) == 20
            and header[:6] == b"\x7fELF\x01\x01"
            and int.from_bytes(header[18:20], "little") == 40)
    elif elf["status"] == "missing":
        elf["matches_expected_sha256"] = False
        elf["valid_arm_elf32_le_header"] = False
    others = {name: file_state(repository_root / name)
              for name in sorted(set(obb + apks + native))}
    obb_unavailable = [p for p in obb if others[p]["status"] != "materialized"]
    return {
        "tracked_smali_file_count": len(smali),
        "tracked_native_so_paths": native,
        "tracked_original_apk_paths": apks,
        "tracked_obb_paths": obb,
        "native_elf": elf,
        "binary_asset_states": others,
        "unmaterialized_obb_paths": obb_unavailable,
        "android_artifact_inventory_complete": (
            bool(smali) and bool(native) and bool(obb) and bool(apks)
            and not obb_unavailable and elf.get("matches_expected_sha256", False)
            and elf.get("valid_arm_elf32_le_header", False)
        ),
    }


def build_report(root, tracked_paths=None):
    root = Path(root)
    inv = root / "FFT_Android_Mod/docs/RE_FUNCTION_INVENTORY.csv"
    priority = root / "FFT_Android_Mod/docs/alvos_prioritarios_nucleo.csv"
    stats, canonical = canonicalize(csv_rows(inv))
    prio = validate_priority(csv_rows(priority), canonical)
    assets = asset_inventory(root, tracked_paths if tracked_paths is not None
                             else git_tracked_paths(root))
    blockers = []
    if stats["overlap_pair_count"]:
        blockers.append("unclassified_overlapping_entrypoint_intervals")
    if not assets["native_elf"].get("matches_expected_sha256"):
        blockers.append("reference_arm_elf_not_sha_verified")
    if not assets["native_elf"].get("valid_arm_elf32_le_header"):
        blockers.append("reference_elf_header_not_verified")
    if not assets["android_artifact_inventory_complete"]:
        blockers.append("android_apk_obb_jni_artifacts_not_fully_verified")
    blockers.append("jni_smali_class_to_native_symbol_mapping_not_validated")
    blockers.append("reachability_and_code_vs_data_not_proven")
    return {
        "schema": 1, "stage": "B01", "task_state": "in_progress",
        "expected_elf_sha256": ELF_SHA256,
        "csv_sha256": sha256_file(inv),
        "priority_csv_sha256": sha256_file(priority),
        "elf_function_inventory": stats, "priority_subset": prio,
        "android_artifacts": assets,
        "blockers": blockers, "ready_to_mark_B01_done": False,
        "semantic_certificates_added": 0,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path,
                        default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        report = build_report(args.root)
    except (InventoryError, OSError) as exc:
        parser.exit(2, "B01_INVENTORY_REJECTED: " + str(exc) + "\n")
    result = json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(result, encoding="utf-8")
    else:
        print(result, end="")
    print("B01_INVENTORY_ROWS=%d" % report["elf_function_inventory"]["declared_entries"])
    print("B01_INVENTORY_UNIQUE=%d" % report["elf_function_inventory"]["unique_entrypoints"])
    print("B01_B01_DONE=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
