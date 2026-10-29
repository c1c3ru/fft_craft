#!/usr/bin/env python3
"""Cross-link original ELF Java selector names to decompiled StorageUtil smali.

This verifies the two methods used by CAPP_INFO::Init. It DOES NOT infer
a runtime path length, NUL byte count or successful Android initialization.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from semantic_a04_java_path_lookup import audit as native_audit
from semantic_a04_714a0_slot import SHA

CLASS="Lcom/yox_project/silver_arrow/StorageUtil;"
METHODS={
    "GetIntPath": {
        "header":".method public static GetIntPath()Ljava/lang/String;",
        "expected_api":["Landroid/content/Context;->getFilesDir()Ljava/io/File;",
                        "Ljava/io/File;->getPath()Ljava/lang/String;"]},
    "GetExt1Path": {
        "header":".method public static GetExt1Path()Ljava/lang/String;",
        "expected_api":["Landroid/content/Context;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;",
                        "Ljava/io/File;->getPath()Ljava/lang/String;"]},
}
CAPACITY=260
ROOT_SUFFIX_BYTES=7
FFT_SUFFIX_BYTES=12


def extract_method(smali, header):
    lines=smali.splitlines()
    starts=[i for i,s in enumerate(lines) if s.strip()==header]
    if len(starts)!=1:
        raise ValueError(f"Original Java method missing or duplicated: {header}")
    start=starts[0]
    ends=[i for i in range(start+1,len(lines)) if lines[i].strip()==".end method"]
    if not ends:
        raise ValueError("Unterminated smali method")
    return "\n".join(lines[start:ends[0]+1])


def analyze(binary,smali_file):
    if hashlib.sha256(binary.read_bytes()).hexdigest()!=SHA:
        raise ValueError("Original native ARM ELF changed")
    raw=smali_file.read_bytes()
    source=raw.decode("utf-8")
    if ".class public final "+CLASS not in source:
        raise ValueError("StorageUtil smali class descriptor changed")
    native=native_audit(binary)
    if native["jni_literals"][0]["static_identifier"].get("ascii_escaped")!=CLASS[1:-1]:
        raise ValueError("Native JNI FindClass and smali descriptor disagree")
    signature=native["jni_literals"][1]["static_identifier"].get("ascii_escaped")
    if signature!="()Ljava/lang/String;":
        raise ValueError("Native JNI signature mismatch")
    selectors=native["selector_entries"]
    if len(selectors)!=7:
        raise ValueError("JNI selector table no longer has seven entries")
    records=[]
    for index,name in enumerate(("GetIntPath","GetExt1Path")):
        entry=selectors[index]
        if entry["static_word_as_possible_pointer"].get("ascii_escaped")!=name:
            raise ValueError("Native selector and Java target disagree")
        info=METHODS[name]
        code=extract_method(source,info["header"])
        for api in info["expected_api"]:
            if api not in code:
                raise ValueError(f"Changed Java path producer {name}: missing {api}")
        if "return-object v0" not in code:
            raise ValueError("Java path no longer returns its path string directly")
        # Absence of a local length guard is not proof of malicious input.
        local_checks=bool(re.search(r"Ljava/lang/String;->(length|getBytes|substring)\(",code))
        records.append({
            "selector":index,"jni_static_method":name,
            "java_smali_method":info["header"],
            "api_calls":info["expected_api"],
            "smali_method_sha256":hashlib.sha256(code.encode("utf-8")).hexdigest(),
            "explicit_local_string_byte_length_gate_seen":local_checks,
            "nul_and_byte_length_verified_at_runtime":False,
            "runtime_value":None})
    return {
        "schema":1,"native_elf_sha256":SHA,
        "smali_sha256":hashlib.sha256(raw).hexdigest(),
        "java_class":CLASS,"jni_signature":signature,
        "used_by_CAPP_INFO_init":records,
        "all_java_selector_names":[entry["static_word_as_possible_pointer"].get("ascii_escaped")
                                   for entry in selectors],
        "candidate_rootpath_field_capacity":CAPACITY,
        "rootpath_suffix_bytes":ROOT_SUFFIX_BYTES,
        "fftpack_suffix_bytes":FFT_SUFFIX_BYTES,
        "max_java_path_bytes_for_both_suffixes":
            CAPACITY-ROOT_SUFFIX_BYTES-FFT_SUFFIX_BYTES,
        "java_utf8_byte_length_limit_proven":False,
        "java_return_is_nul_terminated_by_jni_executed":False,
        "new_certificates":0}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",required=True,type=Path)
    p.add_argument("--smali",required=True,type=Path)
    p.add_argument("--checkpoint",required=True,type=Path)
    a=p.parse_args()
    result=analyze(a.binary,a.smali)
    payload=json.dumps(result,indent=2,sort_keys=True)+"\n"
    a.checkpoint.parent.mkdir(parents=True,exist_ok=True)
    if a.checkpoint.exists() and a.checkpoint.read_text(encoding="utf-8")!=payload:
        raise ValueError("Java StorageUtil source contract replay drift")
    a.checkpoint.write_text(payload,encoding="utf-8")
    print("A04_JAVA_STORAGEUTIL="+result["java_class"])
    print("A04_JAVA_USED_METHODS="+json.dumps(result["used_by_CAPP_INFO_init"]))
    print("A04_JAVA_ROOTPATH_MAX_FOR_FFTPACK="+str(result["max_java_path_bytes_for_both_suffixes"]))
    print("A04_JAVA_RUNTIME_BYTES_PROVEN=0")


if __name__=="__main__":
    main()
