#!/usr/bin/env python3
"""
coverage-check.py - Verify requirement coverage in implementation plan

Ensures every requirement from Stage 1 has:
  - Architecture component in Stage 2
  - Task(s) in Stage 5

Usage: python3 coverage-check.py

Exit codes:
  0 - All requirements covered
  1 - Some requirements not covered
  2 - Error reading files
"""

import sys
import re
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass


@dataclass
class Requirement:
    """Represents a requirement from discovery"""
    id: str
    title: str
    description: str = ""
    covered_by_architecture: bool = False
    covered_by_tasks: List[str] = None
    
    def __post_init__(self):
        if self.covered_by_tasks is None:
            self.covered_by_tasks = []


def parse_requirements(filepath: str = ".ipe/discovery/requirements.md") -> Dict[str, Requirement]:
    """Parse requirements.md and extract all requirements"""
    requirements = {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"⚠️  File not found: {filepath}", file=sys.stderr)
        print("   Run from project root directory", file=sys.stderr)
        return requirements
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}", file=sys.stderr)
        return requirements
    
    # Parse requirements
    # Format: ## R-XXX: Title
    req_pattern = r'^##\s+(R-\d+):\s*(.+)$'
    
    current_req = None
    
    for line in content.split('\n'):
        req_match = re.match(req_pattern, line)
        if req_match:
            req_id = req_match.group(1)
            req_title = req_match.group(2).strip()
            current_req = Requirement(id=req_id, title=req_title)
            requirements[req_id] = current_req
        elif current_req and line.strip() and not line.startswith('#'):
            # Add to description
            current_req.description += line + " "
    
    return requirements


def check_architecture_coverage(requirements: Dict[str, Requirement]) -> None:
    """Check if requirements are addressed in architecture"""
    
    arch_files = [
        ".ipe/solution-design/architecture.md",
        ".ipe/solution-design/stack.md",
        ".ipe/solution-design/data-model.md"
    ]
    
    architecture_content = ""
    for filepath in arch_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                architecture_content += f.read() + "\n"
        except FileNotFoundError:
            continue
    
    # Check if each requirement ID appears in architecture docs
    for req_id in requirements:
        if req_id in architecture_content or \
           req_id.replace('R-', 'REQ-') in architecture_content:
            requirements[req_id].covered_by_architecture = True


def check_task_coverage(requirements: Dict[str, Requirement]) -> None:
    """Check if requirements are covered by tasks"""
    
    try:
        with open(".ipe/implementation/tasks.md", 'r', encoding='utf-8') as f:
            tasks_content = f.read()
    except FileNotFoundError:
        print("⚠️  tasks.md not found, skipping task coverage check", file=sys.stderr)
        return
    
    # For each requirement, find tasks that reference it
    for req_id in requirements:
        # Look for requirement references in tasks
        # Could be in context links, description, or comments
        task_pattern = r'(TASK-\d+)[^\n]*' + re.escape(req_id)
        
        for match in re.finditer(task_pattern, tasks_content):
            task_id = match.group(1)
            if task_id not in requirements[req_id].covered_by_tasks:
                requirements[req_id].covered_by_tasks.append(task_id)
        
        # Also check reverse: requirement mentioned near task
        # Split into task sections
        task_sections = re.split(r'^###\s+TASK-\d+:', tasks_content, flags=re.MULTILINE)
        
        for i, section in enumerate(task_sections[1:], 1):  # Skip header
            if req_id in section or req_id.replace('R-', 'REQ-') in section:
                # Extract task ID from next header
                task_match = re.search(r'^###\s+(TASK-\d+):', task_sections[i], re.MULTILINE)
                if task_match:
                    task_id = task_match.group(1)
                    if task_id not in requirements[req_id].covered_by_tasks:
                        requirements[req_id].covered_by_tasks.append(task_id)


def generate_report(requirements: Dict[str, Requirement]) -> Tuple[int, int, int]:
    """Generate coverage report and return (total, covered, uncovered)"""
    
    print("═══════════════════════════════════════════════════════════════")
    print("  Requirement Traceability Report")
    print("═══════════════════════════════════════════════════════════════")
    print()
    
    fully_covered = []
    partially_covered = []
    not_covered = []
    
    for req_id in sorted(requirements.keys()):
        req = requirements[req_id]
        
        has_arch = req.covered_by_architecture
        has_tasks = len(req.covered_by_tasks) > 0
        
        if has_arch and has_tasks:
            fully_covered.append(req)
        elif has_arch or has_tasks:
            partially_covered.append(req)
        else:
            not_covered.append(req)
    
    # Show fully covered (brief)
    if fully_covered:
        print(f"✅ Fully Covered ({len(fully_covered)} requirements):")
        print()
        for req in fully_covered:
            tasks_str = ", ".join(req.covered_by_tasks)
            print(f"  {req.id}: {req.title}")
            print(f"    → Tasks: {tasks_str}")
        print()
    
    # Show partially covered (detailed)
    if partially_covered:
        print(f"⚠️  Partially Covered ({len(partially_covered)} requirements):")
        print()
        for req in partially_covered:
            print(f"  {req.id}: {req.title}")
            if req.covered_by_architecture:
                print(f"    ✓ Architecture coverage")
            else:
                print(f"    ✗ Not referenced in architecture")
            
            if req.covered_by_tasks:
                tasks_str = ", ".join(req.covered_by_tasks)
                print(f"    ✓ Task coverage: {tasks_str}")
            else:
                print(f"    ✗ No tasks identified")
        print()
    
    # Show not covered (detailed)
    if not_covered:
        print(f"❌ Not Covered ({len(not_covered)} requirements):")
        print()
        for req in not_covered:
            print(f"  {req.id}: {req.title}")
            print(f"    ✗ Not referenced in architecture")
            print(f"    ✗ No tasks identified")
        print()
    
    # Summary
    print("═══════════════════════════════════════════════════════════════")
    print("  Summary")
    print("═══════════════════════════════════════════════════════════════")
    print()
    
    total = len(requirements)
    covered = len(fully_covered)
    percentage = (covered / total * 100) if total > 0 else 0
    
    print(f"Total Requirements:   {total}")
    print(f"Fully Covered:        {covered} ({percentage:.1f}%)")
    print(f"Partially Covered:    {len(partially_covered)}")
    print(f"Not Covered:          {len(not_covered)}")
    print()
    
    return total, covered, len(not_covered)


def main():
    print("🔍 Checking requirement coverage...")
    print()
    
    # Parse requirements
    requirements = parse_requirements()
    
    if not requirements:
        print("⚠️  No requirements found or requirements.md not accessible")
        print("   Make sure you're in the project root directory")
        sys.exit(2)
    
    print(f"Found {len(requirements)} requirements")
    print()
    
    # Check coverage
    print("Checking architecture coverage...")
    check_architecture_coverage(requirements)
    
    print("Checking task coverage...")
    check_task_coverage(requirements)
    
    print()
    
    # Generate report
    total, covered, uncovered = generate_report(requirements)
    
    # Exit based on coverage
    if uncovered == 0:
        print("✅ All requirements have full traceability")
        print()
        print("Every requirement is:")
        print("  1. Addressed in solution design (architecture/stack/data model)")
        print("  2. Implemented by one or more tasks")
        sys.exit(0)
    else:
        print("❌ Some requirements lack full coverage")
        print()
        print("Action items:")
        if uncovered > 0:
            print("  1. Review uncovered requirements")
            print("  2. Add architecture components or tasks as needed")
            print("  3. Ensure requirement IDs are referenced in artifacts")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
