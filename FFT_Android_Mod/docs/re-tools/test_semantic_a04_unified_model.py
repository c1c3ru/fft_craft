#!/usr/bin/env python3
"""One C API for original A04 null and non-null paths; regression vs ARM."""
import ctypes
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from semantic_evidence import read_function
from semantic_a04_b6620_zero_differential import run_original as run_null_arm
from semantic_a04_nonzero_full_differential import (
    original_sections, run_original as run_nonnull_arm,
    META_OFFSET, SIZE)
from semantic_a04_714a0_slot import SHA
import semantic_a04_b6620_xrefs as xrefs

ROOT = Path(__file__).resolve().parents[2]
BINARY = ROOT / "src/lib/armeabi/libgl2jni.so"
MODELS = Path(__file__).resolve().parent / "c-models"


class DirectCallEncoderTests(unittest.TestCase):
    def test_positive_known_direct_calls(self):
        for pc, destination in ((0xab674, 0xb6620), (0xb461c, 0xb45d0)):
            op = xrefs.encode_test_bl(pc, destination)
            self.assertEqual(xrefs.decode_arm_bl(op, pc), destination)

    def test_rejects_other_a32_branch_classes(self):
        self.assertIsNone(xrefs.decode_arm_bl(0xeaffffff, 0x1000))
        self.assertIsNone(xrefs.decode_arm_bl(0xfa000000, 0x1000))
        self.assertIsNone(xrefs.decode_arm_bl(0xe12fff1e, 0x1000))

    def test_rejects_non_encodable_bl(self):
        with self.assertRaises(ValueError):
            xrefs.encode_test_bl(0x1000, 0x1003)


def run_differential():
    if hashlib.sha256(BINARY.read_bytes()).hexdigest() != SHA:
        raise ValueError("Original ARM ELF baseline changed")
    sections = original_sections()
    original_null = read_function(BINARY, 0xb6620, 0x34)
    with tempfile.TemporaryDirectory(prefix="a04-unified-") as temp:
        lib = Path(temp)/"unified.so"
        subprocess.run(["cc", "-std=c11", "-Wall", "-Wextra", "-Werror",
                        "-O2", "-shared", "-fPIC",
                        str(MODELS/"a04_b6620_model.c"),
                        str(MODELS/"a04_b6620_zero.c"),
                        str(MODELS/"a04_nonzero_full.c"),
                        str(MODELS/"a04_sjis_slash_loop.c"),
                        str(MODELS/"a04_sjis_lead.c"),
                        "-o",str(lib)],check=True)
        model = ctypes.CDLL(str(lib)).a04_b6620_model
        model.argtypes = (ctypes.c_void_p,ctypes.c_size_t,
                          ctypes.c_void_p,ctypes.c_size_t)
        model.restype = ctypes.c_int
        null_cases, nonnull_cases, refused = 0, 0, 0

        for metadata in (0,1,0x12345678,0xffffffff):
            for r4 in (0,0xabcdef01):
                for nzcv in (0,0xf0000000):
                    original = run_null_arm(original_null,metadata,r4,nzcv)
                    output=bytearray(b"\xa5"*SIZE)
                    output[META_OFFSET:META_OFFSET+4] = metadata.to_bytes(4,"little")
                    ptr=(ctypes.c_uint8*SIZE).from_buffer(output)
                    if model(ptr,SIZE,None,0) != 1 or bytes(output) != original:
                        raise AssertionError("Unified null branch differs from original ARM")
                    null_cases+=1

        examples = [b"", b"alpha", b"\\", b"dir\\name",
                    b"\x81\\", b"\xe0\\",
                    b"\\x"*12, b"\x9f\\\xfc\\",
                    bytes([i for i in range(1,65)]),
                    b"z"*0x103]
        for sample in examples:
            for meta in (0,0xf0e1d2c3):
                for flags in (0,0xf0000000):
                    observed=run_nonnull_arm(sections,sample,meta,flags)
                    dst=bytearray(b"\xa5"*SIZE)
                    dst[META_OFFSET:META_OFFSET+4]=meta.to_bytes(4,"little")
                    src=bytearray(b"\x7c"*SIZE)
                    src[:len(sample)] = sample
                    src[len(sample)] = 0
                    dp=(ctypes.c_uint8*SIZE).from_buffer(dst)
                    sp=(ctypes.c_uint8*SIZE).from_buffer(src)
                    if model(dp,SIZE,sp,SIZE) != 1 or bytes(dst) != observed:
                        raise AssertionError("Unified nonnull branch differs from original ARM")
                    nonnull_cases += 1

        # These rejected states are NOT run in the unchecked ARM original.
        for small in (0,0x107):
            mem=bytearray(b"\xa5"*SIZE)
            before=bytes(mem)
            d=(ctypes.c_uint8*SIZE).from_buffer(mem)
            if model(d,small,None,0) != 0 or bytes(mem) != before:
                raise AssertionError("Unified API failed on invalid destination size")
            refused += 1

        # Overlapping source/dest is outside the original strcpy contract.
        for offset in (0,2,0x100):
            mem=bytearray(b"z"*SIZE)
            before=bytes(mem)
            d=(ctypes.c_uint8*SIZE).from_buffer(mem)
            s=ctypes.cast(ctypes.byref(d,offset),ctypes.c_void_p)
            if model(d,SIZE,s,SIZE-offset) != 0 or bytes(mem) != before:
                raise AssertionError("Unified API failed to reject aliased input")
            refused += 1

        for content in (b"n"*0x104,b"n"*0x105):
            mem=bytearray(b"\xa5"*SIZE)
            src=bytearray(b"\x7c"*SIZE)
            src[:len(content)]=content
            src[len(content)]=0
            initial=bytes(mem)
            d=(ctypes.c_uint8*SIZE).from_buffer(mem)
            s=(ctypes.c_uint8*SIZE).from_buffer(src)
            if model(d,SIZE,s,SIZE) != 0 or bytes(mem) != initial:
                raise AssertionError("Unified API failed to reject unsafe copy")
            refused += 1
        if model(None,SIZE,None,0) != 0:
            raise AssertionError("Unified API accepted null destination")
        refused += 1
    return {"sha256":SHA,"null_original_arm_cases":null_cases,
            "nonnull_original_arm_cases":nonnull_cases,
            "invalid_states_rejected_without_running_original_arm":refused,
            "mismatches":0,"new_certificates":0}


if __name__=="__main__":
    unittest.main(module=None, exit=False, argv=["ignored"])
    print(json.dumps(run_differential(), sort_keys=True))
