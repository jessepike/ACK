# Claude Code Support Harness Architecture

## Objective
Provide durable context, governance, and execution control for AI-assisted development.

## Layers

### 1. Skill Layer
Encodes repeatable knowledge and workflows.
Reduces prompt entropy.

### 2. Agent Layer
Specialized, isolated workers.
Enables parallelism and responsibility boundaries.

### 3. Tool Layer (MCP)
Bridges Claude to real systems.
Strictly governed.

### 4. Plugin Layer
Distribution and environment consistency.

## Design Principles
- Explicit over implicit
- Small, composable units
- Drift detection over trust
- Humans and agents governed equally

## Common Failure Modes
- Overloaded skills
- Agents with vague scope
- Tools without auditability

## Maturity Path
Phase 1: Manual orchestration
Phase 2: Semi-automated agent chains
Phase 3: Policy-driven execution gates
