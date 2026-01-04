#!/usr/bin/env python3
"""
check-cycles.py - Detect circular dependencies in task graph

Usage: python3 check-cycles.py <dependencies.md>

Exit codes:
  0 - No circular dependencies found
  1 - Circular dependencies detected
  2 - Error reading file or invalid format
"""

import sys
import re
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class DependencyGraph:
    """Directed graph for task dependencies"""
    
    def __init__(self):
        self.graph: Dict[str, Set[str]] = defaultdict(set)
        self.all_tasks: Set[str] = set()
    
    def add_edge(self, from_task: str, to_task: str):
        """Add dependency: from_task depends on to_task"""
        self.graph[from_task].add(to_task)
        self.all_tasks.add(from_task)
        self.all_tasks.add(to_task)
    
    def find_cycles(self) -> List[List[str]]:
        """Find all cycles in the graph using DFS"""
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node: str, path: List[str]) -> bool:
            """DFS helper that returns True if cycle found"""
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in self.graph.get(node, set()):
                if neighbor not in visited:
                    if dfs(neighbor, path):
                        return True
                elif neighbor in rec_stack:
                    # Found a cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append(cycle)
                    return True
            
            path.pop()
            rec_stack.remove(node)
            return False
        
        for task in self.all_tasks:
            if task not in visited:
                dfs(task, [])
        
        return cycles


def parse_dependencies_md(filepath: str) -> DependencyGraph:
    """Parse dependencies.md and build dependency graph"""
    
    graph = DependencyGraph()
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"❌ Error reading file: {e}", file=sys.stderr)
        sys.exit(2)
    
    # Parse dependency matrix if it exists
    # Format: | TASK-XXX | TASK-YYY, TASK-ZZZ | ... |
    matrix_pattern = r'\|\s*(TASK-\d+)\s*\|\s*([^|]*)\s*\|'
    
    for match in re.finditer(matrix_pattern, content):
        task = match.group(1).strip()
        deps_str = match.group(2).strip()
        
        if deps_str and deps_str.lower() not in ['none', '-', '']:
            # Parse comma-separated dependencies
            deps = [d.strip() for d in deps_str.split(',')]
            for dep in deps:
                # Extract TASK-XXX from dep (may have extra text)
                dep_match = re.search(r'TASK-\d+', dep)
                if dep_match:
                    dep_task = dep_match.group(0)
                    graph.add_edge(task, dep_task)
    
    # Also parse from dependency graph section
    # Format: TASK-XXX → TASK-YYY or TASK-XXX depends on TASK-YYY
    arrow_pattern = r'(TASK-\d+)\s*→\s*(TASK-\d+)'
    depends_pattern = r'(TASK-\d+)\s+depends\s+on\s+([TASK-\d+,\s]+)'
    
    for match in re.finditer(arrow_pattern, content):
        from_task = match.group(1)
        to_task = match.group(2)
        graph.add_edge(from_task, to_task)
    
    for match in re.finditer(depends_pattern, content):
        from_task = match.group(1)
        deps_str = match.group(2)
        deps = [d.strip() for d in deps_str.split(',')]
        for dep in deps:
            dep_match = re.search(r'TASK-\d+', dep)
            if dep_match:
                graph.add_edge(from_task, dep_match.group(0))
    
    return graph


def format_cycle(cycle: List[str]) -> str:
    """Format a cycle for display"""
    return ' → '.join(cycle)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    
    filepath = sys.argv[1]
    
    print("🔍 Checking for circular dependencies...")
    print()
    
    graph = parse_dependencies_md(filepath)
    
    if not graph.all_tasks:
        print("⚠️  No task dependencies found in file")
        print("   This may be normal if dependencies haven't been defined yet")
        sys.exit(0)
    
    print(f"Found {len(graph.all_tasks)} unique tasks")
    print(f"Analyzing dependency graph...")
    print()
    
    cycles = graph.find_cycles()
    
    if cycles:
        print(f"❌ Found {len(cycles)} circular dependency cycle(s):")
        print()
        
        for i, cycle in enumerate(cycles, 1):
            print(f"  Cycle {i}:")
            print(f"    {format_cycle(cycle)}")
            print()
        
        print("Circular dependencies must be resolved before implementation.")
        print("Review the dependency graph and break the cycles.")
        sys.exit(1)
    else:
        print("✅ No circular dependencies detected")
        print()
        print("Dependency graph is valid (forms a DAG)")
        sys.exit(0)


if __name__ == "__main__":
    main()
