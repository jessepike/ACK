# IPE Complete Validation Checklist

**Purpose:** Ensure IPE project is ready for implementation  
**Run:** Before starting TASK-001  
**Script:** `./scripts/validate-ipe.sh`

---

## Quick Validation

```bash
# Run complete validation
./scripts/validate-ipe.sh

# Run specific stage validation
./scripts/validate-ipe.sh --stage 4

# Dry run (show what would be checked)
./scripts/validate-ipe.sh --dry-run

# Verbose output
./scripts/validate-ipe.sh --verbose
```

---

## Stage 1: Discovery Validation

### Required Artifacts

- [ ] `.ipe/discovery/discovery-synthesis.md` exists
- [ ] `.ipe/discovery/stakeholders.md` exists
- [ ] `.ipe/discovery/requirements.md` exists
- [ ] `.ipe/discovery/constraints.md` exists
- [ ] `.ipe/discovery/success-criteria.md` exists

### Status Checks

- [ ] All artifacts have `status: finalized`
- [ ] All artifacts have proper frontmatter
- [ ] All artifacts reference each other correctly

### Content Validation

- [ ] At least 3 stakeholders identified
- [ ] At least 5 requirements documented
- [ ] At least 3 constraints listed
- [ ] Success criteria are measurable

### Automated Checks

```bash
# Check all required files exist
test -f .ipe/discovery/discovery-synthesis.md
test -f .ipe/discovery/stakeholders.md
test -f .ipe/discovery/requirements.md
test -f .ipe/discovery/constraints.md
test -f .ipe/discovery/success-criteria.md

# Verify all finalized
grep -q "status: finalized" .ipe/discovery/*.md
```

---

## Stage 2: Solution Design Validation

### Required Artifacts

- [ ] `.ipe/solution-design/architecture.md` exists
- [ ] `.ipe/solution-design/stack.md` exists
- [ ] `.ipe/solution-design/data-model.md` exists
- [ ] `.ipe/solution-design/design-decisions.md` exists

### Status Checks

- [ ] All artifacts have `status: finalized`
- [ ] All design decisions have rationale
- [ ] Stack selections justified

### Content Validation

- [ ] Architecture addresses all requirements
- [ ] Stack is compatible (no conflicts)
- [ ] Data model is normalized
- [ ] API design follows conventions (if applicable)

### Cross-Stage Validation

- [ ] All requirements from Stage 1 addressed
- [ ] All constraints from Stage 1 respected
- [ ] Success criteria achievable with design

### Automated Checks

```bash
# Check required files
test -f .ipe/solution-design/architecture.md
test -f .ipe/solution-design/stack.md
test -f .ipe/solution-design/data-model.md

# Verify cross-references
grep -r "requirements.md" .ipe/solution-design/
```

---

## Stage 3: Environment Setup Validation

### Required Artifacts

- [ ] `.ipe/environment-setup/repo-structure.md` exists and finalized
- [ ] `.ipe/environment-setup/environment-config.md` exists and finalized
- [ ] `.ipe/environment-setup/setup-guide.md` exists and finalized
- [ ] `.ipe/environment-setup/environment-manifest.json` exists

### Repository Structure

- [ ] `src/` directory exists
- [ ] `tests/` directory exists
- [ ] `docs/` directory exists (if applicable)
- [ ] `.gitignore` configured
- [ ] `README.md` exists

### Environment Validation

- [ ] All tools from stack.md are installed
- [ ] All versions match environment-manifest.json
- [ ] Basic tests can run
- [ ] Development server can start

### Automated Checks

```bash
# Check repository structure
test -d src
test -d tests
test -f .gitignore
test -f README.md

# Verify tools installed
python --version
pip --version
# (Check all tools from manifest)

# Run basic tests
pytest --version
```

---

## Stage 4: Workflow Configuration Validation

### Required Artifacts (Governed)

- [ ] `.ipe/workflow-config/dev-workflow.md` finalized
- [ ] `.ipe/workflow-config/environment-variants.md` finalized
- [ ] `.ipe/workflow-config/context-management.md` finalized
- [ ] `.ipe/workflow-config/claude-config.md` finalized

### Required Artifacts (Continuous)

- [ ] `.claude/claude.md` exists and populated
- [ ] `.agent/agent.md` exists and populated
- [ ] `.ipe/workflow-config/operations-playbook.md` exists

### Generated Artifacts

- [ ] `.claude/CLAUDE.md` exists
- [ ] `.claude/CLAUDE.md` is valid (passes validation)
- [ ] `.claude/settings.json` exists
- [ ] `.claude/settings.json` has hooks configured

### Hook Validation

- [ ] All 6 hook scripts exist
- [ ] All hooks are executable
- [ ] Hook configuration in settings.json is valid
- [ ] Test hook execution succeeds

### CLAUDE.md Validation

- [ ] Required sections present
- [ ] Token budget under 20,000 (~5,000 chars/file)
- [ ] All imports reference existing files
- [ ] No syntax errors

### Automated Checks

```bash
# Check governed artifacts finalized
grep "status: finalized" .ipe/workflow-config/dev-workflow.md
grep "status: finalized" .ipe/workflow-config/environment-variants.md
grep "status: finalized" .ipe/workflow-config/context-management.md
grep "status: finalized" .ipe/workflow-config/claude-config.md

# Verify CLAUDE.md exists and valid
test -f .claude/CLAUDE.md
./.claude/hooks/validate-claude-md.sh

# Check hooks configured
jq .hooks .claude/settings.json >/dev/null

# Test hooks
./.claude/hooks/test-hooks.sh
```

---

## Stage 5: Implementation Planning Validation

### Required Artifacts (All Locked)

- [ ] `.ipe/implementation/phases.md` status: locked
- [ ] `.ipe/implementation/tasks.md` status: locked
- [ ] `.ipe/implementation/dependencies.md` status: locked
- [ ] `.ipe/implementation/effort-estimates.md` status: locked
- [ ] `.ipe/implementation/skills-and-agents.md` status: locked

### Tasks Validation

- [ ] All tasks have unique IDs (TASK-XXX)
- [ ] All tasks have acceptance criteria
- [ ] All tasks have complexity ratings
- [ ] All tasks reference dependencies
- [ ] No task is missing required fields

### Dependencies Validation

- [ ] Dependency graph has no cycles
- [ ] All referenced tasks exist
- [ ] Critical path identified
- [ ] Parallelization opportunities noted

### Estimates Validation

- [ ] All tasks have effort estimates
- [ ] Total estimates are reasonable
- [ ] Complexity aligns with estimates
- [ ] Risk factors documented

### Skills Validation

- [ ] All required skills identified
- [ ] Skills are available or creation plan exists
- [ ] Skills map to specific tasks
- [ ] No task lacks execution strategy

### Coverage Validation

- [ ] All features from solution design have tasks
- [ ] All requirements from discovery have tasks
- [ ] All architecture components have tasks

### Automated Checks

```bash
# Check all artifacts locked
grep "status: locked" .ipe/implementation/*.md

# Validate dependencies (no cycles)
python scripts/check-cycles.py .ipe/implementation/dependencies.md

# Check all tasks have criteria
python scripts/validate-tasks.py .ipe/implementation/tasks.md

# Verify coverage
python scripts/coverage-check.py
```

---

## Cross-Stage Validation

### Requirement Traceability

```bash
# Every requirement from Stage 1 has:
# - Architecture component in Stage 2
# - Task(s) in Stage 5

python scripts/trace-requirements.py
```

**Expected Output:**
```
Requirement Traceability Report
================================

R-001: User authentication
  → Architecture: Authentication Service (architecture.md)
  → Stack: FastAPI + JWT (stack.md)
  → Tasks: TASK-006, TASK-007, TASK-008
  ✓ Fully traced

R-002: Project management
  → Architecture: Project Service (architecture.md)
  → Stack: PostgreSQL + SQLAlchemy (stack.md)
  → Tasks: TASK-009, TASK-010, TASK-011
  ✓ Fully traced

Summary: 12/12 requirements traced (100%)
```

### Artifact Cross-References

```bash
# Validate all @references point to existing files
python scripts/validate-references.py
```

**Checks:**
- All `@.ipe/...` references in CLAUDE.md exist
- All `[link](../path)` references resolve
- No broken cross-stage references

### Token Budget

```bash
# Ensure CLAUDE.md + imports under budget
python scripts/check-token-budget.py
```

**Target:** <20,000 tokens total (~5,000 chars/file)  
**Maximum:** <50,000 tokens

---

## Pre-Implementation Checklist

### Before Starting TASK-001

**Complete IPE:**
- [ ] All 5 stages complete
- [ ] All artifacts finalized/locked as appropriate
- [ ] All validations passing

**Environment Ready:**
- [ ] Repository structure correct
- [ ] All tools installed and working
- [ ] Tests can run
- [ ] Development server starts

**Workflows Defined:**
- [ ] Git workflow documented
- [ ] PR process defined
- [ ] Deployment process ready

**Agent Configured:**
- [ ] CLAUDE.md generated and valid
- [ ] claude.md has behavior rules
- [ ] agent.md configured
- [ ] Hooks installed and tested

**Implementation Plan Ready:**
- [ ] All tasks defined with criteria
- [ ] Dependencies mapped
- [ ] Estimates complete
- [ ] Skills available

**Human Approval:**
- [ ] Discovery approved
- [ ] Design approved
- [ ] Environment verified
- [ ] Workflows reviewed
- [ ] Implementation plan signed off

---

## Validation Script Specification

### Script: validate-ipe.sh

**Location:** `./scripts/validate-ipe.sh`

**Usage:**
```bash
./scripts/validate-ipe.sh [options]

Options:
  --stage N       Validate only stage N (1-5)
  --dry-run       Show what would be checked
  --verbose       Detailed output
  --json          Output as JSON
  --fix           Auto-fix simple issues
  --help          Show this help

Exit codes:
  0 - All validations passed
  1 - Validation failures found
  2 - Script error
```

**Implementation:**
```bash
#!/bin/bash
# validate-ipe.sh

set -euo pipefail

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERBOSE=false
DRY_RUN=false
STAGE=""

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --stage)
      STAGE="$2"
      shift 2
      ;;
    --verbose)
      VERBOSE=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --help)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 2
      ;;
  esac
done

# Validation functions
validate_stage_1() {
  echo "Validating Stage 1: Discovery..."
  
  # Check required files
  required_files=(
    ".ipe/discovery/discovery-synthesis.md"
    ".ipe/discovery/stakeholders.md"
    ".ipe/discovery/requirements.md"
    ".ipe/discovery/constraints.md"
    ".ipe/discovery/success-criteria.md"
  )
  
  for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
      echo -e "${RED}✗ Missing: $file${NC}"
      return 1
    fi
    
    if ! grep -q "status: finalized" "$file"; then
      echo -e "${YELLOW}⚠ Not finalized: $file${NC}"
      return 1
    fi
  done
  
  echo -e "${GREEN}✓ Stage 1 validation passed${NC}"
  return 0
}

# ... (similar functions for stages 2-5)

# Main validation
main() {
  echo "IPE Validation Report"
  echo "===================="
  echo ""
  
  if [ -n "$STAGE" ]; then
    validate_stage_$STAGE
  else
    validate_stage_1 && \
    validate_stage_2 && \
    validate_stage_3 && \
    validate_stage_4 && \
    validate_stage_5
  fi
  
  if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ ALL VALIDATIONS PASSED${NC}"
    echo "IPE is ready for implementation"
    echo ""
    echo "Next: Start TASK-001"
    exit 0
  else
    echo ""
    echo -e "${RED}✗ VALIDATION FAILED${NC}"
    echo "Fix issues above before proceeding"
    exit 1
  fi
}

main
```

---

## Python Validation Helpers

### check-cycles.py

**Purpose:** Detect circular dependencies in tasks

```python
#!/usr/bin/env python3
"""Check for circular dependencies in task graph"""

import sys
import re
from typing import Dict, Set, List

def parse_dependencies(filepath: str) -> Dict[str, List[str]]:
    """Parse dependencies.md and extract task graph"""
    # Implementation
    pass

def find_cycles(graph: Dict[str, List[str]]) -> List[List[str]]:
    """Detect cycles in directed graph using DFS"""
    # Implementation
    pass

def main():
    if len(sys.argv) != 2:
        print("Usage: check-cycles.py <dependencies.md>")
        sys.exit(2)
    
    graph = parse_dependencies(sys.argv[1])
    cycles = find_cycles(graph)
    
    if cycles:
        print("❌ Circular dependencies found:")
        for cycle in cycles:
            print(f"  {' → '.join(cycle)}")
        sys.exit(1)
    else:
        print("✅ No circular dependencies")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

### validate-tasks.py

**Purpose:** Ensure all tasks have required fields

```python
#!/usr/bin/env python3
"""Validate tasks.md structure and completeness"""

import sys
import re
from typing import List, Dict

def parse_tasks(filepath: str) -> List[Dict]:
    """Parse tasks.md and extract all tasks"""
    # Implementation
    pass

def validate_task(task: Dict) -> List[str]:
    """Validate single task has all required fields"""
    errors = []
    
    required_fields = [
        'title', 'phase', 'milestone', 'status',
        'complexity', 'domain', 'dependencies',
        'description', 'acceptance_criteria'
    ]
    
    for field in required_fields:
        if field not in task:
            errors.append(f"Missing field: {field}")
    
    # Check acceptance criteria not empty
    if 'acceptance_criteria' in task and not task['acceptance_criteria']:
        errors.append("Acceptance criteria is empty")
    
    return errors

def main():
    if len(sys.argv) != 2:
        print("Usage: validate-tasks.py <tasks.md>")
        sys.exit(2)
    
    tasks = parse_tasks(sys.argv[1])
    all_valid = True
    
    for task in tasks:
        errors = validate_task(task)
        if errors:
            print(f"❌ {task['id']}: {task.get('title', 'Unknown')}")
            for error in errors:
                print(f"   - {error}")
            all_valid = False
    
    if all_valid:
        print(f"✅ All {len(tasks)} tasks valid")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### coverage-check.py

**Purpose:** Verify all requirements have corresponding tasks

```python
#!/usr/bin/env python3
"""Check requirement coverage in implementation plan"""

import sys
from typing import Dict, List, Set

def extract_requirements(requirements_md: str) -> Dict[str, str]:
    """Extract all requirements from requirements.md"""
    # Implementation
    pass

def extract_task_refs(tasks_md: str) -> Set[str]:
    """Extract requirement references from tasks.md"""
    # Implementation
    pass

def main():
    requirements = extract_requirements('.ipe/discovery/requirements.md')
    task_refs = extract_task_refs('.ipe/implementation/tasks.md')
    
    uncovered = set(requirements.keys()) - task_refs
    
    if uncovered:
        print(f"❌ {len(uncovered)} requirements not covered:")
        for req_id in uncovered:
            print(f"   {req_id}: {requirements[req_id]}")
        sys.exit(1)
    else:
        print(f"✅ All {len(requirements)} requirements covered")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## Summary

**Complete validation requires:**
1. All stage artifacts present and properly marked
2. Cross-stage references valid
3. No circular dependencies
4. All requirements traced to tasks
5. CLAUDE.md valid and under token budget
6. Hooks configured and tested
7. Environment functional

**Run before implementation:**
```bash
./scripts/validate-ipe.sh --verbose

# If all pass:
✅ ALL VALIDATIONS PASSED
IPE is ready for implementation

Next: Start TASK-001
```
