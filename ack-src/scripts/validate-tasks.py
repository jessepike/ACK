#!/usr/bin/env python3
"""
validate-tasks.py - Validate tasks.md structure and completeness

Usage: python3 validate-tasks.py <tasks.md>

Checks:
  - All tasks have required fields
  - Acceptance criteria are present
  - Task IDs are unique and sequential
  - Dependencies reference valid tasks
  - All tasks have complexity ratings

Exit codes:
  0 - All tasks valid
  1 - One or more validation errors
  2 - Error reading file
"""

import sys
import re
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field


@dataclass
class Task:
    """Represents a single task"""
    id: str
    title: Optional[str] = None
    phase: Optional[str] = None
    milestone: Optional[str] = None
    status: Optional[str] = None
    complexity: Optional[str] = None
    domain: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    assigned: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    description: Optional[str] = None
    acceptance_criteria: List[str] = field(default_factory=list)
    line_number: int = 0


def parse_tasks_md(filepath: str) -> List[Task]:
    """Parse tasks.md and extract all tasks"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"❌ Error reading file: {e}", file=sys.stderr)
        sys.exit(2)
    
    tasks = []
    current_task = None
    in_acceptance_criteria = False
    
    for i, line in enumerate(lines, 1):
        line = line.rstrip()
        
        # Task header: ### TASK-XXX: Title
        task_header = re.match(r'^###\s+(TASK-\d+):\s*(.+)$', line)
        if task_header:
            # Save previous task
            if current_task:
                tasks.append(current_task)
            
            # Start new task
            current_task = Task(
                id=task_header.group(1),
                title=task_header.group(2),
                line_number=i
            )
            in_acceptance_criteria = False
            continue
        
        if not current_task:
            continue
        
        # Parse task fields
        # Format: **Field:** Value
        field_match = re.match(r'^\*\*([^:]+):\*\*\s*(.*)$', line)
        if field_match:
            field_name = field_match.group(1).strip()
            field_value = field_match.group(2).strip()
            
            if field_name == "Phase":
                current_task.phase = field_value
            elif field_name == "Milestone":
                current_task.milestone = field_value
            elif field_name == "Status":
                current_task.status = field_value
            elif field_name == "Complexity":
                current_task.complexity = field_value
            elif field_name == "Domain":
                current_task.domain = field_value
            elif field_name == "Dependencies":
                if field_value and field_value.lower() not in ['none', '-']:
                    deps = [d.strip() for d in field_value.split(',')]
                    current_task.dependencies = deps
            elif field_name == "Assigned":
                current_task.assigned = field_value
            elif field_name == "Skills Required":
                if field_value and field_value.lower() not in ['none', '-']:
                    skills = [s.strip() for s in field_value.split(',')]
                    current_task.skills = skills
        
        # Description section
        if line.startswith("**Description:**"):
            in_acceptance_criteria = False
        elif re.match(r'^[A-Z].*', line) and not line.startswith('**'):
            # Part of description (starts with capital letter)
            if not in_acceptance_criteria and current_task.description is None:
                current_task.description = line
        
        # Acceptance Criteria section
        if line.startswith("**Acceptance Criteria:**"):
            in_acceptance_criteria = True
        elif in_acceptance_criteria and line.startswith("- [ ]"):
            criterion = line[5:].strip()
            current_task.acceptance_criteria.append(criterion)
    
    # Save last task
    if current_task:
        tasks.append(current_task)
    
    return tasks


def validate_task(task: Task, all_task_ids: Set[str]) -> List[str]:
    """Validate a single task and return list of errors"""
    errors = []
    
    # Required fields
    if not task.title:
        errors.append("Missing title")
    
    if not task.phase:
        errors.append("Missing phase")
    
    if not task.milestone:
        errors.append("Missing milestone")
    
    if not task.status:
        errors.append("Missing status")
    elif task.status not in ["Not Started", "In Progress", "Blocked", "Complete", "🔄 In Progress", "✅ Complete", "🚫 Blocked"]:
        errors.append(f"Invalid status: {task.status}")
    
    if not task.complexity:
        errors.append("Missing complexity")
    elif task.complexity not in ["Simple", "Medium", "Complex", "Very Complex"]:
        errors.append(f"Invalid complexity: {task.complexity}")
    
    if not task.domain:
        errors.append("Missing domain")
    
    if not task.assigned:
        errors.append("Missing assigned agent")
    
    if not task.description:
        errors.append("Missing description")
    
    if not task.acceptance_criteria:
        errors.append("Missing acceptance criteria")
    elif len(task.acceptance_criteria) < 3:
        errors.append(f"Only {len(task.acceptance_criteria)} acceptance criteria (recommend 3+)")
    
    # Validate dependencies reference valid tasks
    for dep in task.dependencies:
        # Extract TASK-XXX from dependency string
        dep_match = re.search(r'TASK-\d+', dep)
        if dep_match:
            dep_id = dep_match.group(0)
            if dep_id not in all_task_ids:
                errors.append(f"Invalid dependency: {dep_id} (task does not exist)")
        elif dep.lower() not in ['none', '-']:
            errors.append(f"Malformed dependency: {dep}")
    
    return errors


def check_task_sequence(tasks: List[Task]) -> List[str]:
    """Check that task IDs are sequential"""
    errors = []
    
    task_numbers = []
    for task in tasks:
        match = re.match(r'TASK-(\d+)', task.id)
        if match:
            task_numbers.append(int(match.group(1)))
    
    if not task_numbers:
        return errors
    
    task_numbers.sort()
    
    # Check for gaps
    for i in range(len(task_numbers) - 1):
        if task_numbers[i+1] != task_numbers[i] + 1:
            gap = task_numbers[i+1] - task_numbers[i] - 1
            errors.append(f"Gap in task sequence: TASK-{task_numbers[i]:03d} → TASK-{task_numbers[i+1]:03d} (missing {gap} task(s))")
    
    # Check numbering starts at 001
    if task_numbers[0] != 1:
        errors.append(f"Task numbering should start at 001, starts at {task_numbers[0]:03d}")
    
    return errors


def check_duplicate_ids(tasks: List[Task]) -> List[str]:
    """Check for duplicate task IDs"""
    errors = []
    seen = {}
    
    for task in tasks:
        if task.id in seen:
            errors.append(f"Duplicate task ID: {task.id} (lines {seen[task.id]} and {task.line_number})")
        else:
            seen[task.id] = task.line_number
    
    return errors


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    
    filepath = sys.argv[1]
    
    print("🔍 Validating tasks.md...")
    print()
    
    tasks = parse_tasks_md(filepath)
    
    if not tasks:
        print("⚠️  No tasks found in file")
        sys.exit(1)
    
    print(f"Found {len(tasks)} tasks")
    print()
    
    # Collect all task IDs
    all_task_ids = {task.id for task in tasks}
    
    # Check for duplicates
    duplicate_errors = check_duplicate_ids(tasks)
    if duplicate_errors:
        print("❌ Duplicate Task IDs:")
        for error in duplicate_errors:
            print(f"   {error}")
        print()
    
    # Check sequence
    sequence_errors = check_task_sequence(tasks)
    if sequence_errors:
        print("⚠️  Task Sequence Issues:")
        for error in sequence_errors:
            print(f"   {error}")
        print()
    
    # Validate each task
    all_valid = True
    task_errors = {}
    
    for task in tasks:
        errors = validate_task(task, all_task_ids)
        if errors:
            task_errors[task.id] = errors
            all_valid = False
    
    if task_errors:
        print("❌ Task Validation Errors:")
        print()
        for task_id, errors in task_errors.items():
            print(f"  {task_id}:")
            for error in errors:
                print(f"    - {error}")
        print()
    
    # Summary
    if all_valid and not duplicate_errors:
        print(f"✅ All {len(tasks)} tasks valid")
        if sequence_errors:
            print("⚠️  Note: Sequence warnings above (not blocking)")
        sys.exit(0)
    else:
        error_count = len(task_errors) + len(duplicate_errors)
        print(f"❌ {error_count} task(s) have errors")
        print()
        print("Fix the errors above before proceeding")
        sys.exit(1)


if __name__ == "__main__":
    main()
