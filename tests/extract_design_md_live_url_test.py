"""Test that extract_from_url script has correct structure and can be imported."""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock


class TestExtractFromURLScriptStructure(unittest.TestCase):
    """Test the extract_from_url.py script structure and imports."""

    SCRIPT_PATH = os.path.join(
        os.path.dirname(__file__), '..', 'skills', 'extract-design-md',
        'scripts', 'extract_from_url.py'
    )

    def setUp(self):
        """Add scripts directory to path for imports."""
        scripts_dir = os.path.dirname(self.SCRIPT_PATH)
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)

    def test_script_imports(self):
        """Test that the script can be imported without errors."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "extract_from_url",
            self.SCRIPT_PATH
        )
        self.assertIsNotNone(spec, "Script spec should exist")
        self.assertIsNotNone(spec.loader, "Script loader should exist")

    def test_extract_from_url_function_exists(self):
        """Test that extract_from_url function is defined in the script."""
        with open(self.SCRIPT_PATH, 'r') as f:
            content = f.read()
        self.assertIn('def extract_from_url', content,
                      "extract_from_url function should be defined")

    def test_main_function_exists(self):
        """Test that main function is defined in the script."""
        with open(self.SCRIPT_PATH, 'r') as f:
            content = f.read()
        self.assertIn('def main', content,
                      "main function should be defined")

    @patch('requests.post')
    def test_extract_from_url_with_mocked_api(self, mock_post):
        """Test extract_from_url with mocked API response."""
        import extract_from_url

        # Setup mock response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "colorScheme": "light",
            "colors": {
                "primary": "#533AFD",
                "secondary": "#E5EDF5",
                "background": "#FFFFFF",
                "textPrimary": "#000000",
                "link": "#533AFD",
            },
            "fonts": [
                {"family": "Sohne-Var", "role": "body"},
                {"family": "SF Pro Display", "role": "heading"},
            ],
            "typography": {"fontSizes": {"h1": "48px", "h2": "32px", "body": "14px"}},
            "spacing": {"baseUnit": 8, "borderRadius": "0px"},
            "components": {
                "buttonPrimary": {
                    "background": "#533AFD",
                    "textColor": "#FFFFFF",
                    "borderRadius": "4px",
                }
            },
            "brandName": "Stripe",
            "screenshot": "https://example.com/screenshot.png",
            "logo": "https://example.com/logo.png",
            "favicon": "https://example.com/favicon.ico",
            "ogImage": "https://example.com/og.png",
        }
        mock_post.return_value = mock_response

        # Test the function
        result = extract_from_url.extract_from_url("https://stripe.com", "test-key")

        # Verify structure
        self.assertIn("colorScheme", result)
        self.assertIn("colors", result)
        self.assertIn("brandName", result)
        self.assertIn("screenshot", result)
        self.assertEqual(result["colorScheme"], "light")
        self.assertEqual(result["brandName"], "Stripe")
        self.assertIsNotNone(result["screenshot"])


if __name__ == '__main__':
    unittest.main()
