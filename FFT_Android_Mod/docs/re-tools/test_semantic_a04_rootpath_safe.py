"""Host-only bounded rootpath model; no claim of original Android libc safety."""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

MODEL=Path(__file__).resolve().parent/"c-models/a04_rootpath_safe.c"
SUFFIX=b"/base/fftpack.bin\x00"


class SafeRootpathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(prefix="a04-rootpath-")
        output=Path(cls.temp.name)/"a04_rootpath.so"
        subprocess.run(["cc","-std=c11","-O2","-Wall","-Wextra","-Werror",
                        "-shared","-fPIC",str(MODEL),"-o",str(output)],check=True)
        cls.fn=ctypes.CDLL(str(output)).a04_build_fftpack_path
        cls.fn.argtypes=[ctypes.c_void_p,ctypes.c_size_t,
                         ctypes.c_void_p,ctypes.c_size_t]
        cls.fn.restype=ctypes.c_int

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def call(self, payload, capacity=260, length=None, alias=False):
        data=bytearray(b"\xa5"*max(260,capacity))
        dest=(ctypes.c_uint8*len(data)).from_buffer(data)
        src=(ctypes.c_uint8*len(payload)).from_buffer_copy(payload)
        ptr=(ctypes.c_void_p(ctypes.addressof(dest)) if alias
             else ctypes.c_void_p(ctypes.addressof(src)))
        if length is None:
            length=len(payload)
        return self.fn(dest,capacity,ptr,length),data

    def test_all_allowed_byte_lengths_preserve_suffix_and_remaining_bytes(self):
        cases=0
        for n in range(243):
            for marker in (b"a",b"/",b"\x81"):
                payload=marker*n
                ok,data=self.call(payload)
                self.assertEqual(ok,1)
                expected=payload+SUFFIX
                self.assertEqual(data[:len(expected)],expected)
                self.assertEqual(data[len(expected):],b"\xa5"*(len(data)-len(expected)))
                cases+=1
        self.assertEqual(cases,729)

    def test_above_242_rejected_without_writes(self):
        for size in (243,244,260,500):
            ok,out=self.call(b"x"*size)
            self.assertEqual(ok,0)
            self.assertEqual(out,b"\xa5"*len(out))

    def test_insufficient_output_capacity_refused(self):
        ok,out=self.call(b"x"*242,259)
        self.assertEqual(ok,0)
        self.assertEqual(out,b"\xa5"*len(out))

    def test_embedded_nul_refused_without_writes(self):
        ok,out=self.call(b"abc\x00def")
        self.assertEqual(ok,0)
        self.assertEqual(out,b"\xa5"*len(out))

    def test_overlapping_buffers_refused(self):
        ok,out=self.call(b"abcd",alias=True)
        self.assertEqual(ok,0)
        self.assertEqual(out,b"\xa5"*len(out))

    def test_null_arguments_refused(self):
        self.assertEqual(self.fn(None,260,None,0),0)


if __name__=="__main__":
    unittest.main()
