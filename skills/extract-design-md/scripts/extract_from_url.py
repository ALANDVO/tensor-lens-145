#!/usr/bin/env python3
"""Extract design metadata from a live URL using Firecrawl API.

This script extracts branding, typography, spacing, and component styles
from a live website URL using the Firecrawl API. Requires a FIRECRAWL_API_KEY
environment variable to authenticate API requests.

The extracted data maps to DESIGN.md frontmatter sections for Stitch MCP projects.
"""

import json
import os
import sys
import requests


def extract_from_url(url: str, api_key: str = None) -> dict:
    """Extract design metadata from a live URL using Firecrawl API.

    Args:
        url: The website URL to extract design metadata from.
        api_key: Firecrawl API key. If not provided, reads from
                 FIRECRAWL_API_KEY environment variable.

    Returns:
        dict containing extracted design metadata with keys:
        - colorScheme: "light" or "dark"
        - colors: dict with primary, secondary, background, textPrimary, link
        - fonts: list of {family, role} dicts
        - typography: dict with fontSizes for h1, h2, body
        - spacing: dict with baseUnit and borderRadius
        - components: dict with buttonPrimary styles
        - brandName: string brand/website name
        - screenshot: screenshot URL (base64 or path)
        - logo: logo URL
        - favicon: favicon URL
        - og_image: OG image URL

    Raises:
        ValueError: If FIRECRAWL_API_KEY is not set or URL is invalid.
        requests.RequestException: If the API request fails.
    """
    if api_key is None:
        api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError(
            "FIRECRAWL_API_KEY environment variable is required. "
            "Set it with: export FIRECRAWL_API_KEY='your-key-here'"
        )

    if not url:
        raise ValueError("URL is required")

    # Firecrawl API endpoint for scraping with branding and screenshot formats
    api_url = "https://api.firecrawl.dev/v2/scrape"

    payload = {
        "url": url,
        "formats": ["branding", "screenshot"],
        "origin": "stitch-skills",
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Map Firecrawl response to DESIGN.md frontmatter keys
        result = {
            "colorScheme": data.get("colorScheme", "light"),
            "colors": {
                "primary": data.get("colors", {}).get("primary", "#000000"),
                "secondary": data.get("colors", {}).get("secondary", "#FFFFFF"),
                "background": data.get("colors", {}).get("background", "#FFFFFF"),
                "textPrimary": data.get("colors", {}).get("textPrimary", "#000000"),
                "link": data.get("colors", {}).get("link", "#533AFD"),
            },
            "fonts": data.get("fonts", []),
            "typography": data.get("typography", {}).get("fontSizes", {"h1": "32px", "h2": "24px", "body": "16px"}),
            "spacing": {
                "baseUnit": data.get("spacing", {}).get("baseUnit", 8),
                "borderRadius": data.get("spacing", {}).get("borderRadius", "4px"),
            },
            "components": {
                "buttonPrimary": {
                    "background": data.get("components", {}).get("buttonPrimary", {}).get("background", "#533AFD"),
                    "textColor": data.get("components", {}).get("buttonPrimary", {}).get("textColor", "#FFFFFF"),
                    "borderRadius": data.get("components", {}).get("buttonPrimary", {}).get("borderRadius", "4px"),
                }
            },
            "brandName": data.get("brandName", "Unknown"),
            "screenshot": data.get("screenshot"),
            "logo": data.get("logo"),
            "favicon": data.get("favicon"),
            "og_image": data.get("ogImage"),
        }

        return result

    except requests.RequestException as e:
        print(f"Error calling Firecrawl API: {e}", file=sys.stderr)
        raise


def main():
    """CLI entry point for extracting design metadata from a live URL."""
    if len(sys.argv) < 2:
        print("Usage: python3 extract_from_url.py <URL> [--api-key KEY]")
        sys.exit(1)

    url = sys.argv[1]
    api_key = None
    if "--api-key" in sys.argv:
        idx = sys.argv.index("--api-key")
        if idx + 1 < len(sys.argv):
            api_key = sys.argv[idx + 1]

    try:
        data = extract_from_url(url, api_key)
        print(json.dumps(data, indent=2))
    except (ValueError, requests.RequestException) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
