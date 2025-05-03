#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cross-platform tracker-replacement for qBittorrent .fastresume files.
Defaults to a BT_backup folder located alongside this script.

Usage:
  python tracker_replace.py <old_tracker> <new_tracker> [--backup-dir DIR] (--dry-run | --apply)

You must specify either --dry-run (no changes) or --apply (write changes).
"""

import argparse
import re
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Replace tracker URLs in qBittorrent .fastresume files (requires --dry-run or --apply)."
    )
    parser.add_argument(
        "old_tracker",
        help="Old tracker URL/text to find",
    )
    parser.add_argument(
        "new_tracker",
        help="New tracker URL/text to replace with",
    )
    parser.add_argument(
        "--backup-dir",
        type=Path,
        default=Path(__file__).parent / "BT_backup",
        help="Directory containing .fastresume files (default: ./BT_backup next to script)",
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change, without writing",
    )
    mode_group.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes to files",
    )

    return parser.parse_args()


def scan_file(path: Path, old_b: bytes, new_b: bytes, section_re: re.Pattern, length_re: re.Pattern):
    """
    Scan a .fastresume file and return list of (old, new) tracker pairs.
    """
    data = path.read_bytes()
    if old_b not in data:
        return []

    m = section_re.search(data)
    if not m:
        return []

    blob = m.group(1)
    pos = 0
    changes = []

    while pos < len(blob):
        lm = length_re.search(blob, pos)
        if not lm:
            break
        _, num = lm.groups()
        length = int(num.decode('ascii'))
        pos = lm.end()
        tracker = blob[pos: pos + length]

        if old_b in tracker:
            old = tracker.decode('utf-8', 'ignore')
            new = tracker.replace(old_b, new_b).decode('utf-8', 'ignore')
            changes.append((old, new))

        pos += length

    return changes


def replace_file(path: Path, old_b: bytes, new_b: bytes, section_re: re.Pattern, length_re: re.Pattern):
    """Perform actual replacement and write back to file."""
    data = path.read_bytes()
    m = section_re.search(data)
    blob = m.group(1)
    pos = 0
    rebuilt = []

    while pos < len(blob):
        lm = length_re.search(blob, pos)
        if not lm:
            break
        _, num = lm.groups()
        length = int(num.decode('ascii'))
        pos = lm.end()
        tracker = blob[pos: pos + length]

        if old_b in tracker:
            tracker = tracker.replace(old_b, new_b)

        rebuilt.append(f"{len(tracker)}:".encode('ascii') + tracker)
        pos += length

    new_blob = b"el".join(rebuilt)
    new_data = data.replace(blob, new_blob, 1)
    path.write_bytes(new_data)


def main():
    args = parse_args()
    old_b = args.old_tracker.encode()
    new_b = args.new_tracker.encode()

    backup_dir: Path = args.backup_dir
    if not backup_dir.is_dir():
        sys.exit(f"Error: backup directory '{backup_dir}' not found")

    section_re = re.compile(rb"trackersll(.*?)ee\d+:", re.DOTALL)
    length_re = re.compile(rb"(el)?(\d+):")

    files = list(backup_dir.glob("*.fastresume"))
    if not files:
        sys.exit(f"No .fastresume files found in '{backup_dir}'")

    if args.dry_run:
        total = 0
        samples = []
        for f in files:
            changes = scan_file(f, old_b, new_b, section_re, length_re)
            if changes:
                total += 1
                if len(samples) < 5:
                    samples.append((f.name, changes[:3]))
        print(f"Dry-run: {total} file(s) would be modified.")
        if samples:
            print("Sample changes:")
            for fname, ch in samples:
                print(f" In {fname}:")
                for old, new in ch:
                    print(f"  {old} -> {new}")
    else:
        print(f"Applying changes in '{backup_dir}'...")
        for f in files:
            changes = scan_file(f, old_b, new_b, section_re, length_re)
            if not changes:
                print(f"Skipping {f.name}")
            else:
                print(f"Updating {f.name}...")
                replace_file(f, old_b, new_b, section_re, length_re)
                for old, new in changes[:3]:
                    print(f"  {old} -> {new}")


if __name__ == "__main__":
    main()
