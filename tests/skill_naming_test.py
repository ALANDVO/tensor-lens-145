"""Test that skill names comply with naming conventions."""

import os
import re

SKILL_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_.\-\s]+$')  # letters, numbers, hyphens, underscores, dots, spaces


def get_skill_names(skills_dir: str) -> list:
    """Extract skill names from all SKILL.md files in the skills directory."""
    names = []
    for root, dirs, files in os.walk(skills_dir):
        for f in files:
            if f == 'SKILL.md':
                path = os.path.join(root, f)
                with open(path, 'r') as fh:
                    content = fh.read()
                # Find the first line that looks like a title/name
                for line in content.split('\n')[:10]:
                    line = line.strip()
                    if line.startswith('#'):
                        # This is a heading; the skill name is the directory name
                        names.append(os.path.basename(root))
                        break
                else:
                    names.append(os.path.basename(root))
    return names


def test_skill_names_no_colons(skills_dir: str = 'skills'):
    """Test that no skill names contain colons."""
    names = get_skill_names(skills_dir)
    for name in names:
        assert ':' not in name, f"Skill name '{name}' contains a colon, which is not allowed"
        # Verify pattern compliance
        assert SKILL_NAME_PATTERN.match(name) is not None, (
            f"Skill name '{name}' does not match allowed pattern: {SKILL_NAME_PATTERN.pattern}"
        )


if __name__ == '__main__':
    test_skill_names_no_colons()
    print("All skill naming tests passed!")
