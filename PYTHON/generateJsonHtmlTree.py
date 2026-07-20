import json
import argparse
from html.parser import HTMLParser
from pathlib import Path

class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title and self.title is None:
            self.title = data.strip()


def get_html_title(file_path: Path) -> str:
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        parser = TitleParser()
        parser.feed(content)
        if parser.title:
            return parser.title
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
    
    #fallback
    return file_path.stem


def scan_directory(current_dir: Path, root_dir: Path) -> list:
    items = []
    
    for entry in sorted(current_dir.iterdir(), key=lambda e: (e.is_file(), e.name.lower())):
        if entry.is_file() and entry.suffix.lower() in [".html", ".htm"]:
            rel_path = entry.relative_to(root_dir).as_posix()
            items.append({
                "title": get_html_title(entry),
                "path": rel_path
            })

        elif entry.is_dir():
            #recursive search
            sub_items = scan_directory(entry, root_dir)

            if not sub_items:
                continue

            #flattening
            if len(sub_items) == 1:
                items.append(sub_items[0])
            else:
                items.append({
                    "directory": entry.name,
                    "items": sub_items
                })

    return items


def generate_json_tree(target_directory: str, output_json_path: str):
    root_dir = Path(target_directory).resolve()

    if not root_dir.exists() or not root_dir.is_dir():
        print(f"Error: The directory '{target_directory}' does not exist.")
        return

    print(f"Scanning '{root_dir}'...")
    tree_data = scan_directory(root_dir, root_dir)

    output_path = Path(output_json_path)
    output_path.write_text(json.dumps(tree_data), encoding="utf-8")
    print(f"Success! JSON tree saved to '{output_path.resolve()}'")


def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory of HTML/HTM files and generate a JSON site structure."
    )
    
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="The target directory to scan (defaults to current directory '.')."
    )
	
    parser.add_argument(
        "-o", "--output",
        default="site_structure.json",
        help="The file path for the output JSON (defaults to 'site_structure.json')."
    )

    args = parser.parse_args()
    generate_json_tree(args.directory, args.output)


if __name__ == "__main__":
    main()