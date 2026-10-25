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
        self.assertIn((0x1000, "fallthrough"), semantic_cfg.predecessors(graph)[0x1004])
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


    def test_dominator_sets_in_entry_reachable_graph(self):
        instructions = decode("000050e3 0300000a 002094e5 4020c2e3 002084e5")
        graph, _ = semantic_cfg.build_cfg(instructions)
        dom = semantic_cfg.modeled_dominators(graph, 0x1000)
        self.assertEqual(dom[0x1000], {0x1000})
        self.assertEqual(dom[0x1008], {0x1000, 0x1004, 0x1008})
        self.assertIn(0x1004, dom[0x1010])
        self.assertEqual(len(semantic_cfg.entry_reachable(graph, 0x1000)), 5)

    def test_conditional_gate_is_model_only(self):
        instructions = decode("000050e3 0300000a 002094e5 4020c2e3 002084e5")
        graph, _ = semantic_cfg.build_cfg(instructions)
        effects = semantic_facts.bitmask_effects(instructions)
        guards = semantic_paths.branch_guards(instructions)
        enriched = semantic_cfg.modeled_guard_dominance(effects, guards, graph, 0x1000)
        self.assertTrue(enriched[0]["reachable_from_entry"])
        self.assertEqual(enriched[0]["modeled_dominating_guards"][0]["branch"], 0x1004)
        self.assertTrue(enriched[0]["modeled_dominating_guards"][0]["modeled_one_sided"])

    def test_branch_alternatives_reconverge(self):
        instructions = decode("000050e3 0200000a 002094e5 4020c2e3 002084e5 fbffffea")
        graph, _ = semantic_cfg.build_cfg(instructions)
        guards = semantic_paths.branch_guards(instructions)
        effects = semantic_facts.bitmask_effects(instructions)
        result = semantic_cfg.modeled_guard_dominance(effects, guards, graph, 0x1000)
        self.assertFalse(result[0]["modeled_dominating_guards"][0]["modeled_one_sided"])

    def test_unreachable_write_is_not_assigned_dominators(self):
        graph = {0x1000: [(0x1004, "fallthrough")], 0x1004: [],
                 0x2000: [(0x2004, "fallthrough")], 0x2004: []}
        self.assertEqual(semantic_cfg.modeled_dominators(graph, 0x1000),
                         {0x1000: {0x1000}, 0x1004: {0x1000, 0x1004}})
        result = semantic_cfg.modeled_guard_dominance(
            [{"addresses": [0x2004]}], [], graph, 0x1000)
        self.assertFalse(result[0]["reachable_from_entry"])
        self.assertEqual(result[0]["modeled_dominating_guards"], [])

    def test_loop_backedge_dominator_fixed_point(self):
        graph = {
            0x1000: [(0x1004, "fallthrough")],
            0x1004: [(0x1008, "taken"), (0x100c, "not_taken")],
            0x1008: [(0x1004, "backedge")],
            0x100c: [],
        }
        dom = semantic_cfg.modeled_dominators(graph, 0x1000)
        self.assertEqual(dom[0x100c], {0x1000, 0x1004, 0x100c})
        self.assertEqual(dom[0x1008], {0x1000, 0x1004, 0x1008})


if __name__ == "__main__":
    unittest.main()
