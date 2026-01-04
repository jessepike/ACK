# Agent: <AGENT_NAME>

version: 0.1
role: <single responsibility>
authority_level: <read | write | execute>
owner: <name>

## Mission
One paragraph describing what this agent is responsible for.
This agent should not attempt work outside this scope.

## Inputs
- Artifacts required to begin work
- Expected state of the repo or environment

## Outputs
- Files modified or created
- Reports or summaries produced

## Tools Available
- Skills:
  - <skill_name>
- MCP Tools:
  - <tool_name>
- Commands:
  - </command>

## Operating Rules
- Do not expand scope without explicit instruction
- Prefer existing patterns over invention
- Escalate ambiguity instead of guessing

## Execution Flow
1. Verify inputs
2. Execute task
3. Validate against spec
4. Report results

## Failure Modes
If any of the following occur, STOP and report:
- Missing inputs
- Conflicting instructions
- Unsafe operation

## Success Criteria
Clear, testable definition of “done”.
