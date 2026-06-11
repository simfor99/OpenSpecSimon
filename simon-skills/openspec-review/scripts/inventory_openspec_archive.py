#!/usr/bin/env python3
"""Inventory one OpenSpec change or archived change."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from openspec_review_lib import inventory_for_change, is_change_dir, json_dump


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("change_dir", help="OpenSpec change directory")
    args = parser.parse_args()

    change_dir = Path(args.change_dir).expanduser()
    if not change_dir.exists():
        print(json_dump({"ok": False, "error": f"not found: {change_dir}"}))
        return 2
    if not is_change_dir(change_dir):
        print(json_dump({"ok": False, "error": f"not an OpenSpec change directory: {change_dir}"}))
        return 2

    data = inventory_for_change(change_dir)
    data["ok"] = True
    print(json_dump(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
