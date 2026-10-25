"""Safety regression tests for bounded unconditional ARM sound trampolines."""
import unittest
from pathlib import Path
from unittest.mock import patch

import semantic_sound_chain as chain
import semantic_branch_microexec as branches


def b_code(address, target):
    delta=target-(address+8)
    if delta%4 or not -(1<<25)<=delta<(1<<25):
        raise ValueError("ARM B cannot encode target")
    return (0xEA000000|((delta>>2)&0xFFFFFF)).to_bytes(4,"little")


class SoundTailChainTests(unittest.TestCase):
    def test_first_branch_and_second_boundary(self):
        instructions={
            chain.ENTRY:b_code(chain.ENTRY,chain.FIRST_TARGET),
            chain.FIRST_TARGET:bytes.fromhex("0100a0e3"),
        }
        with patch.object(chain.semantic_evidence,"read_function",
                          side_effect=lambda binary,pc,n: instructions[pc]):
            visited,boundary,reason=chain.follow(Path("/dummy"))
        self.assertEqual(list(visited),[chain.ENTRY])
        self.assertEqual(boundary,chain.FIRST_TARGET)
        self.assertIn("non-B",reason)
        for value in chain.ARGUMENTS:
            trace=chain.emulate(visited,boundary,value,branches.CPSR_STATES[0])
            self.assertEqual(trace,[chain.ENTRY,chain.FIRST_TARGET])

    def test_two_branch_chain_stops_before_third_opcode(self):
        third=0x211000
        instructions={
            chain.ENTRY:b_code(chain.ENTRY,chain.FIRST_TARGET),
            chain.FIRST_TARGET:b_code(chain.FIRST_TARGET,third),
            third:bytes.fromhex("1eff2fe1"),
        }
        with patch.object(chain.semantic_evidence,"read_function",
                          side_effect=lambda binary,pc,n: instructions[pc]):
            visited,boundary,_=chain.follow(Path("/dummy"))
        self.assertEqual(boundary,third)
        self.assertEqual(list(visited),[chain.ENTRY,chain.FIRST_TARGET])
        self.assertEqual(chain.emulate(visited,boundary,0,
                         branches.CPSR_STATES[1]),
                         [chain.ENTRY,chain.FIRST_TARGET,third])

    def test_wrong_first_target_rejected(self):
        with patch.object(chain.semantic_evidence,"read_function",
                          return_value=b_code(chain.ENTRY,chain.FIRST_TARGET+4)):
            with self.assertRaisesRegex(ValueError,"no longer jumps"):
                chain.follow(Path("/dummy"))

    def test_cycle_rejected(self):
        instructions={
            chain.ENTRY:b_code(chain.ENTRY,chain.FIRST_TARGET),
            chain.FIRST_TARGET:b_code(chain.FIRST_TARGET,chain.ENTRY),
        }
        with patch.object(chain.semantic_evidence,"read_function",
                          side_effect=lambda binary,pc,n: instructions[pc]):
            with self.assertRaisesRegex(ValueError,"Cyclic"):
                chain.follow(Path("/dummy"))

    def test_unmapped_target_stops_without_executing_unknown(self):
        def read(binary,pc,n):
            if pc==chain.ENTRY:
                return b_code(chain.ENTRY,chain.FIRST_TARGET)
            raise ValueError("No executable segment")
        with patch.object(chain.semantic_evidence,"read_function",side_effect=read):
            visited,boundary,reason=chain.follow(Path("/dummy"))
        self.assertEqual(boundary,chain.FIRST_TARGET)
        self.assertIn("not covered",reason)
        self.assertEqual(chain.emulate(visited,boundary,1,
                         branches.CPSR_STATES[0]),
                         [chain.ENTRY,chain.FIRST_TARGET])


if __name__=="__main__":
    unittest.main()
