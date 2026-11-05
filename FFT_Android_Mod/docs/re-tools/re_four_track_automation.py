#!/usr/bin/env python3
"""Fail-closed CI orchestration for T06/T12, B01, A04, and T14..T26.

No tool invocation here can certify the original ELF or Android app. Each lane
uses independent existing proof scripts; this file aggregates only bounded
evidence and never changes source, task states or certificates.
"""
import argparse
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = Path(__file__).resolve().parent
SHA = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
LANES = ("t06_t12", "b01", "a04", "t14_t26")
TASKS = ["T%02d" % n for n in range(14, 27)]
BLOCKERS = {
    "t06_t12": ["original external callee effects unknown",
                "12 symbol-tail bytes and reachability unresolved"],
    "b01": ["C++ class layouts and real calling contexts unproven",
            "external effects and complete stack frames unresolved"],
    "a04": ["no original Android process Java->JNI->R1 evidence",
            "242-byte budget not proven globally"],
    "t14_t26": ["local regression tests do not imply integrated subsystems",
                 "real Android/OBB/gameplay replay pending"],
}


def load(path):
    path = Path(path)
    if not path.is_file() or path.stat().st_size > 5 * 1024 * 1024:
        raise ValueError("Missing or oversized proof file")
    return json.loads(path.read_text(encoding="utf-8"))


def source_count(binary=None, ledger=None):
    binary = binary or ROOT / "src/lib/armeabi/libgl2jni.so"
    ledger = ledger or ROOT / "docs/re-results/semantic-certificates.json"
    if hashlib.sha256(Path(binary).read_bytes()).hexdigest() != SHA:
        raise ValueError("Original ELF identity differs from pinned baseline")
    doc = load(ledger)
    if (not isinstance(doc, dict) or not doc or
            any(not isinstance(x, dict) or x.get("status") != "certified"
                for x in doc.values())):
        raise ValueError("Certificate ledger is not a verified population")
    return len(doc)


def eq(doc, field, expected):
    value = doc.get(field)
    if type(value) is not type(expected) or value != expected:
        raise ValueError("Proof gate failed: " + field)


def parse_a04(stdout):
    if len(stdout) > 64000:
        raise ValueError("Oversized JNI stdout")
    data = {}
    for line in stdout.splitlines():
        if not line.startswith("A04_JNI_"):
            continue
        if "=" not in line:
            raise ValueError("Malformed JNI host record")
        key, val = line.split("=", 1)
        if key in data or not re.fullmatch(r"A04_JNI_[A-Z0-9_]+", key):
            raise ValueError("Duplicate or invalid JNI key")
        if not re.fullmatch(r"[0-9]{1,9}", val):
            raise ValueError("Invalid JNI host count")
        data[key] = int(val)
    return data


def evaluate(lane, proof, certificates):
    if lane not in LANES or not isinstance(proof, dict):
        raise ValueError("Unknown lane or invalid proof data")
    if lane == "t06_t12":
        for k, v in (("original_elf_sha256", SHA),
                     ("wrapper_slices_tested", 2),
                     ("differential_scenarios_passed", 7),
                     ("new_semantic_certificates", 0),
                     ("new_structural_approvals", 0),
                     ("real_external_callees_untested", True),
                     ("T06_done", False)):
            eq(proof, k, v)
        rows = proof.get("wrappers")
        if not isinstance(rows, list) or len(rows) != 2:
            raise ValueError("T06 wrapper evidence incomplete")
        if sorted(len(x.get("scenarios", [])) for x in rows) != [3, 4]:
            raise ValueError("T06 scenario population truncated")
        if sorted(x.get("unattributed_trailing_symbol_bytes") for x in rows) != [0, 12]:
            raise ValueError("T06 unassigned bytes not preserved")
        observed = {"wrappers": 2, "bounded_differentials": 7,
                    "unassigned_bytes": 12}
        scope = "original_ELF_wrappers_with_mocked_external_callees"
    elif lane == "b01":
        for k, v in (("elf_sha256", SHA), ("unique_methods", 7),
                     ("original_elf_vs_named_cpp_differentials", 672),
                     ("new_semantic_certificates", 0), ("B01_done", False),
                     ("cpp_class_layout_proven", False),
                     ("whole_program_call_context_proven", False)):
            eq(proof, k, v)
        if len(proof.get("entries", [])) != 7:
            raise ValueError("B01 original method evidence incomplete")
        observed = {"cpp_methods": 7, "bounded_differentials": 672}
        scope = "original_ELF_12byte_bodies_without_real_objects"
    elif lane == "a04":
        eq(proof, "A04_JNI_HOST_CASES", 271)
        eq(proof, "A04_JNI_MODIFIED_UTF8_CONFIRMED", 1)
        eq(proof, "A04_JNI_REAL_ANDROID_PATH_SAMPLES", 0)
        observed = {"host_jni_cases": 271, "original_app_runtime_samples": 0}
        scope = "host_JNI_not_game_Android_runtime"
    else:
        for k, v in (("format", "t14_t26_unittest_v1"),
                     ("test_modules_count", 29), ("tests_passed", True),
                     ("errors", 0), ("failures", 0),
                     ("native_stage_ctest_passed", True)):
            eq(proof, k, v)
        if proof.get("tasks_with_tests") != TASKS:
            raise ValueError("T14..T26 test suite incomplete")
        n = proof.get("tests_run")
        if type(n) is not int or n < 29:
            raise ValueError("Too few vertical tests executed")
        observed = {"task_suites": 13, "test_modules": 29, "test_cases": n,
                    "native_stage_smoke": True}
        scope = "host_component_slices_and_CMake_CTest_only"
    return {
        "schema": 1, "lane": lane, "elf_sha256": SHA,
        "ledger_certificates": certificates, "observed": observed, "scope": scope,
        "blockers": BLOCKERS[lane], "new_semantic_certificates": 0,
        "task_states_changed": False, "full_equivalence_proven": False,
        "original_android_app_verified": False, "independent_review_required": True,
    }


def run_vertical(output):
    groups, names = [], []
    loader = unittest.TestLoader()
    for task in TASKS:
        files = sorted(TOOLS.glob("test_" + task.lower() + "_*.py"))
        if not files:
            raise ValueError("Missing test suite for " + task)
        for f in files:
            names.append(f.name)
            suite = loader.discover(str(TOOLS), pattern=f.name)
            if suite.countTestCases() < 1:
                raise ValueError("Empty test module")
            groups.append(suite)
    if len(names) != 29 or len(names) != len(set(names)):
        raise ValueError("Expected 29 distinct host regression modules")
    res = unittest.TextTestRunner(stream=sys.stderr).run(unittest.TestSuite(groups))
    if not res.wasSuccessful():
        raise RuntimeError("T14..T26 regressions failed")
    report = {"format": "t14_t26_unittest_v1", "tasks_with_tests": TASKS,
              "test_modules_count": len(names), "tests_run": res.testsRun,
              "tests_passed": True, "errors": len(res.errors),
              "failures": len(res.failures), "native_stage_ctest_passed": False}
    Path(output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("T14_T26_TEST_MODULES=" + str(len(names)))


def verify_lane(doc):
    if not isinstance(doc, dict) or doc.get("lane") not in LANES:
        raise ValueError("Unknown lane artifact")
    if doc.get("schema") != 1 or doc.get("elf_sha256") != SHA:
        raise ValueError("Foreign lane artifact")
    for key, expected in (("new_semantic_certificates", 0),
                          ("task_states_changed", False),
                          ("full_equivalence_proven", False),
                          ("original_android_app_verified", False),
                          ("independent_review_required", True)):
        eq(doc, key, expected)
    if doc.get("blockers") != BLOCKERS[doc["lane"]]:
        raise ValueError("Unexpected or missing blockers")
    return doc["lane"]


def consolidate(directory, ledger_count):
    files = sorted(Path(directory).glob("re-four-track-*/*.json"))
    if len(files) != 4:
        raise ValueError("Four lane artifacts required")
    lanes = {}
    for f in files:
        d = load(f)
        lane = verify_lane(d)
        if lane in lanes:
            raise ValueError("Duplicate lane")
        eq(d, "ledger_certificates", ledger_count)
        lanes[lane] = d
    if set(lanes) != set(LANES):
        raise ValueError("Missing mandatory lane")
    return {"schema": 1, "elf_sha256": SHA, "ledger_certificates": ledger_count,
            "lanes_tested": len(lanes), "lanes": [lanes[x] for x in LANES],
            "new_semantic_certificates": 0, "task_states_changed": False,
            "full_app_reconstructed": False}


def markdown(doc):
    lines = ["# Quatro frentes de engenharia reversa — relatório automático", "",
             "Certificados existentes: **%d**; novos: **0**." %
             doc["ledger_certificates"], "",
             "| Frente | Observações | Escopo |", "|---|---|---|"]
    for x in doc["lanes"]:
        observed = ", ".join("%s=%s" % (k, v) for k, v in
                             sorted(x["observed"].items()))
        lines.append("| %s | %s | %s |" % (x["lane"], observed, x["scope"]))
    lines.extend(["", "## Pendências de evidência", ""])
    for x in doc["lanes"]:
        lines.append("**%s:** %s." % (x["lane"], "; ".join(x["blockers"])))
    lines.extend(["", "Nenhuma aprovação, certificado ou estado T01–T40 é",
                  "alterado por esta automação. Testes de host não constituem",
                  "validação do APK/OBB no Android original.", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("vertical")
    v.add_argument("--output", type=Path, required=True)
    e = sub.add_parser("emit")
    e.add_argument("--lane", choices=LANES, required=True)
    e.add_argument("--evidence", type=Path, required=True)
    e.add_argument("--ctest-passed", action="store_true")
    e.add_argument("--output", type=Path, required=True)
    c = sub.add_parser("combine")
    c.add_argument("--artifacts", type=Path, required=True)
    c.add_argument("--json-output", type=Path, required=True)
    c.add_argument("--md-output", type=Path, required=True)
    a = parser.parse_args()
    if a.cmd == "vertical":
        source_count()
        run_vertical(a.output)
        return
    count = source_count()
    if a.cmd == "emit":
        proof = (parse_a04(a.evidence.read_text(encoding="utf-8"))
                 if a.lane == "a04" else load(a.evidence))
        if a.lane == "t14_t26" and a.ctest_passed:
            proof["native_stage_ctest_passed"] = True
        report = evaluate(a.lane, proof, count)
        verify_lane(report)
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(report, indent=2) + "\n",
                            encoding="utf-8")
        print("RE_FOUR_TRACK_" + a.lane.upper() + "_PASS=1")
    else:
        report = consolidate(a.artifacts, count)
        a.json_output.parent.mkdir(parents=True, exist_ok=True)
        a.md_output.parent.mkdir(parents=True, exist_ok=True)
        a.json_output.write_text(json.dumps(report, indent=2) + "\n",
                                 encoding="utf-8")
        a.md_output.write_text(markdown(report), encoding="utf-8")
        print("RE_FOUR_TRACK_LANES=4")
        print("RE_FOUR_TRACK_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
