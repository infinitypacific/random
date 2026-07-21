#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

def clean_extension(ext):
    ext = ext.strip()
    if not ext.startswith('.'):
        ext = '.' + ext
    return ext

def rename_extensions(directory, from_exts, to_ext, dry_run=False):
    target_dir = Path(directory).resolve()

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Error: The directory '{target_dir}' does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    from_exts = [clean_extension(ext) for ext in from_exts.split(',')]
    to_ext = clean_extension(to_ext)

    print(f"Scanning: {target_dir}")
    print(f"Changing extensions: {', '.join(from_exts)} -> {to_ext}")
    if dry_run:
        print("--- DRY RUN MODE (No files will be modified) ---")
    print("-" * 50)

    count = 0
    for file_path in target_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in from_exts:
            new_file_path = file_path.with_suffix(to_ext)

            if dry_run:
                print(f"[DRY RUN] Would rename: {file_path.name} -> {new_file_path.name}")
            else:
                try:
                    file_path.rename(new_file_path)
                    print(f"Renamed: {file_path.name} -> {new_file_path.name}")
                except Exception as e:
                    print(f"Failed to rename {file_path.name}: {e}", file=sys.stderr)
            
            count += 1

    print("-" * 50)
    if count == 0:
        print("No matching files found to rename.")
    else:
        status = "would be renamed" if dry_run else "successfully renamed"
        print(f"Total files {status}: {count}")

def main():
    parser = argparse.ArgumentParser(
        description="Batch change file extensions in a specified directory."
    )
    
    parser.add_argument(
        "directory",
        help="The target directory containing the files to rename."
    )
    
    parser.add_argument(
        "--from", "-f",
        dest="from_ext",
        required=True,
        help="Comma-separated list of extensions to change (e.g., '.htm,.txt' or 'htm,txt')."
    )
    parser.add_argument(
        "--to", "-t",
        dest="to_ext",
        required=True,
        help="The new extension to apply (e.g., '.html' or 'html')."
    )

    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Preview the changes without actually renaming any files."
    )

    args = parser.parse_args()

    rename_extensions(
        directory=args.directory,
        from_exts=args.from_ext,
        to_ext=args.to_ext,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    main()