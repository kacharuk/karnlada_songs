#!/usr/bin/env python3
"""
Copy all files from a source directory (default: ./output/mp3)
to a target directory (default: docs/audio/เพลงเดี่ยว).
If a filename collision occurs, append a numeric suffix before
the file extension, incrementing until a unique name is found.
Print failures and a summary at the end.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from typing import List, Tuple


def unique_filename(dest_dir: str, filename: str) -> str:
    base, ext = os.path.splitext(filename)
    candidate = filename
    i = 1
    while os.path.exists(os.path.join(dest_dir, candidate)):
        candidate = f"{base} ({i}){ext}"
        i += 1
    return candidate


def gather_source_files(src_dir: str) -> List[str]:
    files: List[str] = []
    for root, _dirs, filenames in os.walk(src_dir):
        for fn in filenames:
            files.append(os.path.join(root, fn))
    return files


def copy_all(src_dir: str, dest_dir: str, dry_run: bool = False) -> Tuple[int, int, int, List[Tuple[str, str]]]:
    os.makedirs(dest_dir, exist_ok=True)
    src_files = gather_source_files(src_dir)
    total = len(src_files)
    copied = 0
    collisions = 0
    failures: List[Tuple[str, str]] = []

    for src_path in src_files:
        filename = os.path.basename(src_path)
        dest_name = filename
        dest_path = os.path.join(dest_dir, dest_name)
        if os.path.exists(dest_path):
            dest_name = unique_filename(dest_dir, dest_name)
            dest_path = os.path.join(dest_dir, dest_name)
            collisions += 1

        try:
            if dry_run:
                print(f"DRY RUN: {src_path} -> {dest_path}")
            else:
                shutil.copy2(src_path, dest_path)
            copied += 1
        except Exception as e:
            failures.append((src_path, str(e)))
            print(f"Failed to copy: {src_path} -> {dest_path} : {e}")

    return total, copied, collisions, failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Copy MP3 files into a target folder with collision suffixing")
    parser.add_argument("--source", "-s", default=os.path.join("output", "mp3"), help="Source directory (default: output/mp3)")
    parser.add_argument("--target", "-t", default=os.path.join("docs", "audio", "เพลงเดี่ยว"), help="Target directory (default: docs/audio/เพลงเดี่ยว)")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without copying")

    args = parser.parse_args()
    src = args.source
    tgt = args.target

    if not os.path.isdir(src):
        print(f"Source directory not found: {src}")
        return 2

    print(f"Copying files from {src} to {tgt}")
    total, copied, collisions, failures = copy_all(src, tgt, dry_run=args.dry_run)

    print("\nSummary")
    print("-------")
    print(f"Total files found: {total}")
    print(f"Files copied: {copied}")
    print(f"Name collisions resolved: {collisions}")
    print(f"Failures: {len(failures)}")

    if failures:
        print("\nFailed copies:")
        for path, err in failures:
            print(f" - {path} : {err}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
