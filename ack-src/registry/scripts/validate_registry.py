#!/usr/bin/env python3
"""
validate_registry.py — Agent Context Registry validator

Validates:
- YAML frontmatter on all .md files
- Required fields per profile (minimal vs strict)
- Enum values for type, status, tier, authority
- Unique doc_ids across registry
- depends_on references exist
- Anthropic skill format (name + description in SKILL.md)

Scans:
- Root primitive dirs: agents/, skills/, tools/, commands/, prompts/, policies/
- Nested domain dirs: domains/*/agents/, domains/*/skills/, etc.
- Docs: docs/
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import re

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


VALID_TYPES = [
    "agent", "skill", "tool", "command", "prompt", "policy",
    "domain_summary", "research_note", "guide", "artifact_registry", "template",
]

VALID_ENUMS = {
    "type": VALID_TYPES,
    "status": ["draft", "active", "deprecated", "archived"],
    "tier": ["tier1", "tier2", "tier3"],
    "authority": ["binding", "guidance", "informational"],
    "review_status": ["draft", "pending", "approved", "deprecated"],
}

REQUIRED_KEYS_STRICT = [
    "doc_id", "slug", "title", "type", "tier", "status",
    "authority", "version", "review_status", "created", "updated", "owner", "depends_on",
]

REQUIRED_KEYS_MINIMAL = ["doc_id", "type", "tier", "version"]

ANTHROPIC_SKILL_KEYS = ["name", "description"]

DEFAULTS = {
    "status": "draft",
    "authority": "guidance",
    "review_status": "draft",
    "owner": "human",
    "depends_on": [],
}

ROOT_DIRS = ["agents", "skills", "tools", "commands", "prompts", "policies", "docs"]
DOMAIN_SUBDIRS = ["agents", "skills", "tools", "commands"]


@dataclass
class Finding:
    level: str
    file: str
    message: str


def parse_frontmatter(text: str) -> Tuple[Optional[Dict[str, Any]], str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        end = text.find("\n---", 4)
        if end == -1:
            return None, text
    fm_raw = text[4:end]
    body = text[end + 4:].lstrip("-\n")
    try:
        fm = yaml.safe_load(fm_raw) or {}
        return (fm, body) if isinstance(fm, dict) else (None, text)
    except yaml.YAMLError:
        return None, text


def scan_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for d in ROOT_DIRS:
        dir_path = root / d
        if dir_path.exists():
            for f in dir_path.rglob("*.md"):
                files.append(f)
    domains_path = root / "domains"
    if domains_path.exists():
        for domain_dir in domains_path.iterdir():
            if domain_dir.is_dir():
                for f in domain_dir.glob("*.md"):
                    files.append(f)
                for subdir in DOMAIN_SUBDIRS:
                    subdir_path = domain_dir / subdir
                    if subdir_path.exists():
                        for f in subdir_path.rglob("*.md"):
                            files.append(f)
    for d in ["templates"]:
        dir_path = root / d
        if dir_path.exists():
            for f in dir_path.rglob("*.md"):
                files.append(f)
    return sorted(set(files))


def is_skill_file(path: Path) -> bool:
    return path.name == "SKILL.md"


def validate_anthropic_skill(path: Path, fm: Dict[str, Any], findings: List[Finding]) -> None:
    for key in ANTHROPIC_SKILL_KEYS:
        if key not in fm:
            findings.append(Finding("ERROR", str(path), f"SKILL.md missing Anthropic key: {key}"))
        elif not isinstance(fm[key], str) or not fm[key].strip():
            findings.append(Finding("ERROR", str(path), f"SKILL.md {key} must be non-empty string"))


def validate_frontmatter(path: Path, fm: Dict[str, Any], findings: List[Finding], profile: str) -> None:
    required = REQUIRED_KEYS_STRICT if profile == "strict" else REQUIRED_KEYS_MINIMAL
    for key in required:
        if key not in fm:
            findings.append(Finding("ERROR", str(path), f"Missing required key: {key}"))
    if profile == "minimal":
        for key, default in DEFAULTS.items():
            if key not in fm:
                fm[key] = default
    if "depends_on" in fm and not isinstance(fm.get("depends_on"), list):
        findings.append(Finding("ERROR", str(path), "depends_on must be a list"))
    tier = fm.get("tier")
    if tier and tier not in VALID_ENUMS["tier"]:
        findings.append(Finding("ERROR", str(path), f"Invalid tier: {tier}"))
    doc_id = fm.get("doc_id")
    if doc_id:
        if not isinstance(doc_id, str):
            findings.append(Finding("ERROR", str(path), "doc_id must be a string"))
        elif not doc_id.strip():
            findings.append(Finding("ERROR", str(path), "doc_id is empty"))
        elif doc_id.strip().upper() == "TODO":
            findings.append(Finding("WARN", str(path), "doc_id is TODO"))


def validate_enums(path: Path, fm: Dict[str, Any], findings: List[Finding]) -> None:
    for key, allowed in VALID_ENUMS.items():
        val = fm.get(key)
        if val is None:
            continue
        if not isinstance(val, str):
            findings.append(Finding("ERROR", str(path), f"{key} must be string"))
            continue
        if val not in allowed:
            findings.append(Finding("ERROR", str(path), f"Invalid {key}: '{val}'. Allowed: {allowed}"))


def infer_type_from_path(path: Path, root: Path) -> Optional[str]:
    rel = path.relative_to(root)
    parts = rel.parts
    if "agents" in parts:
        return "agent"
    if "skills" in parts:
        return "skill"
    if "tools" in parts:
        return "tool"
    if "commands" in parts:
        return "command"
    if "prompts" in parts:
        return "prompt"
    if "policies" in parts:
        return "policy"
    if "docs" in parts:
        return "research_note"
    return None


def compute_next_id(existing_ids: List[str], prefix: str) -> str:
    pref = prefix.rstrip("-")
    pat = re.compile(rf"^{re.escape(pref)}-(\d+)$")
    nums = []
    for i in existing_ids:
        m = pat.match(i)
        if m:
            nums.append(int(m.group(1)))
    n = (max(nums) + 1) if nums else 1
    return f"{pref}-{n:03d}"


def build_inventory(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    items = []
    for r in records:
        items.append({
            "doc_id": r.get("doc_id"),
            "type": r.get("type"),
            "tier": r.get("tier"),
            "status": r.get("status", "draft"),
            "path": r.get("_relpath"),
            "name": r.get("name"),
            "title": r.get("title"),
        })
    return {"generated_by": "scripts/validate_registry.py", "count": len(items), "items": items}


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate Agent Context Registry")
    ap.add_argument("--root", default=".", help="Registry root directory")
    ap.add_argument("--profile", choices=["strict", "minimal"], default="minimal")
    ap.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    ap.add_argument("--write-inventory", action="store_true")
    ap.add_argument("--next-id", metavar="PREFIX")
    ap.add_argument("--summary", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"ERROR: Root not found: {root}", file=sys.stderr)
        return 2

    files = scan_files(root)
    if not files:
        print("No markdown files found.", file=sys.stderr)
        return 0

    if args.next_id:
        ids = []
        for f in files:
            text = f.read_text(encoding="utf-8")
            fm, _ = parse_frontmatter(text)
            if fm and isinstance(fm.get("doc_id"), str):
                ids.append(fm["doc_id"])
        print(compute_next_id(ids, args.next_id))
        return 0

    findings: List[Finding] = []
    records: List[Dict[str, Any]] = []

    for f in files:
        text = f.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        relpath = str(f.relative_to(root))

        if fm is None:
            if args.profile == "strict":
                findings.append(Finding("ERROR", relpath, "Missing frontmatter"))
            else:
                findings.append(Finding("WARN", relpath, "No frontmatter"))
            continue

        if is_skill_file(f):
            validate_anthropic_skill(f, fm, findings)

        has_ags = "doc_id" in fm
        if has_ags or args.profile == "strict":
            validate_frontmatter(f, fm, findings, args.profile)
            validate_enums(f, fm, findings)
        elif not has_ags:
            inferred = infer_type_from_path(f, root)
            findings.append(Finding("INFO", relpath, f"No AGS (inferred: {inferred})"))

        fm["_relpath"] = relpath
        records.append(fm)

    seen: Dict[str, str] = {}
    for r in records:
        doc_id = r.get("doc_id")
        if not isinstance(doc_id, str) or not doc_id.strip():
            continue
        if doc_id in seen:
            findings.append(Finding("ERROR", r["_relpath"], f"Duplicate doc_id '{doc_id}' (also: {seen[doc_id]})"))
        else:
            seen[doc_id] = r["_relpath"]

    known_ids = set(seen.keys())
    for r in records:
        deps = r.get("depends_on", [])
        if not isinstance(deps, list):
            continue
        for dep in deps:
            if isinstance(dep, str) and dep not in known_ids:
                findings.append(Finding("WARN", r["_relpath"], f"depends_on unknown: {dep}"))

    if args.write_inventory:
        inventory = build_inventory(records)
        out_dir = root / "artifacts"
        out_dir.mkdir(exist_ok=True)
        out_path = out_dir / "REGISTRY_INVENTORY.json"
        out_path.write_text(json.dumps(inventory, indent=2), encoding="utf-8")
        print(f"Wrote: {out_path}")

    errors = [f for f in findings if f.level == "ERROR"]
    warns = [f for f in findings if f.level == "WARN"]
    infos = [f for f in findings if f.level == "INFO"]

    for f in errors:
        print(f"ERROR: {f.file}: {f.message}")
    for f in warns:
        print(f"WARN: {f.file}: {f.message}")

    if args.summary:
        type_counts: Dict[str, int] = {}
        for r in records:
            t = r.get("type") or infer_type_from_path(Path(root / r["_relpath"]), root) or "unknown"
            type_counts[t] = type_counts.get(t, 0) + 1
        print("\n--- Summary ---")
        for t, c in sorted(type_counts.items()):
            print(f"  {t}: {c}")

    print(f"\nScanned: {len(files)} | Records: {len(records)} | Errors: {len(errors)} | Warns: {len(warns)}")

    if errors:
        return 1
    if args.strict and warns:
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
