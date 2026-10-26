#!/usr/bin/env python3
"""Identify ARM checkpoint JSONs, excluding semantic snapshots and ledgers.

A structural checkpoint has an 8-digit hexadecimal address as its basename.
Never assume that every JSON file in re-results is a structural checkpoint.
"""
import argparse
import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT_NAME = re.compile(r"^[0-9a-f]{8}\.json$")


def checkpoint_paths(folder):
    return sorted(path for path in Path(folder).glob("*.json")
                  if CHECKPOINT_NAME.fullmatch(path.name))


def summarize(folder):
    paths = checkpoint_paths(folder)
    states = collections.Counter()
    for path in paths:
        record = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(record, dict) or not isinstance(record.get("status"), str):
            raise ValueError(f"invalid checkpoint metadata: {path}")
        if str(record.get("address", "")).lower().removeprefix("0x") != path.stem:
            raise ValueError(f"checkpoint address mismatch: {path}")
        states[record["status"]] += 1
    if states["error"]:
        raise ValueError("Errors in checkpoints: refusing automated merge")
    return len(paths), states


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--results", type=Path, default=ROOT / "docs/re-results")
    p.add_argument("--count", action="store_true")
    p.add_argument("--verify", action="store_true")
    args = p.parse_args()
    if args.count == args.verify:
        p.error("choose exactly one of --count or --verify")
    if args.count:
        print(len(checkpoint_paths(args.results)))
    else:
        n, statuses = summarize(args.results)
        print("Total checkpoints:", n)
        print("Status counts:", dict(statuses))


if __name__ == "__main__":
    main()
