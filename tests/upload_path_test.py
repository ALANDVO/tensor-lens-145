"""Test that SKILL.md upload commands reference real script paths.

Regression for issue: manage-design-system SKILL.md pointed the upload
command at a script that only lived under a different skill directory
(upload-to-stitch), so the command failed from any project cwd.
"""

import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_REF = re.compile(r'python3\s+(\$\{CLAUDE_PLUGIN_ROOT\}|)?(\S+\.py)')


def _referenced_paths(md_path):
    """Yield repo-relative paths for scripts referenced in a SKILL.md."""
    with open(md_path, 'r') as fh:
        text = fh.read()
    for _root, rel in SCRIPT_REF.findall(text):
        # The path may begin with a leading slash from the plugin-root split.
        rel = rel.lstrip('/')
        # Only consider paths that look repo/plugin relative, not bare filenames.
        if '/' not in rel:
            continue
        yield rel


# Scope: the selected feature is the upload path in manage-design-system.
UPLOAD_SKILL = os.path.join(
    REPO_ROOT, 'skills', 'manage-design-system', 'SKILL.md')


def test_upload_skill_scripts_exist():
    checked = 0
    for rel in _referenced_paths(UPLOAD_SKILL):
        # Paths are relative to the repository checkout.
        full = os.path.join(REPO_ROOT, rel)
        assert os.path.exists(full), (
            f"{UPLOAD_SKILL} references missing script: {rel}"
        )
        checked += 1
    assert checked > 0, "Expected at least one script reference to validate"


def test_upload_skill_uses_plugin_variable():
    """The primary command must use ${CLAUDE_PLUGIN_ROOT} or a skill-relative path,
    not a repo-checkout-only relative path (the original defect)."""
    text = open(UPLOAD_SKILL).read()
    assert '${CLAUDE_PLUGIN_ROOT}' in text, (
        "manage-design-system SKILL.md must reference ${CLAUDE_PLUGIN_ROOT} "
        "so the upload command works when the plugin is installed"
    )
    # The broken form pointed at manage-design-system/scripts/, which does not exist.
    assert 'manage-design-system/scripts/upload_to_stitch.py' not in text


if __name__ == '__main__':
    test_upload_skill_scripts_exist()
    test_upload_skill_uses_plugin_variable()
    print("upload path tests passed")
