"""Synthetic CFG and path reachability tests (never semantic proofs)."""
import unittest
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
import semantic_cfg
import semantic_facts
import semantic_paths


def decode(words, start=0x1000):
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    return {ins.address: ins for ins in md.disasm(bytes.fromhex(words), start)}


class ArmCfgTests(unittest.TestCase):
    def test_guard_bypasses_local_flag_clear_on_taken_path(self):
        # CMP r0,#0; BEQ 0x1018 (outside decoded bytes);
        # LDR R2,[R4]; BIC #0x40; STR R2,[R4].
        instructions = decode("000050e3 0300000a 002094e5 4020c2e3 002084e5")
        graph, unknown = semantic_cfg.build_cfg(instructions)
        self.assertIn((0x1008, "not_taken"), graph[0x1004])
        self.assertIn((0x1004, "fallthrough"), graph[0x1000])
        self.assertIn((0x1004, "fallthrough"), semantic_cfg.predecessors(graph)[0x1004])
        self.assertIn((0x1004, "taken", 0x1018), unknown)
        effects = semantic_facts.bitmask_effects(instructions)
        guards = semantic_paths.branch_guards(instructions)
        routes = semantic_cfg.effect_routes(effects, guards, graph)
        self.assertEqual(len(routes), 1)
        self.assertTrue(routes[0]["modeled_guard_routes"][0]["modeled_exclusive"])
        self.assertIsNone(routes[0]["modeled_guard_routes"][0]["taken_path"])
        self.assertEqual(routes[0]["modeled_guard_routes"][0]["other_path"], [0x1008])

    def test_alternative_path_can_reach_same_flag_clear(self):
        # CMP r0,#0; BEQ 0x1014; LDR/BIC/STR; B 0x1008
        # Both branch arms have a route to 0x1008 in this modeled graph.
        instructions = decode("000050e3 0200000a 002094e5 4020c2e3 002084e5 fbffffea")
        graph, unknown = semantic_cfg.build_cfg(instructions)
        self.assertFalse([u for u in unknown if u[0] == 0x1004])
        routes = semantic_cfg.effect_routes(
            semantic_facts.bitmask_effects(instructions),
            semantic_paths.branch_guards(instructions), graph)
        guard = routes[0]["modeled_guard_routes"][0]
        self.assertFalse(guard["modeled_exclusive"])
        self.assertEqual(guard["taken_path"], [0x1014, 0x1008])
        self.assertEqual(guard["other_path"], [0x1008])

    def test_call_returns_without_following_interprocedural_target(self):
        # BL to external; MOV r0, #0; BX LR
        instructions = decode("000000eb 0000a0e3 1eff2fe1")
        graph, _ = semantic_cfg.build_cfg(instructions)
        self.assertEqual(graph[0x1000], [(0x1004, "call_returns")])
        self.assertEqual(graph[0x1008], [])

    def test_unresolved_indirect_branch_recorded(self):
        instructions = decode("13ff2fe1 0000a0e3")
        graph, unknown = semantic_cfg.build_cfg(instructions)
        self.assertEqual(graph[0x1000], [])
        self.assertIn((0x1000, "indirect_transfer", None), unknown)

    def test_jump_table_targets_are_bounded_to_decoded_instructions(self):
        # ADD pc,pc,r0,lsl#2  / MOV r0,#0  / MOV r0,#1
        instructions = decode("00f08fe0 0000a0e3 0100a0e3")
        _, unknown = semantic_cfg.build_cfg(instructions)
        self.assertTrue(any(x[1] == "pc_write" for x in unknown))
        graph, unknown = semantic_cfg.build_cfg(
            instructions, [(0x1000, 0x1000, [0x1004, 0x1008])])
        self.assertIn((0x1004, "jump_table"), graph[0x1000])
        self.assertIn((0x1008, "jump_table"), graph[0x1000])
        self.assertFalse(any(x[1] == "pc_write" for x in unknown))


if __name__ == "__main__":
    unittest.main()
