#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

def prefix_selectors(css_content: str, prefix: str, root_selectors: list, chain_selectors: list, ignore_selectors: list, asterisk_handling: bool) -> str:
    prefix = prefix.strip()
    
    #Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    
    in_keyframes = False

    def replace_selector(match):
        nonlocal in_keyframes
        selector_group = match.group(1)
        cleaned_group = selector_group.strip()
        
        #Handle keyframe blocks (with @-webkit etc...)
        if cleaned_group.startswith('@keyframes') or cleaned_group.startswith('@-'):
            in_keyframes = True
            return match.group(0)
        
        if cleaned_group.startswith('@'):
            return match.group(0)
            
        if asterisk_handling:
            root_selectors.append('*')

        #No prefix on (from, to, 0%, 100%, etc)
        if in_keyframes:
            if re.match(r'^(from|to|\d+%)$', cleaned_group):
                return match.group(0)
            else:
                in_keyframes = False

        selectors = selector_group.split(',')
        prefixed_selectors = []
        
        for sel in selectors:
            cleaned_sel = sel.strip()
            if not cleaned_sel:
                continue
                
            is_ignored = False
            for ign_sel in ignore_selectors:
                if cleaned_sel == ign_sel or cleaned_sel.startswith(ign_sel):
                    prefixed_selectors.append(cleaned_sel)
                    is_ignored = True
                    break
            if is_ignored:
                continue
            
            is_root = False
            for root_sel in root_selectors:
                if (cleaned_sel == root_sel or 
                    cleaned_sel.startswith(root_sel + " ") or 
                    cleaned_sel.startswith(root_sel + ".") or 
                    cleaned_sel.startswith(root_sel + ":") or 
                    cleaned_sel.startswith(root_sel + "[") or 
                    cleaned_sel.startswith(root_sel + "#")):
                    
                    remainder = cleaned_sel[len(root_sel):]
                    if asterisk_handling and root_sel == '*':
                        prefixed_selectors.append(f"{prefix}:where(*){remainder}")
                    else:
                        prefixed_selectors.append(f"{prefix}{remainder}")
                    
                    is_root = True
                    break
            if is_root:
                continue
            
            is_chained = False
            for chain_sel in chain_selectors:
                if cleaned_sel.startswith(chain_sel):
                    prefixed_selectors.append(f"{prefix}{cleaned_sel}")
                    is_chained = True
                    break
            if is_chained:
                continue
            
            prefixed_selectors.append(f"{prefix} {cleaned_sel}")
                
        return ", ".join(prefixed_selectors) + " {"

    #(everything before \s*{ that's not in {})
    pattern = re.compile(r'([^{}]+)\s*\{')
    
    return pattern.sub(replace_selector, css_content)

def parse_list_arg(arg_list):
    result = []
    for item in arg_list:
        for sel in item.split(','):
            cleaned = sel.strip()
            if cleaned:
                result.append(cleaned)
    return result

def main():
    parser = argparse.ArgumentParser(
        description="Isolate CSS by prepending a custom selector to all existing rules."
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to the input CSS file"
    )
    parser.add_argument(
        "-p", "--prefix",
        type=str,
        required=True,
        help="The selector prefix to add (e.g., '.my-widget' or '#isolated-view')"
    )
    parser.add_argument(
        "-r", "--root-selectors",
        type=str,
        nargs="+",
        default=["body", "html", ":root"],
        help="Selectors to treat as root elements (replaced by the prefix instead of prepended). "
             "Accepts space-separated or comma-separated values. Defaults to: body html :root"
    )
    parser.add_argument(
        "-a", "--asterisk-handling",
        action="store_true",
        help="Handle asterisks with :where(*)"
    )
    parser.add_argument(
        "-c", "--chain-selectors",
        type=str,
        nargs="+",
        default=["::", ":host"],
        help="Selectors starting with these strings will be chained directly to the prefix "
             "WITHOUT a space. Defaults to: :: :host"
    )
    parser.add_argument(
        "-g", "--ignore-selectors",
        type=str,
        nargs="+",
        default=[],
        help="Selectors starting with these strings will be left untouched (kept global)."
    )

    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "-o", "--output",
        type=Path,
        help="Path to save the output CSS file (defaults to stdout if -i is not set)",
        default=None
    )
    output_group.add_argument(
        "-i", "--in-place",
        action="store_true",
        help="Overwrite the input file directly with the isolated CSS"
    )

    args = parser.parse_args()

    #cleanup list arguments
    root_selectors = parse_list_arg(args.root_selectors)
    chain_selectors = parse_list_arg(args.chain_selectors)
    ignore_selectors = parse_list_arg(args.ignore_selectors)

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find file '{args.input_file}'", file=sys.stderr)
        sys.exit(1)

    isolated_css = prefix_selectors(css_content, args.prefix, root_selectors, chain_selectors, ignore_selectors, args.asterisk_handling)

    #Write to file
    if args.in_place:
        with open(args.input_file, 'w', encoding='utf-8') as f:
            f.write(isolated_css)
        print(f"Success! Overwrote '{args.input_file}' in-place.")
    elif args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(isolated_css)
        print(f"Success! Isolated CSS written to '{args.output}'.")
    else:
        print(isolated_css)

if __name__ == "__main__":
    main()