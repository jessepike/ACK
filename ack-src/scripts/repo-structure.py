#!/usr/bin/env python3
"""
Repository Structure Checker

Validates file placement against the canonical structure defined in
.claude/rules/repo-structure.md. Outputs JSON report for use by /repo-check skill.

Usage:
    python repo-structure.py [--dir PATH] [--json] [--verbose]

Options:
    --dir PATH    Directory to check (default: current directory)
    --json        Output JSON report (default: human-readable)
    --verbose     Show all files, not just violations
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Default allowed files at root
ALLOWED_ROOT_FILES = {
    # Required
    "README.md",
    "intent.md",
    "brief.md",
    # Optional config
    "LICENSE",
    ".gitignore",
    ".gitattributes",
    "package.json",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    "setup.cfg",
    "Makefile",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    ".dockerignore",
    "tsconfig.json",
    "jest.config.js",
    "jest.config.ts",
    ".eslintrc.js",
    ".eslintrc.json",
    ".prettierrc",
    ".prettierrc.json",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
}

# Known directories and their purposes
KNOWN_DIRECTORIES = {
    "docs": "Documentation",
    "docs/discover": "Problem validation artifacts",
    "docs/design": "Technical specification",
    "docs/setup": "Implementation planning",
    "docs/develop": "Runtime artifacts",
    "docs/guides": "User-facing documentation",
    "src": "Source code",
    "tests": "Test files",
    "scripts": "Automation scripts",
    "inbox": "Incoming files for review",
    "tmp": "Temporary files",
    "_archive": "Archived work",
    ".claude": "Claude Code configuration",
    ".claude/commands": "Slash command skills",
    ".claude/rules": "Behavioral rules",
    ".claude/logs": "Maintenance logs",
}

# Directories to ignore
IGNORE_DIRS = {
    ".git",
    ".github",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
    ".next",
    ".nuxt",
    "coverage",
    ".DS_Store",
}

# File patterns for source code
SOURCE_CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".rb",
    ".java", ".kt", ".swift", ".c", ".cpp", ".h", ".hpp",
}


def load_settings(base_dir: Path) -> dict:
    """Load project-specific settings from .claude/settings.yaml if it exists."""
    settings_path = base_dir / ".claude" / "settings.yaml"
    if settings_path.exists():
        try:
            import yaml
            with open(settings_path) as f:
                return yaml.safe_load(f) or {}
        except ImportError:
            # YAML not available, use defaults
            pass
        except Exception:
            pass
    return {}


def get_allowed_root_files(settings: dict) -> set:
    """Get allowed root files including any project-specific additions."""
    allowed = ALLOWED_ROOT_FILES.copy()
    if "repo_structure" in settings:
        additional = settings["repo_structure"].get("allowed_root", [])
        allowed.update(additional)
    return allowed


def get_ignore_dirs(settings: dict) -> set:
    """Get directories to ignore including any project-specific additions."""
    ignore = IGNORE_DIRS.copy()
    if "repo_structure" in settings:
        additional = settings["repo_structure"].get("ignore", [])
        ignore.update(d.rstrip("/") for d in additional)
    return ignore


def classify_file(filepath: Path, base_dir: Path, settings: dict) -> dict:
    """Classify a file and determine if it's in the right location."""
    rel_path = filepath.relative_to(base_dir)
    parts = rel_path.parts
    filename = filepath.name
    extension = filepath.suffix.lower()

    result = {
        "path": str(rel_path),
        "filename": filename,
        "current_location": str(rel_path.parent) if len(parts) > 1 else "/",
        "severity": None,
        "violation": None,
        "suggestion": None,
    }

    # Check if at root
    if len(parts) == 1:
        allowed = get_allowed_root_files(settings)
        if filename in allowed:
            result["status"] = "valid"
            return result

        # Source code at root is an error
        if extension in SOURCE_CODE_EXTENSIONS:
            result["severity"] = "error"
            result["violation"] = "Source code file at root"
            result["suggestion"] = f"Move to src/{filename}"
            return result

        # Markdown files at root (not allowed ones)
        if extension == ".md":
            result["severity"] = "error"
            result["violation"] = "Markdown file at root (not in allowed list)"
            result["suggestion"] = f"Move to docs/ or inbox/{filename}"
            return result

        # Other files at root
        result["severity"] = "error"
        result["violation"] = "Unknown file at root"
        result["suggestion"] = f"Move to appropriate directory or inbox/{filename}"
        return result

    # Check if in known directory
    first_dir = parts[0]

    # Check for files in ignored directories
    ignore = get_ignore_dirs(settings)
    if first_dir in ignore or first_dir.startswith(".") and first_dir not in {".claude"}:
        result["status"] = "ignored"
        return result

    # Check known directories
    if first_dir in KNOWN_DIRECTORIES or str(rel_path.parent) in KNOWN_DIRECTORIES:
        result["status"] = "valid"

        # Additional checks for specific directories
        if first_dir == "docs" and len(parts) >= 2:
            second_dir = parts[1]
            valid_doc_dirs = {"discover", "design", "setup", "develop", "guides"}
            if second_dir not in valid_doc_dirs:
                result["severity"] = "warning"
                result["violation"] = f"Unknown docs subdirectory: {second_dir}"
                result["suggestion"] = f"Move to docs/{{discover|design|setup|develop|guides}}/"

        return result

    # Unknown directory
    result["severity"] = "warning"
    result["violation"] = f"File in unknown directory: {first_dir}"
    result["suggestion"] = f"Move to known directory or add {first_dir}/ to settings"
    return result


def scan_directory(base_dir: Path, settings: dict, verbose: bool = False) -> dict:
    """Scan a directory and return a report of all files."""
    results = {
        "scan_time": datetime.now().isoformat(),
        "base_dir": str(base_dir),
        "summary": {
            "total_files": 0,
            "valid": 0,
            "errors": 0,
            "warnings": 0,
            "ignored": 0,
        },
        "violations": [],
        "files": [] if verbose else None,
    }

    ignore = get_ignore_dirs(settings)

    for root, dirs, files in os.walk(base_dir):
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if d not in ignore and not (d.startswith(".") and d not in {".claude"})]

        for filename in files:
            # Skip hidden files except in .claude
            if filename.startswith(".") and not root.endswith(".claude"):
                continue

            filepath = Path(root) / filename
            classification = classify_file(filepath, base_dir, settings)

            results["summary"]["total_files"] += 1

            if classification.get("status") == "valid":
                results["summary"]["valid"] += 1
            elif classification.get("status") == "ignored":
                results["summary"]["ignored"] += 1
            elif classification.get("severity") == "error":
                results["summary"]["errors"] += 1
                results["violations"].append(classification)
            elif classification.get("severity") == "warning":
                results["summary"]["warnings"] += 1
                results["violations"].append(classification)

            if verbose and results["files"] is not None:
                results["files"].append(classification)

    return results


def print_human_report(results: dict) -> None:
    """Print a human-readable report."""
    print("\n" + "=" * 60)
    print("Repository Structure Report")
    print("=" * 60)
    print(f"Scanned: {results['base_dir']}")
    print(f"Time: {results['scan_time']}")
    print("-" * 60)

    summary = results["summary"]
    print(f"Total files: {summary['total_files']}")
    print(f"  Valid: {summary['valid']}")
    print(f"  Errors: {summary['errors']}")
    print(f"  Warnings: {summary['warnings']}")
    print(f"  Ignored: {summary['ignored']}")

    if results["violations"]:
        print("\n" + "-" * 60)
        print("VIOLATIONS:")
        print("-" * 60)

        errors = [v for v in results["violations"] if v["severity"] == "error"]
        warnings = [v for v in results["violations"] if v["severity"] == "warning"]

        if errors:
            print("\nERRORS (must fix):")
            for v in errors:
                print(f"  • {v['path']}")
                print(f"    {v['violation']}")
                print(f"    → {v['suggestion']}")

        if warnings:
            print("\nWARNINGS (should fix):")
            for v in warnings:
                print(f"  • {v['path']}")
                print(f"    {v['violation']}")
                print(f"    → {v['suggestion']}")
    else:
        print("\n✓ No violations found!")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Check repository structure")
    parser.add_argument("--dir", type=str, default=".", help="Directory to check")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    parser.add_argument("--verbose", action="store_true", help="Show all files")
    args = parser.parse_args()

    base_dir = Path(args.dir).resolve()

    if not base_dir.exists():
        print(f"Error: Directory not found: {base_dir}", file=sys.stderr)
        sys.exit(1)

    settings = load_settings(base_dir)
    results = scan_directory(base_dir, settings, args.verbose)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_human_report(results)

    # Exit with error code if there are errors
    if results["summary"]["errors"] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
