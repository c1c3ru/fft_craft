#!/usr/bin/env python3
"""Fail closed if the T32 host-only staging build loses source traceability."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REFERENCE = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
EXPECTED_SOURCES = {
    "docs/re-tools/c-models/b01_named_cpp_methods.cpp",
    "docs/re-tools/c-models/t14_boot_framemove.c",
    "docs/re-tools/c-models/t19_evt_flag_high_low.c",
    "docs/re-tools/c-models/t19_evt_flagset.c",
    "docs/re-tools/c-models/t22_ios_resumegetdata.c",
}


def validate(data, cmake, root=ROOT):
    if data.get("schema") != 1 or data.get("reference_elf_sha256") != REFERENCE:
        raise ValueError("T32 stage has wrong baseline")
    for key in ("android_shared_object_built", "jni_bindings_implemented",
                "original_game_elf_linked", "app_integration_proven", "t32_done"):
        if data.get(key) is not False:
            raise ValueError("Host-only stage cannot claim Android completion")
    modules = data.get("modules")
    if not isinstance(modules, list) or len(modules) != len(EXPECTED_SOURCES):
        raise ValueError("T32 module inventory incomplete")
    sources = set()
    owners = set()
    for module in modules:
        path = module.get("source")
        entries = module.get("original_entries")
        if path in sources or path not in EXPECTED_SOURCES:
            raise ValueError("Duplicate/unknown source")
        if not (root / path).is_file():
            raise ValueError("Missing source file: " + path)
        if module.get("complete_function_equivalence") is not False:
            raise ValueError("Staging is not a certified semantic contract")
        if not isinstance(entries, list) or not entries:
            raise ValueError("Module must have original-address provenance")
        for entry in entries:
            if not re.fullmatch(r"[0-9a-f]{8}", entry):
                raise ValueError("Invalid original address")
            if entry in owners:
                raise ValueError("Original address assigned to multiple modules")
            owners.add(entry)
        sources.add(path)
    if sources != EXPECTED_SOURCES:
        raise ValueError("Incomplete set of C/C++ stage sources")
    for path in sources:
        if cmake.count("../" + path) != 1:
            raise ValueError("CMake source not tracked exactly once: " + path)
    if "libgl2jni.so" in cmake or "add_library(fftcraft_stage_models SHARED" in cmake:
        raise ValueError("Never link or replace original game ELF in host stage")
    return len(owners)


def main():
    data = json.loads((HERE / "module-map.json").read_text(encoding="utf-8"))
    cmake = (HERE / "CMakeLists.txt").read_text(encoding="utf-8")
    count = validate(data, cmake)
    print("T32_STAGED_ORIGINAL_ENTRIES=" + str(count))
    print("T32_NATIVE_STAGE_AUTOMATION=PASS")
    print("T32_APK_OR_GAME_ENGINE_COMPLETE=0")


if __name__ == "__main__":
    main()
