# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

design-system-upload-path

## Roadmap

### skill-naming-convention — Fix skill name colon to hyphen convention

Status: done

Acceptance:
- Skill names in SKILL.md files use only letters, numbers, hyphens, underscores, dots, and spaces
- No skill names contain colons that would fail validation by co-pilot CLI or similar tools

Implementation: `skills/react-components/SKILL.md`, `skills/manage-design-system/SKILL.md`, `skills/extract-design-md/SKILL.md`, `skills/upload-to-stitch/SKILL.md`

Tests: `tests/skill_naming_test.py`

### design-system-upload-path — Fix upload path to use variable instead of relative path

Status: done

Acceptance:
- SKILL.md uses ${CLAUDE_PLUGIN_ROOT} (or a skill-relative path) for the upload command
- Referenced upload script path resolves to a real file in the checkout
- Commands work both from repo checkout and when plugin installed via marketplace

Implementation: `skills/manage-design-system/SKILL.md`

Tests: `tests/upload_path_test.py`

### design-md-live-url — Add live URL input mode to extract-design-md skill

Status: planned

Acceptance:
- SKILL.md includes optional From a live URL section using Firecrawl API
- Firecrawl branding/screenshot formats map to DESIGN.md sections
- Source-code path remains default; Firecrawl optional

Implementation: `skills/extract-design-md/SKILL.md`

### schema-defs — Add $defs to outputSchema in upload_design_md

Status: planned

Acceptance:
- outputSchema references resolvable $defs
- ScreenInstance schema defined within schema

Implementation: `skills/upload-to-stitch/scripts/upload_to_stitch.py`

---

Alan Vo · [alanvo.net](https://alanvo.net) · [X: @alanvoasi](https://x.com/alanvoasi)
