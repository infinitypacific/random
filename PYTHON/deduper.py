import os
import hashlib
import argparse
from pathlib import Path

def get_file_hash(file_path):
    hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash.update(chunk)
        return hash_sha256.hexdigest()
    except (PermissionError, OSError):
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Delete duplicate files in a directory tree! :D"
    )
    parser.add_argument(
        "path", 
        type=str, 
        help="The target directory to scan for duplicates!"
    )
    parser.add_argument(
        "-d", "--delete", 
        action="store_true", 
        help="Completely delete the duplicate files. If not set, the script performs a dry run."
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Log all files being scanned, not just duplicates."
    )

    args = parser.parse_args()
    target_dir = Path(args.path)

    if not target_dir.is_dir():
        print(f"[ERROR] {args.path} is not a valid directory.")
        return

    if not args.delete:
        print("--- [DRY RUN] No files will be deleted. Use --delete to confirm. ---\n")

    hashes_found = {}
    duplicates_count = 0

    for subdir, _, files in os.walk(target_dir):
        subdir_path = Path(subdir);
        for filename in files:
            file_path = subdir_path / filename
            
            if file_path.is_symlink():
                continue

            if args.verbose:
                print(f"[SCANNING] {file_path}")

            file_hash = get_file_hash(file_path)
            if file_hash is None:
                continue

            if file_hash in hashes_found:
                print(f"[DUPLICATE] {file_path}")
                print(f"\t\tOriginal: {hashes_found[file_hash]}")
                
                if args.delete:
                    try:
                        os.remove(file_path)
                        print("\t\t[ACTION] Deleted.")
                    except Exception as e:
                        print(f"\t\t[ERROR] {e}")
                else:
                    print("\t\t[ACTION] Not deleted.")
                
                duplicates_count += 1
            else:
                hashes_found[file_hash] = file_path

    print(f"\n--- [DEDUPE SUCCESS] ---")
    print(f"Found {duplicates_count} duplicate files.")

if __name__ == "__main__":
    main()