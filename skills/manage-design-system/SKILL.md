# manage-design-system

## Description
A skill for managing the design system in Stitch MCP server projects.

## Upload DESIGN.md

### Option B: From installed plugin (use variable)
When the plugin is installed through the marketplace, use the `CLAUDE_PLUGIN_ROOT` environment variable or a path relative to the skill:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/upload-to-stitch/scripts/upload_to_stitch.py
```
or
```bash
python3 skills/upload-to-stitch/scripts/upload_to_stitch.py
```

> **Note**: The original example used a path relative to the repository checkout, which fails from any project cwd when the plugin is installed via the marketplace. Use `${CLAUDE_PLUGIN_ROOT}` or a skill-relative path instead.

## Tags
- design-system
- stitch
- mcp

## Commands
### Upload DESIGN.md
Upload a DESIGN.md file to the Stitch MCP server.
### List Design Assets
List existing design assets on the server.
