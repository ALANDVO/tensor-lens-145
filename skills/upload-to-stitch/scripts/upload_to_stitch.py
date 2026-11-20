#!/usr/bin/env python3
"""Upload design data to Stitch MCP server."""

import json
import sys
import os

def upload_design_md(design_md_path: str) -> dict:
    """Upload a DESIGN.md file to the Stitch MCP server.
    
    Returns output schema with resolvable $defs.
    """
    # Read the DESIGN.md file
    with open(design_md_path, 'r') as f:
        content = f.read()
    
    # Parse the YAML frontmatter and design data
    # ... (implementation)
    
    # Build output schema with $defs
    output_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$defs": {
            "ScreenInstance": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "properties": {"type": "object"},
                    "styles": {"type": "object"},
                },
                "required": ["id", "name"],
            },
            "DesignSystem": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "colors": {"type": "object"},
                    "typography": {"type": "object"},
                    "spacing": {"type": "object"},
                },
                "required": ["name"],
            },
        },
        "type": "object",
        "required": ["$defs"],
    }
    
    return {"outputSchema": output_schema, "content": content}


def edit_screen(screen_id: str, dom_operations: list) -> dict:
    """Edit a screen on the Stitch MCP server.
    
    Note: This function returns success status but does NOT persist changes.
    The native Stitch web UI edit works; the programmatic path currently
    does not persist changes. See stitch-sdk#361 for the upstream issue.
    """
    # Note: edit_screens currently returns success + dom_operations
    # but never persists the change. Until the endpoint is fixed,
    # the skill's "edit existing screen" path won't work for agent/SDK users.
    
    result = {
        "success": True,
        "dom_operations": dom_operations,
        "persisted": False,
        "note": "Edit operation returned success but may not persist. "
                "See stitch-sdk#361 for upstream issue.",
    }
    
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 upload_to_stitch.py <command> [args...]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "upload_design_md":
        if len(sys.argv) < 3:
            print("Usage: python3 upload_to_stitch.py upload_design_md <design_md_path>")
            sys.exit(1)
        result = upload_design_md(sys.argv[2])
        print(json.dumps(result, indent=2))
    elif command == "edit_screen":
        if len(sys.argv) < 4:
            print("Usage: python3 upload_to_stitch.py edit_screen <screen_id> <dom_operations_json>")
            sys.exit(1)
        screen_id = sys.argv[2]
        dom_operations = json.loads(sys.argv[3])
        result = edit_screen(screen_id, dom_operations)
        print(json.dumps(result, indent=2))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
