from __future__ import annotations

import json
import subprocess
from datetime import datetime, UTC
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_git_tags() -> list[str]:
    result = subprocess.run(
        ["git", "tag", "--list"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [tag.strip() for tag in result.stdout.splitlines() if tag.strip()]


def next_version() -> str:
    year = datetime.now(UTC).year
    prefix = f"v{year}."
    builds = []
    for tag in run_git_tags():
        if tag.startswith(prefix):
            try:
                builds.append(int(tag.removeprefix(prefix)))
            except ValueError:
                continue
    return f"{year}.{max(builds, default=0) + 1}"


def update_frontend_package(version: str) -> None:
    for path in [ROOT / "frontend" / "package.json", ROOT / "frontend" / "package-lock.json"]:
        payload = json.loads(path.read_text())
        payload["version"] = version
        if path.name == "package-lock.json" and "packages" in payload and "" in payload["packages"]:
            payload["packages"][""]["version"] = version
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def main() -> int:
    version = next_version()
    (ROOT / "VERSION").write_text(f"{version}\n")
    update_frontend_package(version)
    print(version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
