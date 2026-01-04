#!/usr/bin/env python3
"""
fix-frontmatter.py - Validate and fix YAML frontmatter in markdown files.

Usage:
    python fix-frontmatter.py --scan                    # Dry run - report issues
    python fix-frontmatter.py --fix                     # Fix all issues
    python fix-frontmatter.py --scan --dir path/to/dir  # Scan specific directory
    python fix-frontmatter.py --fix --file path/to.md   # Fix single file

Required fields (per ack-src/schemas/FRONTMATTER_SCHEMA.md):
    - type: Document category from controlled vocabulary
    - description: One-line human-readable purpose
    - version: SemVer X.Y.Z
    - updated: ISO 8601 datetime
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Directories to skip
SKIP_DIRS = {
    '_archive',
    'node_modules',
    '.venv',
    'dist-info',
    '.git',
    '__pycache__',
}

# Required frontmatter fields
REQUIRED_FIELDS = ['type', 'description', 'version', 'updated']

# Default values for missing fields
DEFAULTS = {
    'type': 'guide',
    'description': 'TODO: Add description',
    'version': '0.1.0',
    'updated': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
}

# Type inference based on file path/name patterns
TYPE_PATTERNS = [
    (r'/commands/', 'command'),
    (r'/prompts/', 'prompt'),
    (r'/agents/', 'agent'),
    (r'/skills/', 'skill'),
    (r'/tools/', 'tool'),
    (r'/domains/', 'domain'),
    (r'/schemas/', 'schema'),
    (r'/rules/', 'rule'),
    (r'/templates/', 'template'),
    (r'/docs/', 'guide'),
    (r'README\.md$', 'guide'),
    (r'CLAUDE\.md$', 'memory_project'),
    (r'-intent\.md$', 'intent'),
    (r'-brief\.md$', 'project_brief'),
    (r'-architecture\.md$', 'architecture'),
    (r'-research\.md$', 'research'),
    (r'-concept\.md$', 'project_brief'),
    (r'-scope\.md$', 'project_brief'),
    (r'-validation\.md$', 'review'),
    (r'-stack\.md$', 'architecture'),
    (r'-data-model\.md$', 'data_model'),
    (r'-context-schema\.md$', 'schema'),
    (r'-dependencies\.md$', 'architecture'),
    (r'-repo-init\.md$', 'guide'),
    (r'-scaffolding\.md$', 'guide'),
]


def infer_type(filepath: str) -> str:
    """Infer document type from file path."""
    for pattern, doc_type in TYPE_PATTERNS:
        if re.search(pattern, filepath):
            return doc_type
    return DEFAULTS['type']


def infer_description(filepath: str, content: str) -> str:
    """Infer description from file path or first heading."""
    # Try to get from first H1 heading
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        # Clean up template placeholders
        title = re.sub(r'\[.*?\]', '', title).strip(' -')
        if title and len(title) > 3:
            return title

    # Fall back to filename
    name = Path(filepath).stem
    name = name.replace('-', ' ').replace('_', ' ').title()
    return name


def parse_frontmatter(content: str) -> tuple[Optional[dict], str, str]:
    """
    Parse YAML frontmatter from markdown content.

    Returns:
        (frontmatter_dict, frontmatter_raw, body)
        frontmatter_dict is None if no frontmatter found
    """
    if not content.startswith('---'):
        return None, '', content

    # Find the closing ---
    match = re.match(r'^---\n(.*?)\n---\n?(.*)$', content, re.DOTALL)
    if not match:
        return None, '', content

    frontmatter_raw = match.group(1)
    body = match.group(2)

    # Parse YAML manually (simple key: value pairs)
    frontmatter = {}
    for line in frontmatter_raw.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip().strip('"\'')
            frontmatter[key] = value

    return frontmatter, frontmatter_raw, body


def rebuild_frontmatter(original: dict, additions: dict, preserve_order: bool = True) -> str:
    """Rebuild frontmatter YAML string with additions."""
    # Merge: original + additions (additions fill gaps)
    merged = {**additions, **original}  # original takes precedence

    # Preferred field order
    order = ['type', 'stage', 'artifact', 'description', 'version', 'updated', 'status',
             'scope', 'paths', 'depends_on']

    lines = []
    added_keys = set()

    # Add fields in preferred order
    for key in order:
        if key in merged:
            value = merged[key]
            # Quote strings with spaces or special chars
            if isinstance(value, str) and (' ' in value or ':' in value or '"' in value):
                value = f'"{value}"'
            lines.append(f'{key}: {value}')
            added_keys.add(key)

    # Add remaining fields
    for key, value in merged.items():
        if key not in added_keys:
            if isinstance(value, str) and (' ' in value or ':' in value or '"' in value):
                value = f'"{value}"'
            lines.append(f'{key}: {value}')

    return '\n'.join(lines)


def check_file(filepath: str) -> dict:
    """
    Check a file for frontmatter compliance.

    Returns dict with:
        - status: 'compliant' | 'incomplete' | 'no_frontmatter' | 'error'
        - missing: list of missing required fields
        - current: current frontmatter dict (if any)
        - suggested: suggested additions
    """
    result = {
        'filepath': filepath,
        'status': 'unknown',
        'missing': [],
        'current': {},
        'suggested': {},
    }

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)
        return result

    frontmatter, _, body = parse_frontmatter(content)

    if frontmatter is None:
        result['status'] = 'no_frontmatter'
        result['missing'] = REQUIRED_FIELDS.copy()
        # Suggest all required fields
        result['suggested'] = {
            'type': infer_type(filepath),
            'description': infer_description(filepath, content),
            'version': DEFAULTS['version'],
            'updated': DEFAULTS['updated'],
        }
        return result

    result['current'] = frontmatter

    # Check for missing required fields
    for field in REQUIRED_FIELDS:
        if field not in frontmatter or not frontmatter[field]:
            result['missing'].append(field)
            # Suggest value
            if field == 'type':
                result['suggested'][field] = infer_type(filepath)
            elif field == 'description':
                result['suggested'][field] = infer_description(filepath, body)
            elif field == 'version':
                result['suggested'][field] = DEFAULTS['version']
            elif field == 'updated':
                result['suggested'][field] = DEFAULTS['updated']

    if result['missing']:
        result['status'] = 'incomplete'
    else:
        result['status'] = 'compliant'

    return result


def fix_file(filepath: str, dry_run: bool = False) -> dict:
    """
    Fix frontmatter in a file.

    Returns check result with additional 'fixed' field.
    """
    result = check_file(filepath)
    result['fixed'] = False

    if result['status'] == 'compliant':
        return result

    if result['status'] == 'error':
        return result

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        result['error'] = str(e)
        return result

    frontmatter, frontmatter_raw, body = parse_frontmatter(content)

    if result['status'] == 'no_frontmatter':
        # Add new frontmatter
        new_fm = rebuild_frontmatter({}, result['suggested'])
        new_content = f'---\n{new_fm}\n---\n\n{content}'
    else:
        # Update existing frontmatter
        new_fm = rebuild_frontmatter(frontmatter, result['suggested'])
        new_content = f'---\n{new_fm}\n---\n{body}'

    if not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        result['fixed'] = True

    return result


def find_markdown_files(root_dir: str) -> list[str]:
    """Find all markdown files, excluding skip directories."""
    files = []
    root = Path(root_dir)

    for path in root.rglob('*.md'):
        # Check if any parent is in skip list
        skip = False
        for part in path.parts:
            if part in SKIP_DIRS:
                skip = True
                break
        if not skip:
            files.append(str(path))

    return sorted(files)


def print_report(results: list[dict], verbose: bool = False):
    """Print a summary report of results."""
    compliant = [r for r in results if r['status'] == 'compliant']
    incomplete = [r for r in results if r['status'] == 'incomplete']
    no_fm = [r for r in results if r['status'] == 'no_frontmatter']
    errors = [r for r in results if r['status'] == 'error']
    fixed = [r for r in results if r.get('fixed')]

    print("\n" + "=" * 60)
    print("FRONTMATTER COMPLIANCE REPORT")
    print("=" * 60)
    print(f"\nTotal files scanned: {len(results)}")
    print(f"  Compliant:       {len(compliant)}")
    print(f"  Incomplete:      {len(incomplete)}")
    print(f"  No frontmatter:  {len(no_fm)}")
    print(f"  Errors:          {len(errors)}")
    if fixed:
        print(f"  Fixed:           {len(fixed)}")

    if incomplete or no_fm:
        print("\n" + "-" * 60)
        print("FILES NEEDING ATTENTION")
        print("-" * 60)

        for r in incomplete + no_fm:
            rel_path = r['filepath']
            if rel_path.startswith(os.getcwd()):
                rel_path = rel_path[len(os.getcwd())+1:]

            status_icon = "!" if r['status'] == 'incomplete' else "+"
            print(f"\n[{status_icon}] {rel_path}")
            print(f"    Status: {r['status']}")
            if r['missing']:
                print(f"    Missing: {', '.join(r['missing'])}")
            if verbose and r['suggested']:
                print(f"    Suggested:")
                for k, v in r['suggested'].items():
                    print(f"      {k}: {v}")

    if errors:
        print("\n" + "-" * 60)
        print("ERRORS")
        print("-" * 60)
        for r in errors:
            print(f"  {r['filepath']}: {r.get('error', 'Unknown error')}")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description='Validate and fix YAML frontmatter in markdown files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--scan', action='store_true',
                       help='Scan and report issues (dry run)')
    group.add_argument('--fix', action='store_true',
                       help='Fix issues in files')

    parser.add_argument('--dir', type=str, default='.',
                        help='Directory to scan (default: current directory)')
    parser.add_argument('--file', type=str,
                        help='Single file to process')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed suggestions')

    args = parser.parse_args()

    # Determine files to process
    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        files = [args.file]
    else:
        files = find_markdown_files(args.dir)

    if not files:
        print("No markdown files found.")
        sys.exit(0)

    print(f"Processing {len(files)} markdown files...")

    # Process files
    results = []
    for filepath in files:
        if args.fix:
            result = fix_file(filepath, dry_run=False)
        else:
            result = check_file(filepath)
        results.append(result)

        # Progress indicator for large batches
        if len(files) > 20 and len(results) % 20 == 0:
            print(f"  Processed {len(results)}/{len(files)}...")

    # Print report
    print_report(results, verbose=args.verbose)

    # Exit code
    issues = [r for r in results if r['status'] in ('incomplete', 'no_frontmatter', 'error')]
    if args.scan and issues:
        sys.exit(1)  # Non-zero exit if issues found in scan mode

    sys.exit(0)


if __name__ == '__main__':
    main()
