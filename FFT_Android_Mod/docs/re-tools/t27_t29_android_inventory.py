#!/usr/bin/env python3
"""T27/T29: inexpensive STATIC JNI callsite and OBB handoff audit.

No OBB download, APK decompilation, Android emulator, runtime claim,
native bridge replacement, or semantic certificate generation.
"""
import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import b01_smali_jni_obb_audit as baseline

GL_CLASS = "Lcom/square_enix/FFT_Android/GL2JNILib;"
EXPECTED_GL_METHODS = {
    "dialogOnClose", "getCommand", "init", "isExit", "onDestroy",
    "onKeyEvent", "onPause", "onResume", "onTouchEvent",
    "setAccelerometerValue", "setBatteryLevel", "step",
}
OBB_SIZE = 815622218
OBB_SHA = "ca56bc16ab20f0f395bf1bdb7651b0073698090d395ac76687dc1aabcca370e3"
ANDROID_NAME = "{http://schemas.android.com/apk/res/android}name"
INVOKE = re.compile(
    r"\binvoke-(?:static|virtual|direct|interface|super)(?:/range)?"
    r"\s+\{[^}\n]*\},\s*(L[^;\s]+;)->([^\s(]+)(\([^)]*\)\S+)"
)
MAX_SITES = 25000


def invocations(smali_root, methods):
    keys = {(m["class"], m["method"], m["descriptor"]) for m in methods}
    sites = {key: [] for key in keys}
    all_sites = 0
    for path in sorted(smali_root.rglob("*.smali")):
        data = path.read_text(encoding="utf-8", errors="replace")
        relative = path.relative_to(smali_root).as_posix()
        for m in INVOKE.finditer(data):
            owner, name, descriptor = m.groups()
            key = (owner, name, descriptor)
            if key not in sites:
                continue
            all_sites += 1
            if all_sites > MAX_SITES:
                raise ValueError("JNI callsites exceed review limit")
            sites[key].append({
                "smali_source": relative,
                "line": data.count("\n", 0, m.start()) + 1,
                "static_reference_only": True,
            })
    return sites


def manifest_inventory(manifest_path, classes):
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    if root.tag != "manifest":
        raise ValueError("Android manifest missing root")
    package = root.get("package")
    app = root.find("application")
    if not package or app is None:
        raise ValueError("Android package/application declaration missing")
    components = []
    for tag in ("activity", "service", "receiver", "provider"):
        for elem in app.findall(tag):
            name = elem.get(ANDROID_NAME)
            if not name:
                raise ValueError("Android component missing android:name")
            qualified = (package + name if name.startswith(".")
                         else package + "." + name if "." not in name
                         else name)
            descriptor = "L" + qualified.replace(".", "/") + ";"
            components.append({
                "kind": tag, "declared_name": name,
                "smali_class_declared": descriptor in classes,
                "runtime_component_invoked": False,
            })
    if not components:
        raise ValueError("No Android manifest components")
    return {"package": package, "components": sorted(
        components, key=lambda x:(x["kind"], x["declared_name"]))}


def obb_handoff(meta):
    state = meta.get("state")
    if state == "git_lfs_pointer_only":
        if (meta.get("lfs_declared_size_bytes") != OBB_SIZE
                or meta.get("lfs_declared_sha256") != OBB_SHA):
            raise ValueError("Unexpected OBB LFS pointer or content identity")
    elif state == "materialized_non_pointer":
        if (meta.get("actual_size_bytes") != OBB_SIZE
                or meta.get("content_sha256") != OBB_SHA):
            raise ValueError("Materialized OBB does not match pinned content hash")
    else:
        raise ValueError("Expected OBB pointer or explicitly verified local content")
    return {
        "state": state,
        "expected_size_bytes": OBB_SIZE,
        "expected_sha256": OBB_SHA,
        "materialized_sha256_verified": state == "materialized_non_pointer",
        "assets_classified": 0,
        "all_entries_extracted_or_rebuilt": False,
        "format_fat32_or_zip_proven": False,
        "next_gate": "manual explicit LFS materialization and content format audit",
        "t29_done": False,
    }


def summarize(static_report, callsites, manifest, obb):
    gl = [m for m in static_report["native_methods"] if m["class"] == GL_CLASS]
    found = [m["method"] for m in gl]
    if len(gl) != 12 or set(found) != EXPECTED_GL_METHODS:
        raise ValueError("GL2JNILib method surface drifted; manual review required")
    if not manifest["components"]:
        raise ValueError("Android manifest inventory empty")
    rows = []
    for method in sorted(gl, key=lambda m:m["method"]):
        key = (method["class"], method["method"], method["descriptor"])
        references = callsites.get(key, [])
        rows.append({
            "java_class": method["class"], "method": method["method"],
            "descriptor": method["descriptor"],
            "jni_export_candidates": method["jni_export_candidates"],
            "smali_invocation_sites": references,
            "static_invocation_count": len(references),
            "native_binding_runtime_proven": False,
            "native_effects_and_state_proven": False,
        })
    return {
        "schema": 1, "tracks": ["T27", "T29"],
        "reference_arm_elf_sha256": baseline.EXPECTED_ELF,
        "source_evidence": "manifest_smali_ELF_dynsym_and_obb_pointer_only",
        "smali_files": static_report["smali_files_scanned"],
        "smali_classes": static_report["smali_classes_declared"],
        "declared_natives_total": static_report["native_method_count"],
        "gl2jnilib_native_method_count": len(rows),
        "gl2jnilib_methods": rows,
        "manifest": manifest,
        "jni_onload_exported": static_report["jni_onload_exported"],
        "jni_runtime_traces_captured": 0,
        "register_natives_runtime_binding_proven": False,
        "bidirectional_behavioral_jni_mapping_complete": False,
        "obb": obb,
        "original_game_executed": False,
        "new_semantic_certificates": 0,
        "t27_done": False,
        "t29_done": False,
    }


def run(root):
    root = Path(root)
    module = root / "FFT_Android_Mod"
    base = baseline.run(root)
    smali = module / "src/smali"
    gl = [m for m in base["native_methods"] if m["class"] == GL_CLASS]
    inv = invocations(smali, gl)
    manifest_path = module / "src/AndroidManifest.xml"
    manifest = manifest_inventory(
        manifest_path,
        {"L" + name.replace(".smali", "") + ";"
         for name in (
            p.relative_to(smali).as_posix() for p in smali.rglob("*.smali")
         )},
    )
    return summarize(base, inv, manifest, obb_handoff(base["obb"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = run(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, sort_keys=True, indent=2) + "\n",
                           encoding="utf-8")
    print("T27_JNI_DECLARED=" + str(output["gl2jnilib_native_method_count"]))
    print("T27_STATIC_SITES=" + str(sum(
        m["static_invocation_count"] for m in output["gl2jnilib_methods"])))
    print("T29_OBB_STATE=" + output["obb"]["state"])
    print("T27_RUNTIME_BRIDGE_CERTIFIED=0")
    print("T29_ASSETS_CLASSIFIED=0")


if __name__ == "__main__":
    main()
