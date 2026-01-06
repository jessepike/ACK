# URL Insight Extraction Prompt

Analyze the content at `{{SOURCE}}` and extract actionable insights for the ACK project (AI-assisted development toolkit with memory, governance, and registry components).

## Extract & Categorize

For each insight found, provide:

1. **Category**: `tool` | `workflow` | `pattern` | `technique` | `integration` | `architecture`
2. **Title**: Brief name (5 words max)
3. **Description**: What it is and how it works (2-3 sentences)
4. **Application**: Specific way to apply this to ACK (be concrete)
5. **Effort**: `low` | `medium` | `high`
6. **Impact**: `low` | `medium` | `high`

## Prioritization Criteria

Focus on insights that:
- Reduce friction in AI-assisted development workflows
- Improve context/memory management for AI coding assistants
- Enhance artifact governance or validation
- Streamline project scaffolding or templates
- Enable better human-AI collaboration patterns

## Constraints

- Maximum 7 insights (quality over quantity)
- Skip generic advice—only include specific, implementable ideas
- Ignore content unrelated to development tooling, AI assistance, or project management
- Skip insights that duplicate existing backlog items (check first)
- If the source has no relevant insights, report "No new insights found"

## Action: Append to Backlog

After extraction, append insights to `/Users/jessepike/code/ack/tips.backlog.md` using this format:

**High Impact items** → add under `## High Priority` section
**Medium/Low Impact items** → add under `## Medium Priority` section

Entry format:
```markdown
### [CATEGORY] Title Here
- **Source**: {{SOURCE_NAME}}
- **Description**: Description here.
- **Application**: Application here.
- **Effort**: low | **Impact**: high
- **Status**: backlog
```

## Summary Output

After updating backlog, report:
- Number of insights added (high priority / medium priority)
- New backlog totals
- Source name added to backlog
