"""One-hop R1 argument sources remain unknown when direct calls are absent."""
import unittest
from pathlib import Path
from unittest import mock

import semantic_a04_r1_upstream as target


def fake_first():
    return {"source_kinds":{"incoming_abi_argument_candidate":2},
            "callsites":[
                {"callsite":"000a3c4c","candidate_source_kind":
                 "incoming_abi_argument_candidate",
                 "r1_trace":{"terminal":"r1"}},
                {"callsite":"000ab6a4","candidate_source_kind":
                 "incoming_abi_argument_candidate",
                 "r1_trace":{"terminal":"r2"}}]}


def fake_refs():
    return {"direct_bl_candidates":[
        {"callsite":"000a3c4c","target":"000b6620",
         "symbol_owners":[{"name":"BMP_LoadFile","start":"000a3be0",
                           "end":"000a4000"}]},
        {"callsite":"000ab6a4","target":"000b6620",
         "symbol_owners":[{"name":"CEGL2_SHADER_Load","start":"000ab674",
                           "end":"000ab800"}]}]}


class UpstreamTests(unittest.TestCase):
    @mock.patch.object(target, "direct_bl_to_targets")
    @mock.patch.object(target, "scan_original",return_value=fake_refs())
    @mock.patch.object(target, "audit",return_value=fake_first())
    @mock.patch.object(target.hashlib, "sha256")
    def test_bounded_upstream_graph_is_only_candidate(self, h, a, s, bl):
        h.return_value.hexdigest.return_value=target.SHA
        bl.return_value={
            0x000a3be0:[{"pc":"00012300","target":"000a3be0","static_only":True}],
            0x000ab674:[]}
        with mock.patch.object(Path, "read_bytes",return_value=b"fixture"):
            result=target.one_hop(Path("synthetic.elf"))
        self.assertEqual(result["incoming_abi_downstream_calls"],2)
        self.assertEqual(result["sources_without_a32_upstream_caller"],1)
        self.assertEqual(result["total_source_to_function_a32_edges"],1)
        self.assertEqual(result["source_bound_or_nul_proven"],0)
        self.assertFalse(result["global_reachability_verified"])

    @mock.patch.object(target.hashlib, "sha256")
    def test_original_sha_mismatch_rejected(self, sha):
        sha.return_value.hexdigest.return_value="bad"
        with mock.patch.object(Path,"read_bytes",return_value=b"fixture"):
            with self.assertRaisesRegex(ValueError,"ELF changed"):
                target.one_hop(Path("wrong.elf"))


if __name__=="__main__":
    unittest.main()
