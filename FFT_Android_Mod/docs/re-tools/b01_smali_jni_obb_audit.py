#!/usr/bin/env python3
"""B01 read-only Smali/JNI linkage and OBB manifest audit.

Never claims that a name match demonstrates RegisterNatives binding or an
executed native path; no APK/OBB bytes or game content are copied to outputs.
"""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from elftools.elf.elffile import ELFFile

EXPECTED_ELF = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
METHOD = re.compile(r"^\s*\.method\s+(.+?)\s+([^\s(]+)\(([^)]*)\)(\S+)\s*$", re.M)
CLASS = re.compile(r"^\s*\.class\s+[^\n]*?\s+(L[^;\s]+;)", re.M)
LFS = re.compile(r"\Aversion https://git-lfs.github.com/spec/v1\n"
                 r"oid sha256:([a-f0-9]{64})\nsize ([0-9]+)\n?\Z")
MAX_CLASSES = 10000
MAX_ZIP_ENTRIES = 200000


def digest_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def jni_encode(value):
    out = []
    for c in value:
        if c.isascii() and c.isalnum():
            out.append(c)
        elif c == "/":
            out.append("_")
        elif c == "_":
            out.append("_1")
        elif c == ";":
            out.append("_2")
        elif c == "[":
            out.append("_3")
        else:
            out.append("_0%04x" % ord(c))
    return "".join(out)


def scan_smali(root):
    sources = sorted(root.rglob("*.smali"))
    if not sources or len(sources) > MAX_CLASSES:
        raise ValueError("Smali source count missing or excessive")
    native = []
    load_lib = []
    storage_candidates = []
    class_definitions = set()
    class_prefix = {}
    for path in sources:
        content = path.read_text(encoding="utf-8", errors="replace")
        hit = CLASS.search(content)
        if not hit:
            continue
        descriptor = hit.group(1)
        class_definitions.add(descriptor)
        class_prefix[descriptor] = path.relative_to(root).as_posix()
        for match in METHOD.finditer(content):
            modifiers, name, args, ret = match.groups()
            if "native" in modifiers.split():
                native.append({"class": descriptor, "method": name,
                               "descriptor": f"({args}){ret}",
                               "source": path.relative_to(root).as_posix()})
        # These are static references; not proof that the class or getter is used.
        for m in re.finditer(r"const-string(?:/jumbo)?\s+[^,]+,\s+\"([^\"]+)\"", content):
            if m.group(1) == "gl2jni":
                load_lib.append({"class": descriptor,
                                 "evidence_kind": "const-string_gl2jni",
                                 "source": path.relative_to(root).as_posix()})
        if ("StorageUtil;" in content or
                "GetIntPath" in content or "GetExt1Path" in content):
            storage_candidates.append({
                "class": descriptor,
                "source": path.relative_to(root).as_posix(),
                "mentions_GetIntPath": "GetIntPath" in content,
                "mentions_GetExt1Path": "GetExt1Path" in content,
                "mentions_StorageUtil": "StorageUtil" in content
            })
    return {"smali_files_scanned": len(sources),
            "classes_declared_count": len(class_definitions),
            "native_methods": sorted(native, key=lambda x:(x["class"], x["method"], x["descriptor"])),
            "gl2jni_literal_references": load_lib,
            "storageutil_static_references": storage_candidates}


def dynsym_exports(elf_path):
    if digest_file(elf_path) != EXPECTED_ELF:
        raise ValueError("Reference ARM ELF hash mismatch")
    with elf_path.open("rb") as f:
        elf = ELFFile(f)
        if elf["e_machine"] != "EM_ARM":
            raise ValueError("Reference ELF not ARM")
        table = elf.get_section_by_name(".dynsym")
        if table is None:
            raise ValueError("No dynamic ELF symbol table")
        exported = set()
        imports = set()
        for sym in table.iter_symbols():
            if not sym.name:
                continue
            if sym["st_shndx"] == "SHN_UNDEF":
                imports.add(sym.name)
            else:
                exported.add(sym.name)
        return exported, imports


def link_methods(native, exports):
    pairs = []
    for entry in native:
        cls = entry["class"].removeprefix("L").removesuffix(";")
        base = "Java_" + jni_encode(cls) + "_" + jni_encode(entry["method"])
        candidates = sorted(sym for sym in exports if sym == base or sym.startswith(base + "__"))
        # Exported names only; native method may instead be bound via RegisterNatives.
        pairs.append({**entry, "jni_export_candidates": candidates,
                      "static_export_candidate": bool(candidates),
                      "runtime_binding_proven": False,
                      "method_equivalence_proven": False})
    return pairs


def inspect_obb(path):
    if not path.is_file():
        return {"state": "missing"}
    size = path.stat().st_size
    if size <= 2048:
        try:
            head = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            head = ""
        m = LFS.fullmatch(head.replace("\r\n", "\n"))
        if m:
            return {"state": "git_lfs_pointer_only", "pointer_bytes": size,
                    "lfs_declared_size_bytes": int(m.group(2)),
                    "lfs_declared_sha256": m.group(1),
                    "materialized_bytes_verified": False}
    result = {"state": "materialized_non_pointer",
              "actual_size_bytes": size,
              "content_sha256": digest_file(path)}
    if not zipfile.is_zipfile(path):
        result["archive_format"] = "unknown_not_zip"
        result["entries_verified"] = False
        return result
    with zipfile.ZipFile(path) as z:
        members = z.infolist()
        if len(members) > MAX_ZIP_ENTRIES:
            raise ValueError("OBB entry count exceeds audit bound")
        # Do not extract or disclose filenames or content.
        result["archive_format"] = "zip_directory_only"
        result["archive_entry_count"] = len(members)
        result["archive_uncompressed_bytes_declared"] = sum(m.file_size for m in members)
        result["archive_compressed_bytes_declared"] = sum(m.compress_size for m in members)
        result["entries_verified"] = False
        result["member_crc_or_data_verified"] = False
    return result


def run(root):
    root = Path(root)
    elf = root / "FFT_Android_Mod/src/lib/armeabi/libgl2jni.so"
    smali = root / "FFT_Android_Mod/src/smali"
    obb = root / "FFT_Android_Mod/obb-data/main.202000.com.square_enix.android_googleplay.FFT_en2.obb"
    smali_data = scan_smali(smali)
    exports, imports = dynsym_exports(elf)
    linked = link_methods(smali_data["native_methods"], exports)
    return {
        "schema": 1, "task": "B01", "elf_sha256": EXPECTED_ELF,
        "source": "static_smali_and_ELF_dynsym_only",
        "smali_files_scanned": smali_data["smali_files_scanned"],
        "smali_classes_declared": smali_data["classes_declared_count"],
        "native_method_count": len(linked),
        "native_methods": linked,
        "native_export_candidates_count": sum(bool(p["jni_export_candidates"]) for p in linked),
        "unresolved_native_methods_count": sum(not p["jni_export_candidates"] for p in linked),
        "jni_named_exports": sorted(sym for sym in exports if sym.startswith("Java_")),
        "jni_onload_exported": "JNI_OnLoad" in exports,
        "register_natives_import_found": "RegisterNatives" in imports,
        "register_natives_vtable_calls_unresolved": True,
        "storageutil_static_references": smali_data["storageutil_static_references"],
        "gl2jni_literal_references": smali_data["gl2jni_literal_references"],
        "obb": inspect_obb(obb),
        "android_jni_runtime_binding_proven": False,
        "original_game_runtime_observed": False,
        "b01_complete": False,
        "new_semantic_certificates": 0,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    report = run(a.root)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(f"B01_SMALI_FILES={report['smali_files_scanned']}")
    print(f"B01_NATIVE_METHODS={report['native_method_count']}")
    print(f"B01_STATIC_JNI_EXPORT_CANDIDATES={report['native_export_candidates_count']}")
    print(f"B01_OBB_STATE={report['obb']['state']}")
    print("B01_JNI_RUNTIME_BINDING_PROVEN=0")
    print("B01_DONE=0")


if __name__ == "__main__":
    main()
