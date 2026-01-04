#!/usr/bin/env python3
"""
trace-requirements.py - Generate complete traceability report

Shows full path from requirements through design to implementation:
  Requirement → Architecture → Stack → Tasks

Usage: python3 trace-requirements.py [--format text|json|csv]

Exit codes:
  0 - Complete traceability
  1 - Some requirements not fully traced
  2 - Error reading files
"""

import sys
import json
import csv
import re
from typing import Dict, List, Set
from dataclasses import dataclass, asdict
from io import StringIO


@dataclass
class TraceLink:
    """Represents a single requirement trace"""
    requirement_id: str
    requirement_title: str
    architecture_refs: List[str]
    stack_refs: List[str]
    data_model_refs: List[str]
    task_refs: List[str]
    fully_traced: bool
    
    def to_dict(self):
        return asdict(self)


def parse_requirements() -> Dict[str, str]:
    """Parse requirements and return {id: title}"""
    requirements = {}
    
    try:
        with open(".ipe/discovery/requirements.md", 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return requirements
    
    for match in re.finditer(r'^##\s+(R-\d+):\s*(.+)$', content, re.MULTILINE):
        requirements[match.group(1)] = match.group(2).strip()
    
    return requirements


def find_references_in_file(filepath: str, requirement_id: str) -> List[str]:
    """Find sections/components that reference a requirement"""
    refs = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return refs
    
    # Split into sections by headers
    sections = re.split(r'^#+\s+', content, flags=re.MULTILINE)
    
    for i, section in enumerate(sections):
        if i == 0:  # Skip before first header
            continue
        
        # Check if requirement is mentioned in this section
        if requirement_id in section or requirement_id.replace('R-', 'REQ-') in section:
            # Extract section title (first line)
            lines = section.split('\n')
            if lines:
                title = lines[0].strip()
                refs.append(title)
    
    return refs


def find_task_references(requirement_id: str) -> List[str]:
    """Find tasks that reference a requirement"""
    tasks = []
    
    try:
        with open(".ipe/implementation/tasks.md", 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return tasks
    
    # Find task sections that mention the requirement
    task_pattern = r'###\s+(TASK-\d+):[^\n]+'
    
    current_task = None
    for line in content.split('\n'):
        task_match = re.match(task_pattern, line)
        if task_match:
            current_task = task_match.group(1)
        elif current_task and (requirement_id in line or requirement_id.replace('R-', 'REQ-') in line):
            if current_task not in tasks:
                tasks.append(current_task)
    
    return tasks


def generate_traces(requirements: Dict[str, str]) -> List[TraceLink]:
    """Generate trace links for all requirements"""
    traces = []
    
    for req_id, req_title in requirements.items():
        # Find references in design documents
        arch_refs = find_references_in_file(".ipe/solution-design/architecture.md", req_id)
        stack_refs = find_references_in_file(".ipe/solution-design/stack.md", req_id)
        data_refs = find_references_in_file(".ipe/solution-design/data-model.md", req_id)
        task_refs = find_task_references(req_id)
        
        # Determine if fully traced
        has_design = bool(arch_refs or stack_refs or data_refs)
        has_tasks = bool(task_refs)
        fully_traced = has_design and has_tasks
        
        trace = TraceLink(
            requirement_id=req_id,
            requirement_title=req_title,
            architecture_refs=arch_refs,
            stack_refs=stack_refs,
            data_model_refs=data_refs,
            task_refs=task_refs,
            fully_traced=fully_traced
        )
        
        traces.append(trace)
    
    return traces


def output_text(traces: List[TraceLink]) -> None:
    """Output traceability report as formatted text"""
    
    print("═══════════════════════════════════════════════════════════════")
    print("  Requirement Traceability Matrix")
    print("═══════════════════════════════════════════════════════════════")
    print()
    
    fully_traced = [t for t in traces if t.fully_traced]
    partially_traced = [t for t in traces if not t.fully_traced and (t.architecture_refs or t.stack_refs or t.data_model_refs or t.task_refs)]
    not_traced = [t for t in traces if not (t.architecture_refs or t.stack_refs or t.data_model_refs or t.task_refs)]
    
    # Fully traced requirements
    if fully_traced:
        print(f"✅ Fully Traced ({len(fully_traced)}):")
        print()
        for trace in fully_traced:
            print(f"{trace.requirement_id}: {trace.requirement_title}")
            
            if trace.architecture_refs:
                print(f"  → Architecture: {', '.join(trace.architecture_refs)}")
            if trace.stack_refs:
                print(f"  → Stack: {', '.join(trace.stack_refs)}")
            if trace.data_model_refs:
                print(f"  → Data Model: {', '.join(trace.data_model_refs)}")
            if trace.task_refs:
                print(f"  → Tasks: {', '.join(trace.task_refs)}")
            print()
    
    # Partially traced
    if partially_traced:
        print(f"⚠️  Partially Traced ({len(partially_traced)}):")
        print()
        for trace in partially_traced:
            print(f"{trace.requirement_id}: {trace.requirement_title}")
            
            if trace.architecture_refs:
                print(f"  ✓ Architecture: {', '.join(trace.architecture_refs)}")
            else:
                print(f"  ✗ Architecture: Not referenced")
            
            if trace.stack_refs:
                print(f"  ✓ Stack: {', '.join(trace.stack_refs)}")
            
            if trace.data_model_refs:
                print(f"  ✓ Data Model: {', '.join(trace.data_model_refs)}")
            
            if trace.task_refs:
                print(f"  ✓ Tasks: {', '.join(trace.task_refs)}")
            else:
                print(f"  ✗ Tasks: Not implemented")
            print()
    
    # Not traced
    if not_traced:
        print(f"❌ Not Traced ({len(not_traced)}):")
        print()
        for trace in not_traced:
            print(f"{trace.requirement_id}: {trace.requirement_title}")
            print(f"  ✗ No references found in design or implementation")
            print()
    
    # Summary
    print("═══════════════════════════════════════════════════════════════")
    print("  Summary")
    print("═══════════════════════════════════════════════════════════════")
    print()
    
    total = len(traces)
    traced = len(fully_traced)
    percentage = (traced / total * 100) if total > 0 else 0
    
    print(f"Total Requirements:   {total}")
    print(f"Fully Traced:         {traced} ({percentage:.1f}%)")
    print(f"Partially Traced:     {len(partially_traced)}")
    print(f"Not Traced:           {len(not_traced)}")
    print()


def output_json(traces: List[TraceLink]) -> None:
    """Output traceability report as JSON"""
    
    output = {
        "total_requirements": len(traces),
        "fully_traced": len([t for t in traces if t.fully_traced]),
        "partially_traced": len([t for t in traces if not t.fully_traced and (t.architecture_refs or t.task_refs)]),
        "not_traced": len([t for t in traces if not (t.architecture_refs or t.task_refs)]),
        "traces": [t.to_dict() for t in traces]
    }
    
    print(json.dumps(output, indent=2))


def output_csv(traces: List[TraceLink]) -> None:
    """Output traceability report as CSV"""
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "Requirement ID",
        "Title",
        "Architecture",
        "Stack",
        "Data Model",
        "Tasks",
        "Fully Traced"
    ])
    
    # Data
    for trace in traces:
        writer.writerow([
            trace.requirement_id,
            trace.requirement_title,
            '; '.join(trace.architecture_refs) if trace.architecture_refs else '',
            '; '.join(trace.stack_refs) if trace.stack_refs else '',
            '; '.join(trace.data_model_refs) if trace.data_model_refs else '',
            '; '.join(trace.task_refs) if trace.task_refs else '',
            'Yes' if trace.fully_traced else 'No'
        ])
    
    print(output.getvalue())


def main():
    # Parse arguments
    output_format = 'text'
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--format', '-f']:
            if len(sys.argv) > 2:
                output_format = sys.argv[2]
            else:
                print("Error: --format requires argument (text|json|csv)", file=sys.stderr)
                sys.exit(2)
        elif sys.argv[1] in ['--help', '-h']:
            print(__doc__)
            sys.exit(0)
    
    if output_format not in ['text', 'json', 'csv']:
        print(f"Error: Invalid format '{output_format}' (must be text, json, or csv)", file=sys.stderr)
        sys.exit(2)
    
    # Generate traces
    requirements = parse_requirements()
    
    if not requirements:
        print("⚠️  No requirements found", file=sys.stderr)
        print("   Make sure you're in the project root directory", file=sys.stderr)
        sys.exit(2)
    
    traces = generate_traces(requirements)
    
    # Output in requested format
    if output_format == 'json':
        output_json(traces)
    elif output_format == 'csv':
        output_csv(traces)
    else:
        output_text(traces)
    
    # Exit based on traceability
    fully_traced = len([t for t in traces if t.fully_traced])
    total = len(traces)
    
    if fully_traced == total:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
