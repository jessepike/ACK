# IPE Validation Scripts

**Purpose:** Automated validation and quality checks for IPE projects  
**Location:** `./scripts/` in your project root  
**Language:** Bash + Python 3

---

## Installation

```bash
# Copy scripts to your project
cp -r scripts/ /path/to/your/project/

# Make executable
chmod +x scripts/*.sh scripts/*.py

# Test
./scripts/validate-ipe.sh --help
```

---

## Scripts Overview

| Script | Purpose | Language | When to Run |
|--------|---------|----------|-------------|
| `validate-ipe.sh` | Complete IPE validation | Bash | Before implementation |
| `check-cycles.py` | Detect circular dependencies | Python | Stage 5 completion |
| `validate-tasks.py` | Validate task completeness | Python | Stage 5 completion |
| `coverage-check.py` | Requirement coverage | Python | Stage 5 completion |
| `trace-requirements.py` | Full traceability report | Python | Audit/documentation |
| `check-token-budget.py` | CLAUDE.md size check | Python | Stage 4 completion |

---

## validate-ipe.sh

**Main validation script** - validates entire IPE project or specific stages.

### Usage

```bash
# Validate entire IPE
./scripts/validate-ipe.sh

# Validate specific stage
./scripts/validate-ipe.sh --stage 3

# Verbose output
./scripts/validate-ipe.sh --verbose

# Dry run (show what would be checked)
./scripts/validate-ipe.sh --dry-run
```

### What It Checks

**Stage 1 (Discovery):**
- All required artifacts exist
- All artifacts finalized
- Minimum stakeholder count (3+)
- Minimum requirement count (5+)

**Stage 2 (Solution Design):**
- All required artifacts exist
- All artifacts finalized
- Stack selections documented

**Stage 3 (Environment Setup):**
- All required artifacts exist
- All artifacts finalized
- Repository structure created
- Environment manifest valid

**Stage 4 (Workflow Configuration):**
- Governed artifacts finalized
- Continuous artifacts exist
- CLAUDE.md generated and valid
- Hooks configured
- Hook scripts present

**Stage 5 (Implementation Planning):**
- All artifacts locked
- Tasks have required fields (delegates to validate-tasks.py)
- No circular dependencies (delegates to check-cycles.py)

**Cross-Stage:**
- Requirement coverage (delegates to coverage-check.py)
- CLAUDE.md token budget (delegates to check-token-budget.py)
- Import references valid

### Example Output

```
═══════════════════════════════════════════════════════════════
  IPE Validation Report
═══════════════════════════════════════════════════════════════

Project: risk-tools
Date: 2025-01-02 15:30:00 UTC

Stage 1: Discovery
─────────────────────────────────────────────────────────────────
✓ Discovery directory exists
✓ discovery-synthesis.md is finalized
✓ stakeholders.md is finalized
✓ requirements.md is finalized
✓ constraints.md is finalized
✓ success-criteria.md is finalized
✓ Found 5 stakeholders (minimum 3)
✓ Found 12 requirements (minimum 5)

...

═══════════════════════════════════════════════════════════════
  Validation Summary
═══════════════════════════════════════════════════════════════

Total Checks:   47
Passed:         45
Failed:         0
Warnings:       2

✅ ALL VALIDATIONS PASSED

IPE project is ready for implementation

Next: Start TASK-001
```

---

## check-cycles.py

**Detects circular dependencies** in task dependency graph.

### Usage

```bash
python3 scripts/check-cycles.py .ipe/implementation/dependencies.md
```

### What It Does

- Parses dependency matrix from dependencies.md
- Builds directed graph
- Runs cycle detection algorithm (DFS)
- Reports any circular dependencies found

### Example Output

**No cycles:**
```
🔍 Checking for circular dependencies...

Found 20 unique tasks
Analyzing dependency graph...

✅ No circular dependencies detected

Dependency graph is valid (forms a DAG)
```

**Cycles found:**
```
🔍 Checking for circular dependencies...

Found 20 unique tasks
Analyzing dependency graph...

❌ Found 1 circular dependency cycle(s):

  Cycle 1:
    TASK-006 → TASK-010 → TASK-011 → TASK-006

Circular dependencies must be resolved before implementation.
Review the dependency graph and break the cycles.
```

---

## validate-tasks.py

**Validates task completeness** - ensures all tasks have required fields.

### Usage

```bash
python3 scripts/validate-tasks.py .ipe/implementation/tasks.md
```

### What It Checks

**For each task:**
- Has unique ID
- Has title, phase, milestone
- Has valid status
- Has complexity rating
- Has domain tags
- Has description
- Has acceptance criteria (3+ recommended)
- Dependencies reference valid tasks

**Overall:**
- No duplicate task IDs
- Task IDs are sequential
- No gaps in numbering

### Example Output

**All valid:**
```
🔍 Validating tasks.md...

Found 20 tasks

✅ All 20 tasks valid
```

**Errors found:**
```
🔍 Validating tasks.md...

Found 20 tasks

❌ Task Validation Errors:

  TASK-006:
    - Missing acceptance criteria
    - Invalid dependency: TASK-999 (task does not exist)

  TASK-010:
    - Missing complexity

❌ 2 task(s) have errors

Fix the errors above before proceeding
```

---

## coverage-check.py

**Verifies requirement coverage** - ensures all requirements have corresponding tasks.

### Usage

```bash
python3 scripts/coverage-check.py
```

### What It Checks

- Every requirement from Stage 1 is referenced in:
  - Architecture (Stage 2)
  - Tasks (Stage 5)

### Example Output

```
🔍 Checking requirement coverage...

Found 12 requirements

Checking architecture coverage...
Checking task coverage...

═══════════════════════════════════════════════════════════════
  Requirement Traceability Report
═══════════════════════════════════════════════════════════════

✅ Fully Covered (10 requirements):

  R-001: User authentication
    → Tasks: TASK-006, TASK-007, TASK-008

  R-002: Project management
    → Tasks: TASK-009, TASK-010, TASK-011

  ...

⚠️  Partially Covered (2 requirements):

  R-005: Email notifications
    ✓ Architecture coverage
    ✗ No tasks identified

═══════════════════════════════════════════════════════════════
  Summary
═══════════════════════════════════════════════════════════════

Total Requirements:   12
Fully Covered:        10 (83.3%)
Partially Covered:    2
Not Covered:          0
```

---

## trace-requirements.py

**Full traceability report** - shows requirement → architecture → tasks path.

### Usage

```bash
# Text output
python3 scripts/trace-requirements.py

# JSON output
python3 scripts/trace-requirements.py --format json > trace.json

# CSV output
python3 scripts/trace-requirements.py --format csv > trace.csv
```

### What It Produces

Complete trace from requirements through design to implementation.

### Example Output

```
═══════════════════════════════════════════════════════════════
  Requirement Traceability Matrix
═══════════════════════════════════════════════════════════════

✅ Fully Traced (10):

R-001: User authentication
  → Architecture: Authentication Service
  → Stack: FastAPI + JWT
  → Data Model: User model
  → Tasks: TASK-006, TASK-007, TASK-008

R-002: Project management
  → Architecture: Project Service
  → Stack: PostgreSQL + SQLAlchemy
  → Data Model: Project model
  → Tasks: TASK-009, TASK-010, TASK-011

...
```

**JSON format** useful for CI/CD integration:
```json
{
  "total_requirements": 12,
  "fully_traced": 10,
  "partially_traced": 2,
  "not_traced": 0,
  "traces": [
    {
      "requirement_id": "R-001",
      "requirement_title": "User authentication",
      "architecture_refs": ["Authentication Service"],
      "stack_refs": ["FastAPI + JWT"],
      "task_refs": ["TASK-006", "TASK-007", "TASK-008"],
      "fully_traced": true
    }
  ]
}
```

---

## check-token-budget.py

**Validates CLAUDE.md size** - ensures context stays within limits.

### Usage

```bash
# Check default location
python3 scripts/check-token-budget.py

# Check specific file
python3 scripts/check-token-budget.py /path/to/CLAUDE.md
```

### What It Checks

- Core CLAUDE.md token count
- Each import file token count
- Total tokens (core + imports)
- Compares against budgets:
  - Target: 20,000 tokens (~80 KB)
  - Warning: 30,000 tokens (~120 KB)
  - Maximum: 50,000 tokens (~200 KB)

### Example Output

```
🔍 Checking CLAUDE.md token budget...

═══════════════════════════════════════════════════════════════
  CLAUDE.md Token Budget Analysis
═══════════════════════════════════════════════════════════════

Core CLAUDE.md:      3,200 tokens (12.5 KB)

Imports (5 files):

  .ipe/discovery/requirements.md
    2,100 tokens (8.2 KB)

  .ipe/solution-design/architecture.md
    3,800 tokens (14.8 KB)

  .ipe/implementation/tasks.md
    8,400 tokens (32.8 KB)

  ...

Total Imports:       18,200 tokens

─────────────────────────────────────────────────────────────────
TOTAL:               21,400 tokens (83.6 KB)

─────────────────────────────────────────────────────────────────
Budget Targets:

  Target:   20,000 tokens  (78.1 KB)
  Warning:  30,000 tokens  (117.2 KB)
  Maximum:  50,000 tokens  (195.3 KB)

⚠️  Exceeds target, within warning threshold
   Using 71.3% of warning budget

   Recommendation: Consider pruning or moving content to optional imports

─────────────────────────────────────────────────────────────────
Optimization Suggestions:

  Largest imports to consider moving to optional:
    - .ipe/implementation/tasks.md (8,400 tokens)
    - .ipe/solution-design/architecture.md (3,800 tokens)

  To make import optional, comment it out in CLAUDE.md:
    # @.ipe/verbose-artifact.md  # Optional, load on demand
```

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: IPE Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Make scripts executable
        run: chmod +x scripts/*.sh scripts/*.py
      
      - name: Validate IPE
        run: ./scripts/validate-ipe.sh --verbose
      
      - name: Generate Trace Report
        if: success()
        run: |
          python3 scripts/trace-requirements.py --format json > trace.json
          python3 scripts/trace-requirements.py --format csv > trace.csv
      
      - name: Upload Artifacts
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: validation-reports
          path: |
            trace.json
            trace.csv
```

---

## Common Workflows

### Before Starting Implementation

```bash
# Full validation
./scripts/validate-ipe.sh --verbose

# If passes, you're ready for TASK-001
```

### After Creating Stage 5 Plan

```bash
# Validate tasks
python3 scripts/validate-tasks.py .ipe/implementation/tasks.md

# Check dependencies
python3 scripts/check-cycles.py .ipe/implementation/dependencies.md

# Verify coverage
python3 scripts/coverage-check.py
```

### Periodic Health Checks

```bash
# Weekly: Check token budget
python3 scripts/check-token-budget.py

# Before each stage transition
./scripts/validate-ipe.sh --stage N
```

### Generating Reports

```bash
# For documentation/audit
python3 scripts/trace-requirements.py > docs/traceability-report.txt

# For tool integration
python3 scripts/trace-requirements.py --format json > reports/trace.json
```

---

## Troubleshooting

### Script Not Found

```bash
# Make sure you're in project root
cd /path/to/project

# Check scripts exist
ls -la scripts/

# Make executable
chmod +x scripts/*.sh scripts/*.py
```

### Python Import Errors

```bash
# Scripts use only standard library
# Requires Python 3.7+
python3 --version

# No pip install needed
```

### Permission Denied

```bash
# Make scripts executable
chmod +x scripts/*.sh scripts/*.py

# Or run explicitly
bash scripts/validate-ipe.sh
python3 scripts/check-cycles.py
```

### Validation Failures

```bash
# Run with verbose for details
./scripts/validate-ipe.sh --verbose

# Run specific validations
python3 scripts/validate-tasks.py .ipe/implementation/tasks.md
python3 scripts/check-cycles.py .ipe/implementation/dependencies.md

# Check from correct directory
pwd  # Should be project root
```

---

## Dependencies

**Bash scripts:**
- Bash 4.0+
- Standard Unix tools (grep, sed, awk)
- jq (for JSON parsing) - optional, used for settings.json validation

**Python scripts:**
- Python 3.7+
- Standard library only (no pip install required)

**Install jq (optional):**
```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# Fedora
sudo dnf install jq
```

---

## Exit Codes

All scripts use consistent exit codes:

| Code | Meaning |
|------|---------|
| 0 | Success - validation passed |
| 1 | Validation failed - errors found |
| 2 | Script error - invalid usage or file not found |

**Use in automation:**
```bash
if ./scripts/validate-ipe.sh; then
    echo "Ready for implementation"
    ./start-implementation.sh
else
    echo "Fix validation errors first"
    exit 1
fi
```

---

## Contributing

### Adding New Validations

1. Add check to `validate-ipe.sh` or create new Python script
2. Follow existing patterns for output formatting
3. Use consistent exit codes
4. Update this README
5. Add tests/examples

### Output Format Standards

**Success:** Green ✓  
**Failure:** Red ✗  
**Warning:** Yellow ⚠️  
**Info:** Blue ℹ️  

**Use ANSI colors** for terminal output  
**Provide JSON option** for tool integration

---

## Version History

**1.0.0** - Initial release
- Complete IPE validation (all 5 stages)
- Cycle detection
- Task validation
- Coverage checking
- Traceability reporting
- Token budget validation
