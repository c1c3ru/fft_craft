#!/usr/bin/env python3
"""Aggregate independent Android Context/JNI path measurements across APIs.

Do not include actual path contents, infer a global maximum or attribute
measurements to the original game's native process. Fail closed on malformed
or mislabeled platform observations.
"""
import argparse
import json
from pathlib import Path

PACKAGE="com.square_enix.android_googleplay.FFT_en2"
BOUND=242
METHODS=("GetIntPath","GetExt1Path")


def consolidate(files, expected_apis):
    if len(set(expected_apis)) != len(expected_apis) or not expected_apis:
        raise ValueError("Expected API matrix invalid")
    if len(files)!=len(expected_apis):
        raise ValueError("Every API must contribute exactly one JSON artifact")
    records={}
    for file in files:
        source=json.loads(file.read_text(encoding="utf-8"))
        sdk=source.get("android_sdk")
        if type(sdk) is not int or sdk not in expected_apis or sdk in records:
            raise ValueError("Unexpected, missing, or duplicate API measurement")
        if (source.get("status")!="sampled_not_a_global_bound"
                or source.get("running_original_game_apk") is not False
                or source.get("original_strcpy_executed") is not False
                or source.get("same_package_name_as_original_game") is not True
                or source.get("package_identity")!=PACKAGE
                or source.get("native_method")!="JNI GetStringUTFLength"):
            raise ValueError("Incomplete diagnostic APK provenance")
        if source.get("native_ascii_242")!=242 or source.get("native_ascii_243")!=243:
            raise ValueError("JNI boundary counters absent")
        if source.get("native_nul_utf_bytes_hex")!="61c08062":
            raise ValueError("ART NUL byte evidence absent")
        if source.get("native_emoji_utf_bytes_hex")!="f09f9880":
            raise ValueError("ART emoji byte evidence absent")
        observations={}
        for method in METHODS:
            row=source.get(method)
            if not isinstance(row,dict) or type(row.get("present")) is not bool:
                raise ValueError("Malformed method measurement: "+method)
            if row["present"]:
                n=row.get("jni_mutf8_byte_length")
                if type(n) is not int or n<0 or row.get("within_242_bytes")!=(n<=BOUND):
                    raise ValueError("Inconsistent JNI count: "+method)
                observations[method]={"present":True,"jni_bytes":n,
                                      "remaining_budget_bytes":BOUND-n,
                                      "observed_within_budget":n<=BOUND}
            else:
                if row.get("jni_mutf8_byte_length") is not None:
                    raise ValueError("Absent path must have null count")
                observations[method]={"present":False,"jni_bytes":None,
                                      "remaining_budget_bytes":None,
                                      "observed_within_budget":None}
        records[sdk]=observations

    return {
        "schema":1,
        "source":"independent_test_only_APK_same_package_ID",
        "expected_api_levels":sorted(expected_apis),
        "diagnostic_apk_path_samples":len(records),
        "maximum_java_path_jni_bytes_for_260_byte_layout":BOUND,
        "api_observations":[{"android_api":sdk,"methods":records[sdk]}
                            for sdk in sorted(records)],
        "observed_violation_of_layout_precondition":any(
            value["observed_within_budget"] is False
            for methods in records.values() for value in methods.values()),
        "global_maximum_proven":False,
        "original_game_apk_executed":False,
        "original_native_elf_executed":False,
        "libc_strcpy_on_untrusted_input_executed":False,
        "java_jni_path_safety_certificates":0,
        "path_contents_retained":False,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--expected-apis",nargs="+",type=int,required=True)
    args=p.parse_args()
    files=sorted(args.input.rglob("a04-android-api-*.json"))
    data=consolidate(files,args.expected_apis)
    result=json.dumps(data,indent=2,sort_keys=True)+"\n"
    args.output.write_text(result,encoding="utf-8")
    print("A04_ANDROID_MATRIX_SAMPLED_API_LEVELS="+
          ",".join(str(x) for x in data["expected_api_levels"]))
    print("A04_ANDROID_MATRIX_OBSERVED_VIOLATIONS="+
          str(int(data["observed_violation_of_layout_precondition"])))
    print("A04_ANDROID_MATRIX_GLOBAL_BOUND_PROVEN=0")


if __name__=="__main__":
    main()
