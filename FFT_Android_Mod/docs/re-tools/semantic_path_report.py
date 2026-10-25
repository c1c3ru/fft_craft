#!/usr/bin/env python3
"""Reproducible local branch contracts for priority ARM review functions."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import semantic_evidence as evidence
import semantic_facts
import semantic_paths
import semantic_cfg


def active_review_rows(results, digest, limit):
    """Guard against stale queue entries after a structural v3 promotion.

    Only same-binary, same-address auto_structural records may disappear
    from the review queue without an error. Corrupt or mismatched records
    must continue to fail the report instead of being silently omitted.
    """
    with (results / "REVIEW_QUEUE.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    selected = []
    for row in rows:
        address = row["address"].lower()
        record = json.loads((results / f"{address}.json").read_text(encoding="utf-8"))
        if (record.get("binary_sha256") != digest
                or record.get("address", "").lower() != address
                or record.get("pipeline_version") != 2
                or int(record.get("size", -1)) != int(row["size"])):
            raise ValueError(f"Invalid review checkpoint {address}")
        if record.get("status") == "auto_structural":
            continue
        if record.get("status") != "needs_review":
            raise ValueError(f"Invalid review status for {address}")
        selected.append((row, record))
        if len(selected) >= limit:
            break
    return selected


def build(binary, results, limit=12):
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    queue = active_review_rows(results, digest, limit)
    lines = [
        "# Priority ARM conditional-path contracts", "",
        f"ELF SHA-256: `{digest}`", "",
        "These are locally observed CMP/TST -> conditional branch edges; "
        "they are not dominance claims, execution traces, complete path "
        "constraints or proof of semantic equivalence.", "",
    ]
    for row, record in queue:
        address = row["address"].lower()
        title = str(row["name"]).replace("|", "/")
        lines += [f"## `{address}` — {title}", ""]
        if int(address, 16) & 1:
            lines += ["Thumb-tagged address: local ARM CMP/TST branch contract extraction "
                      "not supported; no predicate is inferred.", ""]
            continue
        instructions, tables, _ = evidence.collect(
            evidence.read_function(binary, int(address, 16), int(record["size"])),
            int(address, 16))
        guards = semantic_paths.branch_guards(instructions)
        graph, uncertain_edges = semantic_cfg.build_cfg(instructions, tables)
        effects = semantic_cfg.modeled_guard_dominance(
            semantic_cfg.effect_routes(
                semantic_paths.incoming_guard_edges(
                    semantic_facts.bitmask_effects(instructions), guards),
                guards, graph),
            guards, graph, int(address, 16))
        reachable = semantic_cfg.entry_reachable(graph, int(address, 16))
        lines += [f"Observed direct compare/branch pairs: **{len(guards)}**; "
                  f"local bitmask sequences: **{len(effects)}**.", "",
                  f"Modeled ARM CFG nodes: **{len(graph)}**; "
                  f"entry-reachable: **{len(reachable)}**; "
                  f"unmodeled outgoing edges/transfers: **{len(uncertain_edges)}**.", "",
                  "Modeled dominators are calculated only for nodes reachable "
                  "from the function entry. They do not establish dominance "
                  "across unknown incoming edges, indirect transfers, exceptions "
                  "or callees.", "",
                  "A route in this graph is a candidate, not a proven executable "
                  "path. An absent route may be due to unresolved indirect jumps, "
                  "callee effects, missing code or exceptional control flow.", ""]
        lines += ["| Compare / branch | Taken edge | Fallthrough edge |",
                  "|---|---|---|"]
        for g in guards[:30]:
            lines.append(
                f'| `0x{g["compare"]:x}` {g["compare_insn"]}; '
                f'`0x{g["branch"]:x}` {g["branch_insn"]} | '
                f'{g["taken_predicate"]} → `0x{g["taken_target"]:x}` | '
                f'{g["fallthrough_predicate"]} → `0x{g["fallthrough_target"]:x}` |')
        if not guards:
            lines.append("| No directly adjacent CMP/TST-branch pair | — | — |")
        lines.extend(["", "### Local memory-bit effects and direct incoming edges", ""])
        if not effects:
            lines += ["No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.", ""]
        for fact in effects[:20]:
            kind = "clears" if fact["kind"] == "clear_bits" else "sets"
            sites = ", ".join(f'`0x{a:x}`' for a in fact["addresses"])
            lines.append(f'- Candidate {kind} `0x{fact["mask"]:x}` at '
                         f'`{fact["memory"]}`; sequence: {sites}.')
            if fact["incoming_guard_edges"]:
                for edge in fact["incoming_guard_edges"]:
                    lines.append(
                        f'  - Direct {edge["edge"]} entry from '
                        f'`0x{edge["branch"]:x}`, following '
                        f'`0x{edge["compare"]:x}`: {edge["predicate"]}. '
                        "Other entries may exist.")
            else:
                lines.append("  - No direct CMP/TST-branch incoming edge demonstrated; "
                             "entry condition remains unknown.")
            parents = fact["modeled_predecessors"]
            if parents:
                display = ", ".join(f'`0x{a:x}` ({kind})' for a, kind in parents[:8])
                lines.append(f"  - Modeled direct predecessors: {display}.")
            else:
                lines.append("  - No decoded direct predecessor identified.")
            if not fact["reachable_from_entry"]:
                lines.append("  - Candidate write is not reachable from the "
                             "chosen function entry in this graph. No "
                             "dominance conclusion is available.")
            else:
                lines.append(
                    f'  - Entry-relative modeled dominators: '
                    f'{fact["modeled_dominator_count"]} decoded nodes '
                    "(not global or dynamic dominance).")
            dominating = fact["modeled_dominating_guards"]
            if dominating:
                lines.append(
                    "  - Conditional branches dominating this write "
                    "in the entry-rooted modeled graph:")
                for guard in dominating[:6]:
                    relation = ("Only one successor has a modeled route"
                                if guard["modeled_one_sided"] else
                                "Both successors have modeled routes")
                    lines.append(
                        f'    - `0x{guard["branch"]:x}` after '
                        f'`0x{guard["compare"]:x}`: {relation}; '
                        f'taken [{guard["taken_predicate"]}], '
                        f'other [{guard["other_predicate"]}]. '
                        "Not a proof of execution-path exclusivity.")
            else:
                lines.append("  - No conditional CMP/TST branch proven to "
                             "dominate this write even in the bounded model.")
            routes = fact["modeled_guard_routes"]
            # First report modeled single-edge candidates, then alternative
            # paths where both choices might reach the candidate write.
            routes = sorted(routes, key=lambda r: not r["modeled_exclusive"])
            for route in routes[:6]:
                taken = route["taken_path"]
                other = route["other_path"]
                fmt = lambda p: (" → ".join(f"0x{a:x}" for a in p[:7])
                                 + (" → ..." if len(p) > 7 else "") if p else
                                 "no route found in modeled graph")
                lines.append(
                    f'  - Branch `0x{route["branch"]:x}` after compare '
                    f'`0x{route["compare"]:x}`: '
                    f'[{route["taken_predicate"]}] → {fmt(taken)}; '
                    f'[{route["other_predicate"]}] → {fmt(other)}. '
                    + ("Only one modeled successor reaches the write; "
                       "NOT a dominance or impossibility proof."
                       if route["modeled_exclusive"] else
                       "Both modeled successors can reach the write."))
            if not routes:
                lines.append("  - No preceding branch guard can reach this "
                             "write in the bounded decoded graph.")
        lines.append("")
    lines.extend(["## Verification still required", "",
                  "Inspect incomplete/unmodeled CFG predecessor sets, aliasing, effects of callees "
                  "and compare behavior with execution traces before any semantic approval.", ""])
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path,
                   default=evidence.ROOT / "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--results", type=Path,
                   default=evidence.ROOT / "docs/re-results")
    p.add_argument("--limit", type=int, default=12)
    args = p.parse_args()
    if not 1 <= args.limit <= 30:
        p.error("--limit must be 1..30")
    dest = args.results / "SEMANTIC_PATH_CONTRACTS.md"
    dest.write_text(build(args.binary, args.results, args.limit), encoding="utf-8")
    print(f"Wrote {dest}")


if __name__ == "__main__":
    main()
