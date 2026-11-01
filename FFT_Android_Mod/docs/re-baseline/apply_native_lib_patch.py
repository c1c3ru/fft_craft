#!/usr/bin/env python3
"""Reproduz o patch binario registrado em native_lib_patch_diff.json.

Aplica os bytes "after" de cada diff sobre uma copia do backup original
e confirma que o resultado bate com o SHA-256 do arquivo atualmente em
src/lib/<abi>/libgl2jni.so. Nao explica o MOTIVO do patch (ver
T01_BASELINE_REPORT.md, item pendente) -- apenas comprova que o conjunto
de diffs registrado reproduz exatamente o binario atual a partir do
backup, byte a byte.

Uso:
    python3 apply_native_lib_patch.py armeabi
    python3 apply_native_lib_patch.py x86
    python3 apply_native_lib_patch.py all   # roda as duas ABIs
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
DIFF_JSON = HERE / "native_lib_patch_diff.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def apply_abi(abi: str, data: dict) -> bool:
    entry = data["libs"][abi]
    backup_path = REPO_ROOT / entry["backup_path"]
    current_path = REPO_ROOT / entry["current_path"]

    buf = bytearray(backup_path.read_bytes())
    for d in entry["diffs"]:
        offset = int(d["offset"], 16)
        before = int(d["before"], 16)
        after = int(d["after"], 16)
        if buf[offset] != before:
            print(f"[{abi}] ERRO: byte em {hex(offset)} do backup é "
                  f"{hex(buf[offset])}, esperado {hex(before)} — backup "
                  "mudou desde o registro do diff.")
            return False
        buf[offset] = after

    reconstructed_hash = hashlib.sha256(bytes(buf)).hexdigest()
    current_hash = sha256_file(current_path)
    ok = reconstructed_hash == current_hash == entry["current_sha256"]
    status = "OK" if ok else "FALHOU"
    print(f"[{abi}] {len(entry['diffs'])} bytes aplicados — reconstrução {status}")
    print(f"[{abi}] backup={entry['backup_sha256']}")
    print(f"[{abi}] reconstruído={reconstructed_hash}")
    print(f"[{abi}] atual_registrado={entry['current_sha256']}")
    print(f"[{abi}] atual_recalculado={current_hash}")
    return ok


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in ("armeabi", "x86", "all"):
        print(__doc__)
        return 2
    data = json.loads(DIFF_JSON.read_text())
    abis = ["armeabi", "x86"] if sys.argv[1] == "all" else [sys.argv[1]]
    all_ok = True
    for abi in abis:
        all_ok &= apply_abi(abi, data)
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
