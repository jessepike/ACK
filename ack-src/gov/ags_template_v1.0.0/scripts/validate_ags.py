#!/usr/bin/env python3
"""
validate_ags.py — Minimal AGS enforcement script (v0)

What it does:
- Scans docs/ and schemas/ for Markdown files with YAML frontmatter.
- Validates required frontmatter keys (Tier 1 and Tier 2 supported).
- Ensures doc_id uniqueness.
- Validates depends_on references exist.
- Generates artifacts/ARTIFACT_REGISTRY.json from frontmatter (single source of truth).

Design intent:
- "One script that blocks something."
- Keep rules minimal and deterministic.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import subprocess
from dataclasses import dataclass
from pathlib import Path
from datetime import date
from typing import Any, Dict, List, Optional, Tuple
import re

try:
    import yaml  # type: ignore
except Exception as e:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    raise



VALID_ENUMS = {'type': ['adr', 'adr_index', 'agent_run', 'api_spec', 'architecture', 'artifact_registry', 'build_artifact', 'change_summary', 'data_model', 'drift_report', 'drift_rules', 'governance_policy', 'observability_plan', 'project_brief', 'prompt', 'release_notes', 'research_note', 'runbook', 'schema', 'security_baseline', 'standard', 'system_map', 'tasks_plan', 'test_strategy', 'threat_model', 'validation_plan', 'validation_result'], 'status': ['active', 'archived', 'deprecated', 'draft'], 'authority': ['binding', 'guidance', 'informational'], 'review_status': ['accepted', 'deprecated', 'draft', 'reviewed']}

OPTIONAL_KEYS = [
  "status",
  "authority",
  "review_status",
  "created",
  "updated",
  "owner",
  "depends_on",
]

DEFAULTS = {
  "status": "draft",
  "authority": "binding",
  "review_status": "draft",
  "owner": "human",
  "depends_on": [],
}

REQUIRED_KEYS = [
  "doc_id",
  "slug",
  "title",
  "type",
  "tier",
  "version"
]

SCAN_DIRS = ["docs", "schemas", "prompts"]  # prompts are tier2 in this package (still validated)


@dataclass
class Finding:
    level: str  # ERROR|WARN
    file: str
    message: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")



def render_frontmatter(fm: Dict[str, Any], body: str) -> str:
    return "---\n" + yaml.safe_dump(fm, sort_keys=False).strip() + "\n---\n\n" + (body.lstrip() if body else "")


def parse_frontmatter(md_text: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    Extract YAML frontmatter if present.

    Returns (frontmatter_dict_or_none, body_text).
    """
    if not md_text.startswith("---\n"):
        return None, md_text
    # Find second --- delimiter
    end = md_text.find("\n---\n", 4)
    if end == -1:
        return None, md_text
    fm_raw = md_text[4:end]
    body = md_text[end + 5 :]
    try:
        fm = yaml.safe_load(fm_raw) or {}
        if not isinstance(fm, dict):
            return None, md_text
        return fm, body
    except Exception:
        return None, md_text


def is_markdown(p: Path) -> bool:
    return p.suffix.lower() == ".md"


def scan_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for d in SCAN_DIRS:
        p = root / d
        if not p.exists():
            continue
        for f in p.rglob("*.md"):
            files.append(f)
    return sorted(files)


def validate_frontmatter(path: Path, fm: Dict[str, Any], findings: List[Finding], profile: str) -> None:
    # Required keys
    required = list(REQUIRED_KEYS)
    if profile == "strict":
        required += list(OPTIONAL_KEYS)
    for k in required:
        if k not in fm:
            findings.append(Finding("ERROR", str(path), f"Missing required frontmatter key: {k}"))

    # Apply defaults for optional keys (minimal profile)
    if profile == "minimal":
        for k, v in DEFAULTS.items():
            if k not in fm:
                fm[k] = v

    # Basic types
    if "depends_on" in fm and not isinstance(fm.get("depends_on"), list):
        findings.append(Finding("ERROR", str(path), "depends_on must be a list (can be empty)."))

    # Tier literal
    tier = fm.get("tier")
    if tier not in ("tier1", "tier2", "tier3"):
        findings.append(Finding("ERROR", str(path), f"tier must be one of tier1|tier2|tier3 (got: {tier})"))

    # doc_id sanity
    doc_id = fm.get("doc_id")
    if isinstance(doc_id, str):
        if len(doc_id.strip()) == 0:
            findings.append(Finding("ERROR", str(path), "doc_id is empty."))
        if doc_id.strip().upper() == "TODO":
            findings.append(Finding("ERROR", str(path), "doc_id is TODO. Use --next-id <prefix> to allocate a new id."))
    else:
        findings.append(Finding("ERROR", str(path), "doc_id must be a string."))



def validate_enums(path: Path, fm: Dict[str, Any], findings: List[Finding]) -> None:
    for key, allowed in VALID_ENUMS.items():
        val = fm.get(key)
        if val is None:
            continue
        if not isinstance(val, str):
            findings.append(Finding("ERROR", str(path), f"{key} must be a string (got {type(val).__name__})."))
            continue
        if val not in allowed:
            findings.append(Finding("ERROR", str(path), f"Invalid {key}: {val!r}. Allowed: {sorted(list(allowed))}"))



def registry_equal(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    try:
        return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    except Exception:
        return False


def load_registry_on_disk(root: Path) -> Optional[Dict[str, Any]]:
    p = root / "artifacts" / "ARTIFACT_REGISTRY.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def build_registry(records: List[Dict[str, Any]], root: Path) -> Dict[str, Any]:
    artifacts: List[Dict[str, Any]] = []
    for r in records:
        artifacts.append(
            {
                "artifact_id": r["doc_id"],
                "slug": r["slug"],
                "title": r["title"],
                "type": r["type"],
                "tier": r["tier"],
                "format": "md",
                "path": r["_relpath"],
                "status": r["status"],
                "authority": r["authority"],
                "version": r["version"],
                "review_status": r["review_status"],
                "depends_on": r.get("depends_on", []),
            }
        )
    return {"generated_by": "scripts/validate_ags.py", "artifacts": artifacts}




def generate_change_report(root: Path, diff_range: str) -> str:
    """Return a short git-based change report for the given diff range."""
    try:
        cmd = ["git", "-C", str(root), "log", "--oneline", f"{diff_range}", "--", "docs", "artifacts", "schemas", "scripts"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            return ""
        return res.stdout.strip()
    except Exception:
        return ""
def get_git_changed_files(root: Path, diff_range: str) -> Optional[List[str]]:
    """
    Return list of changed files (posix relative paths) using git diff.

    diff_range examples:
      - "HEAD" (default): changes in working tree vs HEAD
      - "--cached": staged changes
      - "origin/main...HEAD": range
    """
    git_dir = root / ".git"
    if not git_dir.exists():
        return None
    try:
        if diff_range == "--cached":
            cmd = ["git", "-C", str(root), "diff", "--name-only", "--cached"]
        else:
            cmd = ["git", "-C", str(root), "diff", "--name-only", diff_range]
        out = subprocess.check_output(cmd, text=True).strip()
        files = [line.strip().replace("\\", "/") for line in out.splitlines() if line.strip()]
        return files
    except Exception:
        return None


def load_drift_rules(root: Path) -> Optional[Dict[str, Any]]:
    p = root / "artifacts" / "drift_rules.yaml"
    if not p.exists():
        return None
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def check_drift_rules(changed: List[str], rules_doc: Dict[str, Any], findings: List[Finding]) -> None:
    rules = rules_doc.get("rules", [])
    if not isinstance(rules, list):
        return

    def any_changed(paths: List[str]) -> bool:
        for p in paths:
            if p.endswith("/"):
                if any(c.startswith(p) for c in changed):
                    return True
            else:
                if p in changed:
                    return True
        return False

    def any_prefix_changed(prefixes: List[str]) -> bool:
        for pref in prefixes:
            if any(c.startswith(pref) for c in changed):
                return True
        return False

    for rule in rules:
        if not isinstance(rule, dict):
            continue
        trigger_any = rule.get("trigger_any_changed", [])
        trigger_prefix = rule.get("trigger_prefix_changed", [])
        require_any = rule.get("require_any_changed", [])
        msg = rule.get("message", "Drift rule violated.")
        triggered = False

        if isinstance(trigger_any, list) and trigger_any and any_changed([str(x) for x in trigger_any if isinstance(x, (str,))]):
            triggered = True
        if isinstance(trigger_prefix, list) and trigger_prefix and any_prefix_changed([str(x) for x in trigger_prefix if isinstance(x, (str,))]):
            triggered = True

        if not triggered:
            continue

        # require any changed: accept file exact, or directory prefix
        if isinstance(require_any, list) and require_any:
            ok = False
            for req in require_any:
                if not isinstance(req, str):
                    continue
                if req.endswith("/"):
                    if any(c.startswith(req) for c in changed):
                        ok = True
                elif req.endswith("docs/adrs/"):
                    if any(c.startswith("docs/adrs/") for c in changed):
                        ok = True
                else:
                    if req in changed:
                        ok = True
            if not ok:
                findings.append(Finding("ERROR", "drift_rules", msg))



def compute_next_id(existing_ids: List[str], prefix: str) -> str:
    """
    Compute next id for a prefix.

    Supports:
      - numeric ids: doc-001
      - alpha prefix with dash and 3-digit number: gov-010
    """
    pref = prefix.rstrip("-")
    pat = re.compile(rf"^{re.escape(pref)}-(\d+)$")
    nums = []
    for i in existing_ids:
        m = pat.match(i)
        if m:
            try:
                nums.append(int(m.group(1)))
            except Exception:
                pass
    n = (max(nums) + 1) if nums else 1
    return f"{pref}-{n:03d}"



def infer_id_prefix(relpath: str) -> str:
    p = relpath.replace("\\", "/")
    if p.startswith("docs/adrs/"):
        return "adr"
    if p.startswith("docs/") and "GOVERNANCE" in p.upper():
        return "gov"
    if p.startswith("docs/"):
        return "doc"
    if p.startswith("schemas/"):
        return "sch"
    if p.startswith("prompts/"):
        return "prm"
    if p.startswith("artifacts/"):
        return "art"
    return "doc"


def write_allocated_id(path: Path, new_id: str) -> None:
    txt = read_text(path)
    fm, body = parse_frontmatter(txt)
    if not fm:
        return
    fm["doc_id"] = new_id
    # Update updated date if present
    if "updated" in fm:
        fm["updated"] = str(date.today())
    new_txt = render_frontmatter(fm, body)
    path.write_text(new_txt, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Package root directory (default: current dir)")
    ap.add_argument("--write-registry", action="store_true", help="Write artifacts/ARTIFACT_REGISTRY.json")
    ap.add_argument("--profile", choices=["strict","minimal"], default="strict", help="Validation profile: strict requires all schema keys; minimal requires only core keys and applies defaults.")
    ap.add_argument("--next-id", metavar="PREFIX", help="Print next available ID for a prefix (e.g., gov, adr). Exits after printing.")
    ap.add_argument("--change-report", action="store_true", help="Generate artifacts/CHANGE_REPORT.md from git log (if available).")
    ap.add_argument("--fix-todo-ids", action="store_true", help="Replace doc_id: TODO in files with allocated IDs (writes files).")
    ap.add_argument("--check-registry", action="store_true", help="Warn/error if artifacts/ARTIFACT_REGISTRY.json is out of sync with current scan.")
    ap.add_argument("--auto-check-drift", action="store_true", help="Run drift checks automatically when in a git repo (equivalent to --check-drift).")
    ap.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    ap.add_argument("--check-drift", action="store_true", help="Evaluate drift rules using git diff")
    ap.add_argument("--diff-range", default="HEAD", help="Git diff range (default: HEAD). Use --cached for staged changes.")
    args = ap.parse_args()

    if getattr(args, 'cached', False):
        args.diff_range = '--cached'
    if getattr(args, 'auto_check_drift', False):
        args.check_drift = True

    root = Path(args.root).resolve()
    # Scan files once (docs + ADRs).
    files = scan_files(root)

    # If asked, print next available id for a prefix and exit.
    if args.next_id:
        ids = []
        for f in files:
            fm, _ = parse_frontmatter(read_text(f))
            if fm and isinstance(fm.get("doc_id"), str):
                ids.append(fm["doc_id"])
        print(compute_next_id(ids, args.next_id))
        return 0

    findings: List[Finding] = []
    records: List[Dict[str, Any]] = []

    # Self-heal: replace doc_id: TODO using prefix allocation.
    if args.fix_todo_ids:
        ids = []
        for f in files:
            fm, _ = parse_frontmatter(read_text(f))
            if fm and isinstance(fm.get('doc_id'), str):
                ids.append(fm['doc_id'])
        # Allocate per-prefix to avoid collisions.
        for f in files:
            fm, _ = parse_frontmatter(read_text(f))
            if not fm:
                continue
            doc_id = fm.get('doc_id')
            if isinstance(doc_id, str) and doc_id.strip().upper() == 'TODO':
                rel = str(f.relative_to(root)).replace('\\','/')
                pref = infer_id_prefix(rel)
                new_id = compute_next_id(ids, pref)
                write_allocated_id(f, new_id)
                ids.append(new_id)
                print(f"Allocated {new_id} -> {rel}")
        # Re-scan after edits
        files = scan_files(root)
    if not files:
        print("ERROR: No markdown files found to scan.", file=sys.stderr)
        return 2

    # Parse and validate frontmatter
    for f in files:
        txt = read_text(f)
        fm, _body = parse_frontmatter(txt)
        if fm is None:
            findings.append(Finding("ERROR", str(f), "Missing or invalid YAML frontmatter block."))
            continue

        validate_frontmatter(f, fm, findings, args.profile)
        validate_enums(f, fm, findings)
        fm["_relpath"] = str(f.relative_to(root)).replace("\\", "/")
        records.append(fm)

    # Uniqueness checks
    seen: Dict[str, str] = {}
    for r in records:
        doc_id = r.get("doc_id")
        if not isinstance(doc_id, str):
            continue
        if doc_id in seen:
            findings.append(Finding("ERROR", r["_relpath"], f"Duplicate doc_id '{doc_id}' (also in {seen[doc_id]})."))
        else:
            seen[doc_id] = r["_relpath"]

    # depends_on references
    known_ids = set(seen.keys())
    for r in records:
        deps = r.get("depends_on", [])
        if not isinstance(deps, list):
            continue
        for dep in deps:
            if not isinstance(dep, str):
                findings.append(Finding("ERROR", r["_relpath"], f"depends_on contains non-string value: {dep!r}"))
                continue
            if dep not in known_ids:
                findings.append(Finding("ERROR", r["_relpath"], f"depends_on references missing doc_id: {dep}"))

    # Registry generation
    registry = build_registry(records, root)
    if args.write_registry:
        out = root / "artifacts" / "ARTIFACT_REGISTRY.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(registry, indent=2), encoding="utf-8")
        print(f"WROTE registry: {out}")

    # Registry freshness check (derived registry must match on-disk JSON).
    if args.check_registry:
        on_disk = load_registry_on_disk(root)
        if on_disk is None:
            findings.append(Finding('WARN', 'artifacts/ARTIFACT_REGISTRY.json', 'Registry missing on disk. Run with --write-registry.'))
        elif not registry_equal(on_disk, registry):
            msg = 'Registry out of sync with current scan. Run with --write-registry.'
            if args.profile == 'strict':
                findings.append(Finding('ERROR', 'artifacts/ARTIFACT_REGISTRY.json', msg))
            else:
                findings.append(Finding('WARN', 'artifacts/ARTIFACT_REGISTRY.json', msg))


    # Optional: generate a git-based change report (best-effort).
    if args.change_report:
        report = generate_change_report(root, args.diff_range)
        if report:
            out_path = root / "artifacts" / "CHANGE_REPORT.md"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text("# CHANGE_REPORT.md\n\n" + report + "\n", encoding="utf-8")
        else:
            findings.append(Finding("WARN", "artifacts/CHANGE_REPORT.md", "Unable to generate change report (git unavailable or no changes)."))

    # Drift rule enforcement (best-effort; requires git + drift_rules.yaml).
    if args.check_drift:
        changed = get_git_changed_files(root, args.diff_range)
        if changed is not None:
            rules = load_drift_rules(root)
            if rules:
                check_drift_rules(changed, rules, findings)
            else:
                findings.append(Finding("WARN", "drift_rules.yaml", "Drift checking enabled but drift_rules.yaml not found or empty."))
        else:
            findings.append(Finding("WARN", "git", "Drift checking enabled but git diff could not be computed."))
    # Print report
    errors = [f for f in findings if f.level == "ERROR"]
    warns = [f for f in findings if f.level == "WARN"]

    for f in errors + warns:
        print(f"{f.level}: {f.file}: {f.message}")

    if errors:
        print(f"\nFAILED: {len(errors)} error(s), {len(warns)} warning(s)")
        return 1
    if args.strict and warns:
        print(f"\nFAILED (strict): {len(warns)} warning(s)")
        return 1

    print(f"\nOK: {len(records)} file(s) validated. Errors: 0. Warnings: {len(warns)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
