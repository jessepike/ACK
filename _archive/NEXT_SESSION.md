# Next Session — Claude Registry

## Status
**Sandbox/Development** — Not implemented in any live projects yet.

## Open Questions to Resolve

1. **What does `claude-mem` MCP do?** 
   - Showed as connected in your screenshot
   - Need to document purpose and config

2. **What does `project-studio` MCP do?**
   - Custom server you have
   - Need to document

3. **What does `claude-in-chrome` MCP do?**
   - Browser automation?
   - Need to document config and capabilities

4. **Do you want to contribute commands back to community repos?**
   - wshobson/commands, qdhenry/Claude-Command-Suite, etc.

## Files Pending Manual Copy

Download from this session and copy to registry:

```bash
cp ~/Downloads/pr.md ~/code/tools/claude-registry/commands/
cp ~/Downloads/branch.md ~/code/tools/claude-registry/commands/
cp ~/Downloads/review.md ~/code/tools/claude-registry/commands/
cp ~/Downloads/MCP_INVENTORY.md ~/code/tools/claude-registry/docs/
cp ~/Downloads/BUILTIN_COMMANDS_REFERENCE.md ~/code/tools/claude-registry/docs/
cp ~/Downloads/mcp-base.json ~/code/tools/claude-registry/templates/
```

## Suggested Next Steps

### Immediate
- [ ] Copy downloaded files to registry
- [ ] Test AGS validation: `python scripts/validate_ags.py`

### Short-term
- [ ] Add GitHub domain package (agent + skill + tool + commands)
- [ ] Add LangChain/LangGraph domain
- [ ] Create policies (code review rules, commit standards)
- [ ] Document claude-mem, project-studio, claude-in-chrome

### Medium-term
- [ ] Hook integration (AGS validation to pre-commit)
- [ ] Cross-project learning mechanism
- [ ] Plugin evaluation (package as Claude Code plugin?)

## Session Artifacts

Files created this session:
- 6 prompts (AGS frontmatter added)
- 6 commands (1 deprecated)
- 3 agents
- 3 skills
- 3 domain summaries
- MCP inventory with registries
- Built-in commands reference
- Updated mcp-base.json template

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| 6 primitive types | Agent, Skill, Tool, Command, Prompt, Policy |
| Tool = MCP + CLI + Script | Not just CLI specs |
| AGS frontmatter on all | `doc_id`, `tier`, `status`, `version`, `depends_on` |
| Domain packages | Complete vertical slices |
| Symlink model | Projects link to registry, don't copy |
| Deprecated /review | Built-in exists in Claude Code |
| Sandbox only | No live project integration until complete |
