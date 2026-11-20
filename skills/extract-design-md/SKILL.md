# extract-design-md

## Description
A skill for extracting design metadata from frontend code and live URLs to generate DESIGN.md files for Stitch MCP server projects.

## Input Modes

### Phase 1: Source Code (Default)
Reads frontend source code from the local repository to extract design metadata including colors, fonts, typography, spacing, and component styles.

### Phase 1: From a Live URL (Optional)
> **Prerequisite**: A Firecrawl API key is required for this mode. Set the `FIRECRAWL_API_KEY` environment variable.

To extract design metadata from a live URL instead of source code, use the Firecrawl API:

```bash
curl -s -X POST https://api.firecrawl.dev/v2/scrape \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","formats":["branding","screenshot"],"origin":"stitch-skills"}'
```

**Branding Fields Mapped to DESIGN.md:**

| Firecrawl Field | DESIGN.md Frontmatter Key | Description |
|---|---|---|
| `colorScheme` | `colorScheme` | Light or dark color scheme |
| `colors.primary` | `colors.primary` | Primary brand color |
| `colors.secondary` | `colors.secondary` | Secondary brand color |
| `colors.background` | `colors.background` | Background color |
| `colors.textPrimary` | `colors.textPrimary` | Primary text color |
| `colors.link` | `colors.link` | Link color |
| `fonts[].family` | `fonts` | Font families with roles |
| `typography.fontSizes` | `typography.fontSizes` | Heading and body font sizes |
| `spacing.baseUnit` | `spacing.baseUnit` | Base unit for spacing |
| `spacing.borderRadius` | `spacing.borderRadius` | Border radius values |
| `components.buttonPrimary` | `components.buttonPrimary` | Button style definitions |
| `brandName` | `brandName` | Brand/website name |

The response also includes logo, favicon, and OG image URLs, plus a screenshot URL (`data.screenshot`) for writing the atmosphere paragraph.

### Phase 2: Mapping
Maps the extracted branding fields onto the same DESIGN.md sections and YAML frontmatter regardless of input source (source code or live URL).

### Phase 3: Atmosphere
Reads the screenshot to write the atmosphere paragraph describing the overall look and feel.

## Tags
- design-md
- firecrawl
- stitch
- mcp

## Commands
### Extract from Source Code
Extract design metadata from local frontend source code (default mode).

### Extract from Live URL
Extract design metadata from a live URL using Firecrawl API.
  ```bash
  # Requires FIRECRAWL_API_KEY environment variable
  python3 skills/extract-design-md/scripts/extract_from_url.py https://example.com
  ```
### Generate DESIGN.md
Generate a complete DESIGN.md file from extracted metadata.
