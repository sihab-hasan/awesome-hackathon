#!/usr/bin/env python3
"""Configure owner/repository-specific GitHub metadata before the first push."""
from __future__ import annotations

import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OWNER = "sihab-hasan"
DEFAULT_REPO = "awesome-hackathon"

def write_lf(path: Path, text: str) -> None:
    """Write UTF-8 text with deterministic LF line endings on every OS."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    path.write_bytes(normalized.encode("utf-8"))


TEXT_FILES = [
    ROOT / "README.md",
    ROOT / "CITATION.cff",
    ROOT / "mkdocs.yml",
    ROOT / "mkdocs-site.yml",
    ROOT / ".github" / "CODEOWNERS",
    ROOT / "docs" / "maintainers" / "maintainers.md",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True, help="GitHub account or organization")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="GitHub repository name")
    parser.add_argument("--maintainer", help="Maintainer username; defaults to owner")
    return parser.parse_args()


def replace_text(text: str, owner: str, repo: str, maintainer: str) -> str:
    replacements = {
        f"github.com/{DEFAULT_OWNER}/{DEFAULT_REPO}": f"github.com/{owner}/{repo}",
        f"{DEFAULT_OWNER}.github.io/{DEFAULT_REPO}": f"{owner}.github.io/{repo}",
        f"{DEFAULT_OWNER}/{DEFAULT_REPO}": f"{owner}/{repo}",
        f"@{DEFAULT_OWNER}": f"@{maintainer}",
        f"github.com/{DEFAULT_OWNER}": f"github.com/{maintainer}",
        f"`{DEFAULT_OWNER}`": f"`{maintainer}`",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Support rerunning after the first customization.
    text = re.sub(r"https://github\.com/[^/\s]+/awesome-hackathon", f"https://github.com/{owner}/{repo}", text)
    text = re.sub(r"https://[^.\s]+\.github\.io/awesome-hackathon/?", f"https://{owner}.github.io/{repo}/", text)
    return text


def main() -> int:
    args = parse_args()
    owner = args.owner.strip()
    repo = args.repo.strip()
    maintainer = (args.maintainer or owner).strip()
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", owner):
        raise SystemExit("Invalid GitHub owner")
    if not re.fullmatch(r"[A-Za-z0-9._-]+", repo):
        raise SystemExit("Invalid repository name")
    for path in TEXT_FILES:
        text = path.read_text(encoding="utf-8")
        write_lf(path, replace_text(text, owner, repo, maintainer))
    print(f"Configured repository for https://github.com/{owner}/{repo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
