# Skill: <SKILL_NAME>

version: 0.1
owner: <name>
status: active
scope: claude-code
last_updated: YYYY-MM-DD

## Purpose
Concise description of what this skill enables Claude to do consistently.
This skill exists to eliminate repeated prompting and reduce agent drift.

## When This Skill Applies
Claude should apply this skill when:
- <clear trigger condition>
- <stack / language / repo pattern>
- <workflow phase>

## When This Skill Does NOT Apply
Explicit exclusions to prevent overreach.

## Inputs
- Expected files
- Expected context (e.g., repo root, PR diff, test output)

## Outputs
- Artifacts produced (files, diffs, reports)
- Expected format and structure

## Required Behaviors
Claude MUST:
- <non-negotiable rule>
- <non-negotiable rule>

Claude MUST NOT:
- <explicit prohibition>

## Workflow
1. Step-by-step procedure Claude should follow
2. Include validation or sanity checks
3. Define stop conditions

## Examples
### Example 1: Typical Case
<short example>

### Example 2: Edge Case
<short example>

## Validation Checklist
- [ ] Output matches expected format
- [ ] No unauthorized files touched
- [ ] Errors surfaced explicitly

## Notes
Operational constraints, assumptions, or future improvements.
