"""GetParam/GetScale static audit regression and exact callsite contracts."""
import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import semantic_getparam_getscale as contracts


def bl_word(source,target):
    offset=target-source-8
    if offset%4:
        raise ValueError("Not ARM-word aligned")
    return (0xEB000000|((offset>>2)&0xFFFFFF)).to_bytes(4,"little")


class CallTargetTests(unittest.TestCase):
    def test_targets_aligned_and_unique(self):
        self.assertEqual(len(contracts.TARGETS),2)
        self.assertEqual(len({i[0] for i in contracts.TARGETS}),2)
        self.assertEqual(contracts.TARGETS[0][0],0x28C320)
        self.assertEqual(contracts.TARGETS[1][0],0x0A6F28)

    def test_callsite_target_accepts_matching_bl(self):
        target,size,_,site=contracts.TARGETS[0]
        def read(binary,address,count):
            return bl_word(site,target) if address==site else (
                bytes.fromhex("0000a0e1")*(size//4))
        with patch.object(contracts.semantic_evidence,"read_function",side_effect=read):
            raw,insns=contracts.decode(Path("/fake"),target,size,site)
        self.assertEqual(len(raw),12)
        self.assertEqual(len(insns),3)

    def test_wrong_bl_or_truncation_fails(self):
        target,size,_,site=contracts.TARGETS[1]
        def wrong(binary,address,count):
            return bl_word(site,target+4) if address==site else (
                bytes.fromhex("0000a0e1")*(size//4))
        with patch.object(contracts.semantic_evidence,"read_function",side_effect=wrong):
            with self.assertRaisesRegex(ValueError,"different destination"):
                contracts.decode(Path("/fake"),target,size,site)
        def truncated(binary,address,count):
            return bl_word(site,target) if address==site else bytes.fromhex("0000a0e1")
        with patch.object(contracts.semantic_evidence,"read_function",side_effect=truncated):
            with self.assertRaisesRegex(ValueError,"truncated"):
                contracts.decode(Path("/fake"),target,size,site)

    def test_inventory_exact_size_and_symbol(self):
        with tempfile.TemporaryDirectory() as tmp:
            csvpath=Path(tmp)/"inventory.csv"
            with csvpath.open("w",newline="") as f:
                writer=csv.DictWriter(f,fieldnames=("address","size","demangled"))
                writer.writeheader()
                for address,size,name,_ in contracts.TARGETS:
                    writer.writerow({"address":f"{address:08x}","size":size,
                                     "demangled":name})
            self.assertTrue(contracts.inventory_check(csvpath))
            body=csvpath.read_text()
            csvpath.write_text(body.replace("16,CGX_SCREEN_CORRECT","20,CGX_SCREEN_CORRECT"))
            with self.assertRaisesRegex(ValueError,"Inventory target drift"):
                contracts.inventory_check(csvpath)

    def test_real_elf_callers_if_present(self):
        binary=contracts.semantic_evidence.ROOT/"src/lib/armeabi/libgl2jni.so"
        if not binary.is_file():
            self.skipTest("Original ELF unavailable")
        for address,size,_,site in contracts.TARGETS:
            with self.subTest(target=address):
                raw,insns=contracts.decode(binary,address,size,site)
                self.assertEqual(len(raw),size)
                self.assertEqual(len(insns),size//4)


if __name__=="__main__":
    unittest.main()
