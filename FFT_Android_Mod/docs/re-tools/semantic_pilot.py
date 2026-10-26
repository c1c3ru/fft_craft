#!/usr/bin/env python3
"""Bounded parallel ARM evidence pilot. Reports are partial, never certificates."""
import argparse
import concurrent.futures as futures
import hashlib
import json
from pathlib import Path

import semantic_evidence


def inspect_task(task, binary, expected_digest, max_bytes=20000):
    if task["binary_sha256"] != expected_digest:
        raise ValueError("manifest ELF digest mismatch")
    address = int(task["address"], 16)
    size = int(task["size"])
    if size < 1 or size > max_bytes:
        raise ValueError("invalid or oversized task")
    thumb = bool(address & 1)
    code = semantic_evidence.read_function(binary, address & ~1, size)
    if thumb:
        instructions, tables, unresolved = semantic_evidence.collect_thumb(code, address & ~1)
    else:
        instructions, tables, unresolved = semantic_evidence.collect(code, address)
    literals = semantic_evidence.pc_relative_literals(instructions, address & ~1, code, thumb=thumb)
    calls = [hex(a) for a, ins in instructions.items()
             if ins.mnemonic.startswith(("bl ", "blx ")) or ins.mnemonic in ("bl", "blx")]
    stores = [hex(a) for a, ins in instructions.items()
              if ins.mnemonic.startswith(("str", "stm", "vstr", "vstm", "swp"))]
    alignment = 2 if thumb else 4
    slots = set(range(address & ~1, (address & ~1) + len(code) - len(code) % alignment, alignment))
    observed = {a + offset for a, ins in instructions.items()
                for offset in range(0, ins.size, alignment)}
    missing = sorted(slots - observed)
    return {
        "address": task["address"], "name": task["name"], "size": size,
        "binary_sha256": expected_digest, "semantic_status": "partial",
        "evidence_class": "static_bounded", "instruction_set": "thumb" if thumb else "arm",
        "decoded_instructions": len(instructions), "unvisited_slots": len(missing),
        "candidate_literal_addresses": [hex(a) for a in sorted(literals)],
        "call_sites": calls, "store_sites": stores,
        "resolved_jump_tables": len(tables), "unresolved_dispatches": [hex(a) for a in unresolved],
        "unverified": ["complete_control_flow", "register_effects", "runtime_memory_effects",
                       "input_output_contract", "differential_tests", "semantic_equivalence"],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, default=semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--manifests", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--workers", type=int, default=5)
    args = p.parse_args()
    if not 1 <= args.workers <= 16:
        p.error("workers must be 1..16")
    digest = hashlib.sha256(args.binary.read_bytes()).hexdigest()
    tasks = []
    for path in sorted(args.manifests.glob("semantic-worker-*.json")):
        manifest = json.loads(path.read_text())
        if manifest["elf_sha256"] != digest:
            raise ValueError(f"stale manifest: {path}")
        tasks.extend(manifest["tasks"])
    addresses = [t["address"] for t in tasks]
    if len(addresses) != len(set(addresses)):
        raise ValueError("duplicate addresses across manifests")
    args.output.mkdir(parents=True, exist_ok=True)
    failures = []
    with futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        running = {pool.submit(inspect_task, task, args.binary, digest): task for task in tasks}
        for future in futures.as_completed(running):
            task = running[future]
            try:
                result = future.result()
            except Exception as error:
                failures.append((task["address"], str(error)))
                continue
            path = args.output / (task["address"] + ".json")
            path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(f"PILOT_PARTIAL={len(tasks) - len(failures)}")
    print(f"PILOT_FAILED={len(failures)}")
    for address, error in failures:
        print(f"FAILED {address}: {error}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
