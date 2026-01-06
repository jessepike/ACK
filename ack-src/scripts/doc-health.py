#!/usr/bin/env python3
"""
Documentation Health Checker

Validates documentation files for:
- YAML frontmatter compliance
- Required sections per doc type
- Internal link verification
- Staleness detection

Outputs JSON report for use by /doc-check skill.

Usage:
    python doc-health.py [--dir PATH] [--json] [--category CATEGORY] [--verbose]

Options:
    --dir PATH          Directory to check (default: current directory)
    --json              Output JSON report (default: human-readable)
    --category CAT      Filter by category: tech, product, user, all (default: all)
    --staleness DAYS    Days before marking as stale (default: 14)
    --verbose           Show all docs, not just issues
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

# Required frontmatter fields
REQUIRED_FRONTMATTER = ["type", "description", "version", "updated"]

# Valid types from FRONTMATTER_SCHEMA.md
VALID_TYPES = {
    # Core artifacts
    "intent", "project_brief", "architecture", "data_model", "schema", "plan", "tasks",
    # Memory
    "memory_global", "memory_project",
    # Rules
    "rule_constitution", "rule_preferences", "rule_workflows",
    "rule_architecture", "rule_stack", "rule_domain",
    # Supporting
    "adr", "research", "review", "guide", "command", "stage_guide",
    # Governance
    "artifact_registry",
}

# Document categories and their locations
DOC_CATEGORIES = {
    "tech": {
        "paths": ["docs/design/"],
        "types": ["architecture", "data_model", "stack", "schema", "adr"],
        "source_of_truth": ["src/", "schema/"],
    },
    "product": {
        "paths": ["docs/discover/", "docs/setup/"],
        "types": ["project_brief", "plan", "tasks", "research", "intent"],
        "source_of_truth": None,  # Human-driven, no code comparison
    },
    "user": {
        "paths": ["docs/guides/"],
        "types": ["guide"],
        "source_of_truth": ["src/cli/", "src/api/"],
    },
}

# Required sections per doc type
REQUIRED_SECTIONS = {
    "architecture": ["## Overview", "## Components", "## Data Flow"],
    "data_model": ["## Entities", "## Relationships"],
    "plan": ["## Phases", "## Milestones"],
    "tasks": ["## Tasks"],
    "guide": ["## Overview"],
    "project_brief": ["## Problem", "## Solution"],
}

# Default staleness thresholds (days)
DEFAULT_STALENESS = {
    "tech": 7,
    "product": 30,
    "user": 14,
}


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}, content

    try:
        end_match = re.search(r'\n---\s*\n', content[3:])
        if not end_match:
            return {}, content

        yaml_content = content[3:end_match.start() + 3]
        body = content[end_match.end() + 3:]

        # Simple YAML parsing without external dependency
        frontmatter = {}
        for line in yaml_content.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                frontmatter[key] = value

        return frontmatter, body
    except Exception:
        return {}, content


def check_frontmatter(frontmatter: dict) -> list[dict]:
    """Check frontmatter for compliance issues."""
    issues = []

    # Check required fields
    for field in REQUIRED_FRONTMATTER:
        if field not in frontmatter:
            issues.append({
                "type": "missing_field",
                "field": field,
                "severity": "error",
                "message": f"Missing required frontmatter field: {field}",
            })

    # Check type is valid
    if "type" in frontmatter:
        doc_type = frontmatter["type"]
        if doc_type not in VALID_TYPES:
            issues.append({
                "type": "invalid_type",
                "field": "type",
                "severity": "warning",
                "message": f"Unknown document type: {doc_type}",
            })

    # Check version format (semver)
    if "version" in frontmatter:
        version = frontmatter["version"]
        if not re.match(r'^\d+\.\d+\.\d+$', version):
            issues.append({
                "type": "invalid_version",
                "field": "version",
                "severity": "warning",
                "message": f"Version not in semver format: {version}",
            })

    # Check updated is valid ISO 8601
    if "updated" in frontmatter:
        updated = frontmatter["updated"]
        try:
            # Try parsing various ISO 8601 formats
            if "T" in updated:
                datetime.fromisoformat(updated.replace("Z", "+00:00"))
            else:
                datetime.strptime(updated, "%Y-%m-%d")
        except ValueError:
            issues.append({
                "type": "invalid_date",
                "field": "updated",
                "severity": "warning",
                "message": f"Updated not in ISO 8601 format: {updated}",
            })

    return issues


def check_sections(body: str, doc_type: str) -> list[dict]:
    """Check for required sections based on doc type."""
    issues = []

    required = REQUIRED_SECTIONS.get(doc_type, [])
    for section in required:
        # Case-insensitive search for section header
        pattern = re.escape(section).replace(r"\ ", r"\s+")
        if not re.search(pattern, body, re.IGNORECASE):
            issues.append({
                "type": "missing_section",
                "section": section,
                "severity": "warning",
                "message": f"Missing required section: {section}",
            })

    return issues


def check_links(body: str, base_dir: Path, doc_path: Path) -> list[dict]:
    """Check internal links for broken references."""
    issues = []

    # Find markdown links: [text](path)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    for match in re.finditer(link_pattern, body):
        link_text, link_path = match.groups()

        # Skip external links and anchors
        if link_path.startswith(("http://", "https://", "#", "mailto:")):
            continue

        # Resolve relative path
        if link_path.startswith("/"):
            target = base_dir / link_path[1:]
        else:
            target = doc_path.parent / link_path

        # Remove anchor if present
        target_str = str(target).split("#")[0]
        target = Path(target_str)

        if not target.exists():
            issues.append({
                "type": "broken_link",
                "link": link_path,
                "severity": "warning",
                "message": f"Broken link: {link_path}",
            })

    return issues


def check_staleness(
    frontmatter: dict,
    file_path: Path,
    base_dir: Path,
    category: str,
    threshold_days: int
) -> list[dict]:
    """Check if document is stale based on last update."""
    issues = []

    # Get updated date from frontmatter
    updated_str = frontmatter.get("updated", "")
    if not updated_str:
        issues.append({
            "type": "staleness",
            "severity": "warning",
            "message": "No 'updated' date in frontmatter, cannot check staleness",
        })
        return issues

    try:
        if "T" in updated_str:
            updated = datetime.fromisoformat(updated_str.replace("Z", "+00:00"))
            if updated.tzinfo:
                updated = updated.replace(tzinfo=None)
        else:
            updated = datetime.strptime(updated_str, "%Y-%m-%d")
    except ValueError:
        return issues  # Already flagged in frontmatter check

    # Check age
    age = datetime.now() - updated
    if age.days > threshold_days:
        issues.append({
            "type": "staleness",
            "severity": "info",
            "message": f"Document is {age.days} days old (threshold: {threshold_days})",
            "days_old": age.days,
        })

    # For tech/user docs, check if source files are newer
    cat_config = DOC_CATEGORIES.get(category, {})
    source_paths = cat_config.get("source_of_truth", [])

    if source_paths:
        for src_path in source_paths:
            src_dir = base_dir / src_path.rstrip("/")
            if src_dir.exists():
                # Find most recently modified file in source
                newest_src = None
                for root, _, files in os.walk(src_dir):
                    for f in files:
                        fp = Path(root) / f
                        mtime = datetime.fromtimestamp(fp.stat().st_mtime)
                        if newest_src is None or mtime > newest_src:
                            newest_src = mtime

                if newest_src and newest_src > updated:
                    issues.append({
                        "type": "source_newer",
                        "severity": "warning",
                        "message": f"Source files in {src_path} modified after last doc update",
                        "source_path": src_path,
                    })

    return issues


def determine_category(file_path: Path, base_dir: Path) -> Optional[str]:
    """Determine which category a doc belongs to based on path."""
    rel_path = str(file_path.relative_to(base_dir))

    for category, config in DOC_CATEGORIES.items():
        for path_prefix in config["paths"]:
            if rel_path.startswith(path_prefix):
                return category

    return None


def scan_document(
    file_path: Path,
    base_dir: Path,
    staleness_thresholds: dict,
    verbose: bool = False
) -> dict:
    """Scan a single document and return its health status."""
    rel_path = file_path.relative_to(base_dir)
    category = determine_category(file_path, base_dir)

    result = {
        "path": str(rel_path),
        "category": category,
        "frontmatter": None,
        "issues": [],
        "status": "valid",
    }

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        result["status"] = "error"
        result["issues"].append({
            "type": "read_error",
            "severity": "error",
            "message": f"Could not read file: {e}",
        })
        return result

    # Parse frontmatter
    frontmatter, body = parse_frontmatter(content)
    result["frontmatter"] = frontmatter

    # Check frontmatter
    result["issues"].extend(check_frontmatter(frontmatter))

    # Check sections if we know the type
    doc_type = frontmatter.get("type", "")
    if doc_type:
        result["issues"].extend(check_sections(body, doc_type))

    # Check internal links
    result["issues"].extend(check_links(body, base_dir, file_path))

    # Check staleness
    if category:
        threshold = staleness_thresholds.get(category, 14)
        result["issues"].extend(
            check_staleness(frontmatter, file_path, base_dir, category, threshold)
        )

    # Determine overall status
    severities = [i["severity"] for i in result["issues"]]
    if "error" in severities:
        result["status"] = "error"
    elif "warning" in severities:
        result["status"] = "warning"
    elif "info" in severities:
        result["status"] = "info"

    return result


def scan_directory(
    base_dir: Path,
    category_filter: str,
    staleness_thresholds: dict,
    verbose: bool = False
) -> dict:
    """Scan all documentation files in a directory."""
    results = {
        "scan_time": datetime.now().isoformat(),
        "base_dir": str(base_dir),
        "summary": {
            "total_docs": 0,
            "valid": 0,
            "errors": 0,
            "warnings": 0,
            "info": 0,
        },
        "documents": [],
    }

    # Determine which paths to scan
    if category_filter == "all":
        scan_paths = []
        for cat_config in DOC_CATEGORIES.values():
            scan_paths.extend(cat_config["paths"])
    else:
        cat_config = DOC_CATEGORIES.get(category_filter, {})
        scan_paths = cat_config.get("paths", [])

    # Also check root for intent.md and brief.md
    root_docs = ["intent.md", "brief.md"]
    for doc in root_docs:
        doc_path = base_dir / doc
        if doc_path.exists():
            scan_result = scan_document(doc_path, base_dir, staleness_thresholds, verbose)
            scan_result["category"] = "product"  # Root docs are product docs
            results["documents"].append(scan_result)
            results["summary"]["total_docs"] += 1

            if scan_result["status"] == "valid":
                results["summary"]["valid"] += 1
            elif scan_result["status"] == "error":
                results["summary"]["errors"] += 1
            elif scan_result["status"] == "warning":
                results["summary"]["warnings"] += 1
            elif scan_result["status"] == "info":
                results["summary"]["info"] += 1

    # Scan category directories
    for scan_path in scan_paths:
        full_path = base_dir / scan_path
        if not full_path.exists():
            continue

        for root, _, files in os.walk(full_path):
            for filename in files:
                if not filename.endswith(".md"):
                    continue

                file_path = Path(root) / filename
                scan_result = scan_document(file_path, base_dir, staleness_thresholds, verbose)
                results["documents"].append(scan_result)
                results["summary"]["total_docs"] += 1

                if scan_result["status"] == "valid":
                    results["summary"]["valid"] += 1
                elif scan_result["status"] == "error":
                    results["summary"]["errors"] += 1
                elif scan_result["status"] == "warning":
                    results["summary"]["warnings"] += 1
                elif scan_result["status"] == "info":
                    results["summary"]["info"] += 1

    return results


def print_human_report(results: dict) -> None:
    """Print a human-readable report."""
    print("\n" + "=" * 60)
    print("Documentation Health Report")
    print("=" * 60)
    print(f"Scanned: {results['base_dir']}")
    print(f"Time: {results['scan_time']}")
    print("-" * 60)

    summary = results["summary"]
    print(f"Total docs: {summary['total_docs']}")
    print(f"  Valid: {summary['valid']}")
    print(f"  Errors: {summary['errors']}")
    print(f"  Warnings: {summary['warnings']}")
    print(f"  Info: {summary['info']}")

    # Group by status
    errors = [d for d in results["documents"] if d["status"] == "error"]
    warnings = [d for d in results["documents"] if d["status"] == "warning"]
    info = [d for d in results["documents"] if d["status"] == "info"]

    if errors:
        print("\n" + "-" * 60)
        print("ERRORS (must fix):")
        for doc in errors:
            print(f"\n  {doc['path']} [{doc['category']}]")
            for issue in doc["issues"]:
                if issue["severity"] == "error":
                    print(f"    ✗ {issue['message']}")

    if warnings:
        print("\n" + "-" * 60)
        print("WARNINGS (should fix):")
        for doc in warnings:
            print(f"\n  {doc['path']} [{doc['category']}]")
            for issue in doc["issues"]:
                if issue["severity"] == "warning":
                    print(f"    ⚠ {issue['message']}")

    if info:
        print("\n" + "-" * 60)
        print("INFO:")
        for doc in info:
            print(f"\n  {doc['path']} [{doc['category']}]")
            for issue in doc["issues"]:
                if issue["severity"] == "info":
                    print(f"    ℹ {issue['message']}")

    if not errors and not warnings and not info:
        print("\n✓ All documents are healthy!")

    print("\n" + "=" * 60)


def load_settings(base_dir: Path) -> dict:
    """Load project-specific settings from .claude/settings.yaml if it exists."""
    settings_path = base_dir / ".claude" / "settings.yaml"
    if settings_path.exists():
        try:
            import yaml
            with open(settings_path) as f:
                return yaml.safe_load(f) or {}
        except ImportError:
            pass
        except Exception:
            pass
    return {}


def main():
    parser = argparse.ArgumentParser(description="Check documentation health")
    parser.add_argument("--dir", type=str, default=".", help="Directory to check")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    parser.add_argument("--category", type=str, default="all",
                       choices=["tech", "product", "user", "all"],
                       help="Category to check")
    parser.add_argument("--staleness", type=int, default=None,
                       help="Days before marking as stale (overrides per-category defaults)")
    parser.add_argument("--verbose", action="store_true", help="Show all docs")
    args = parser.parse_args()

    base_dir = Path(args.dir).resolve()

    if not base_dir.exists():
        print(f"Error: Directory not found: {base_dir}", file=sys.stderr)
        sys.exit(1)

    # Load settings
    settings = load_settings(base_dir)
    doc_settings = settings.get("doc_maintenance", {})

    # Build staleness thresholds
    staleness_thresholds = DEFAULT_STALENESS.copy()
    if "categories" in doc_settings:
        staleness_thresholds.update(doc_settings["categories"])
    if args.staleness:
        # Override all with command line value
        for cat in staleness_thresholds:
            staleness_thresholds[cat] = args.staleness

    results = scan_directory(base_dir, args.category, staleness_thresholds, args.verbose)

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
