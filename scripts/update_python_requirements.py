from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.request import urlopen


PINNED_REQUIREMENT = re.compile(r"^([A-Za-z0-9_.-]+)(\[.*\])?==([^#\s]+)(.*)$")


def latest_version(package_name: str) -> str:
    with urlopen(f"https://pypi.org/pypi/{package_name}/json", timeout=20) as response:
        payload = json.load(response)
    return str(payload["info"]["version"])


def update_line(line: str) -> str:
    match = PINNED_REQUIREMENT.match(line.rstrip("\n"))
    if match is None:
        return line

    package_name, extras, _current_version, suffix = match.groups()
    latest = latest_version(package_name)
    extras = extras or ""
    return f"{package_name}{extras}=={latest}{suffix}\n"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: update_python_requirements.py path/to/requirements.txt", file=sys.stderr)
        return 2

    requirements_path = Path(sys.argv[1])
    updated = "".join(update_line(line) for line in requirements_path.read_text().splitlines(keepends=True))
    requirements_path.write_text(updated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
