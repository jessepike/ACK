#!/usr/bin/env python3
"""
check-token-budget.py - Validate CLAUDE.md token budget

Ensures CLAUDE.md and its imports stay within recommended limits:
  - Target: ~20,000 tokens (~80,000 chars)
  - Warning: >30,000 tokens (~120,000 chars)
  - Maximum: <50,000 tokens (~200,000 chars)

Usage: python3 check-token-budget.py [claude-md-path]

Exit codes:
  0 - Within budget
  1 - Exceeds budget
  2 - Error reading files
"""

import sys
import os
import re
from typing import List, Tuple


# Rough token estimation (GPT-4 style)
# 1 token ≈ 4 characters for English text
CHARS_PER_TOKEN = 4

# Budgets in tokens
TARGET_BUDGET = 20000
WARNING_BUDGET = 30000
MAX_BUDGET = 50000


def estimate_tokens(text: str) -> int:
    """Estimate token count from character count"""
    return len(text) // CHARS_PER_TOKEN


def find_imports(content: str, base_path: str) -> List[Tuple[str, int]]:
    """Find all @imports in CLAUDE.md and return (path, token_count)"""
    imports = []
    
    # Find all lines starting with @
    for line in content.split('\n'):
        if line.strip().startswith('@'):
            import_path = line.strip()[1:]  # Remove @
            
            # Resolve relative to base_path
            if not import_path.startswith('/'):
                import_path = os.path.join(base_path, import_path)
            
            # Check if file exists
            if os.path.isfile(import_path):
                try:
                    with open(import_path, 'r', encoding='utf-8') as f:
                        import_content = f.read()
                    
                    tokens = estimate_tokens(import_content)
                    imports.append((import_path, tokens))
                except Exception as e:
                    print(f"⚠️  Error reading import {import_path}: {e}", file=sys.stderr)
            else:
                print(f"⚠️  Import file not found: {import_path}", file=sys.stderr)
    
    return imports


def analyze_claude_md(filepath: str = ".claude/CLAUDE.md") -> Tuple[int, int, List[Tuple[str, int]]]:
    """
    Analyze CLAUDE.md and return (core_tokens, total_tokens, imports)
    
    Returns:
        core_tokens: Tokens in CLAUDE.md itself
        total_tokens: Core + all imports
        imports: List of (path, tokens) for each import
    """
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"❌ Error reading file: {e}", file=sys.stderr)
        sys.exit(2)
    
    # Calculate core tokens (CLAUDE.md content)
    core_tokens = estimate_tokens(content)
    
    # Find and calculate import tokens
    base_path = os.path.dirname(filepath)
    if not base_path:
        base_path = "."
    
    imports = find_imports(content, base_path)
    import_tokens = sum(tokens for _, tokens in imports)
    
    total_tokens = core_tokens + import_tokens
    
    return core_tokens, total_tokens, imports


def format_tokens(tokens: int) -> str:
    """Format token count with appropriate color"""
    if tokens <= TARGET_BUDGET:
        return f"\033[0;32m{tokens:,}\033[0m"  # Green
    elif tokens <= WARNING_BUDGET:
        return f"\033[1;33m{tokens:,}\033[0m"  # Yellow
    else:
        return f"\033[0;31m{tokens:,}\033[0m"  # Red


def format_size(chars: int) -> str:
    """Format character count as KB"""
    kb = chars / 1024
    return f"{kb:.1f} KB"


def main():
    if len(sys.argv) > 2:
        print(__doc__)
        sys.exit(2)
    
    filepath = sys.argv[1] if len(sys.argv) == 2 else ".claude/CLAUDE.md"
    
    print("🔍 Checking CLAUDE.md token budget...")
    print()
    
    core_tokens, total_tokens, imports = analyze_claude_md(filepath)
    
    # Display results
    print("═══════════════════════════════════════════════════════════════")
    print("  CLAUDE.md Token Budget Analysis")
    print("═══════════════════════════════════════════════════════════════")
    print()
    
    print(f"Core CLAUDE.md:      {format_tokens(core_tokens)} tokens ({format_size(core_tokens * CHARS_PER_TOKEN)})")
    print()
    
    if imports:
        print(f"Imports ({len(imports)} files):")
        print()
        
        # Sort by token count descending
        imports_sorted = sorted(imports, key=lambda x: x[1], reverse=True)
        
        for path, tokens in imports_sorted:
            # Show relative path from project root
            rel_path = os.path.relpath(path)
            print(f"  {rel_path}")
            print(f"    {format_tokens(tokens)} tokens ({format_size(tokens * CHARS_PER_TOKEN)})")
        
        print()
        import_total = sum(tokens for _, tokens in imports)
        print(f"Total Imports:       {format_tokens(import_total)} tokens")
        print()
    else:
        print("No imports found")
        print()
    
    print("─────────────────────────────────────────────────────────────────")
    print(f"TOTAL:               {format_tokens(total_tokens)} tokens ({format_size(total_tokens * CHARS_PER_TOKEN)})")
    print()
    
    # Budget comparison
    print("─────────────────────────────────────────────────────────────────")
    print("Budget Targets:")
    print()
    print(f"  Target:   {TARGET_BUDGET:,} tokens  ({format_size(TARGET_BUDGET * CHARS_PER_TOKEN)})")
    print(f"  Warning:  {WARNING_BUDGET:,} tokens  ({format_size(WARNING_BUDGET * CHARS_PER_TOKEN)})")
    print(f"  Maximum:  {MAX_BUDGET:,} tokens  ({format_size(MAX_BUDGET * CHARS_PER_TOKEN)})")
    print()
    
    # Status
    if total_tokens <= TARGET_BUDGET:
        print("✅ Within target budget")
        percentage = (total_tokens / TARGET_BUDGET) * 100
        print(f"   Using {percentage:.1f}% of target budget")
        exit_code = 0
    elif total_tokens <= WARNING_BUDGET:
        print("⚠️  Exceeds target, within warning threshold")
        percentage = (total_tokens / WARNING_BUDGET) * 100
        print(f"   Using {percentage:.1f}% of warning budget")
        print()
        print("   Recommendation: Consider pruning or moving content to optional imports")
        exit_code = 0  # Warning, not failure
    elif total_tokens <= MAX_BUDGET:
        print("⚠️  Exceeds warning threshold")
        percentage = (total_tokens / MAX_BUDGET) * 100
        print(f"   Using {percentage:.1f}% of maximum budget")
        print()
        print("   ⚠️  URGENT: Reduce token count before proceeding")
        print("   Actions:")
        print("     - Move large imports to optional (commented out)")
        print("     - Condense decision summaries")
        print("     - Remove verbose content")
        exit_code = 1
    else:
        print("❌ EXCEEDS MAXIMUM BUDGET")
        over_budget = total_tokens - MAX_BUDGET
        print(f"   Over by {over_budget:,} tokens ({format_size(over_budget * CHARS_PER_TOKEN)})")
        print()
        print("   ❌ CRITICAL: Must reduce before implementation")
        print("   Actions:")
        print("     1. Move all optional imports to commented section")
        print("     2. Significantly condense core CLAUDE.md")
        print("     3. Consider using progressive disclosure")
        print("     4. Remove redundant content")
        exit_code = 1
    
    print()
    
    # Suggestions if over target
    if total_tokens > TARGET_BUDGET and imports:
        print("─────────────────────────────────────────────────────────────────")
        print("Optimization Suggestions:")
        print()
        
        # Find largest imports
        largest = sorted(imports, key=lambda x: x[1], reverse=True)[:3]
        
        print("  Largest imports to consider moving to optional:")
        for path, tokens in largest:
            rel_path = os.path.relpath(path)
            print(f"    - {rel_path} ({tokens:,} tokens)")
        
        print()
        print("  To make import optional, comment it out in CLAUDE.md:")
        print("    # @.ipe/verbose-artifact.md  # Optional, load on demand")
        print()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
