#!/usr/bin/env python3
"""Prepare the complete public documentation site from repository Markdown.

The Git repository remains the source of truth. This script creates a temporary
`.site-docs/` tree containing every Markdown document, required linked assets,
and a generated navigation configuration for Zensical.
"""
from __future__ import annotations

import argparse
import html
import re
import shutil
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCS_DIR = ROOT / ".site-docs"
DEFAULT_CONFIG = ROOT / "mkdocs-site.generated.yml"
BASE_CONFIG = ROOT / "mkdocs-site.yml"
SITE_ASSETS = ROOT / "site-assets"

MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
H1 = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)

TOP_LEVEL_SECTIONS = [
    ("Handbook", "handbook"),
    ("Resources", "resources"),
    ("Blueprints", "blueprints"),
    ("Playbooks", "playbooks"),
    ("Checklists", "checklists"),
    ("Tracks", "tracks"),
    ("Project Ideas", "project-ideas"),
    ("Organizers", "organizers"),
    ("Judges", "judges"),
    ("Community", "community"),
    ("Prompts", "prompts"),
    ("Catalog", "catalog"),
]

START_HERE = [
    "docs/getting-started/quickstart.md",
    "docs/getting-started/stack-selector.md",
    "docs/getting-started/faq.md",
    "docs/project/roadmap.md",
]
ROOT_REPOSITORY_ORDER = [
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "SUPPORT.md",
    "CHANGELOG.md",
]

SKIP_DIRS = {".git", ".site-docs", "site", ".venv", "node_modules", "__pycache__"}


def write_lf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs-dir", default=str(DEFAULT_DOCS_DIR.relative_to(ROOT)))
    parser.add_argument("--config", default=str(DEFAULT_CONFIG.relative_to(ROOT)))
    return parser.parse_args()


def markdown_sources() -> list[Path]:
    result: list[Path] = []
    for path in ROOT.rglob("*.md"):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        result.append(path)
    return sorted(result, key=lambda p: p.relative_to(ROOT).as_posix().casefold())


def repo_url() -> str:
    text = BASE_CONFIG.read_text(encoding="utf-8")
    match = re.search(r"(?m)^repo_url:\s*(\S+)\s*$", text)
    return match.group(1).rstrip("/") if match else "https://github.com/sihab-hasan/awesome-hackathon"


def source_note(source_rel: Path) -> str:
    url = f"{repo_url()}/blob/main/{source_rel.as_posix()}"
    return (
        '<div class="source-meta">'
        f'<span>Canonical source: <code>{html.escape(source_rel.as_posix())}</code></span>'
        f'<a href="{html.escape(url)}">View on GitHub</a>'
        "</div>"
    )


def inject_source_note(text: str, source_rel: Path) -> str:
    lines = text.splitlines()
    if not lines:
        return text
    insert_at = 1 if lines[0].startswith("#") else 0
    note = source_note(source_rel)
    lines[insert_at:insert_at] = ["", note, ""]
    return "\n".join(lines).rstrip() + "\n"


def copy_markdown(docs_dir: Path, sources: list[Path]) -> dict[str, str]:
    """Copy all Markdown and return source path -> generated docs path mapping."""
    mapping: dict[str, str] = {}
    for source in sources:
        rel = source.relative_to(ROOT)
        if rel == Path("README.md"):
            target_rel = Path("index.md")
        elif rel.parts and rel.parts[0] == ".github":
            # Zensical/MkDocs-style file scanners may ignore hidden source directories.
            # Publish GitHub-operation Markdown under a visible website path instead.
            target_rel = Path("github").joinpath(*rel.parts[1:])
        else:
            target_rel = rel
        target = docs_dir / target_rel
        text = source.read_text(encoding="utf-8")
        write_lf(target, inject_source_note(text, rel))
        mapping[rel.as_posix()] = target_rel.as_posix()
    return mapping


def copy_linked_files(docs_dir: Path, sources: list[Path]) -> None:
    """Copy non-Markdown files referenced by local Markdown links."""
    linked: set[Path] = set()
    for source in sources:
        text = source.read_text(encoding="utf-8")
        for raw in MARKDOWN_LINK.findall(text):
            target = raw.strip().split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            candidate = (source.parent / target).resolve()
            try:
                rel = candidate.relative_to(ROOT.resolve())
            except ValueError:
                continue
            if candidate.is_file() and candidate.suffix.lower() != ".md":
                linked.add(rel)
    # Site-critical public data/assets are copied even when only referenced from HTML.
    for path in (ROOT / "assets").rglob("*"):
        if path.is_file() and path.suffix.lower() != ".md":
            linked.add(path.relative_to(ROOT))
    for path in (ROOT / "catalog").glob("*.json"):
        linked.add(path.relative_to(ROOT))
    for name in ("LICENSE", "VERSION", "CITATION.cff"):
        path = ROOT / name
        if path.is_file():
            linked.add(Path(name))

    for rel in sorted(linked, key=lambda p: p.as_posix().casefold()):
        target = docs_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, target)


def copy_site_assets(docs_dir: Path) -> None:
    if not SITE_ASSETS.is_dir():
        return
    for source in SITE_ASSETS.rglob("*"):
        if source.is_file():
            rel = source.relative_to(SITE_ASSETS)
            target = docs_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def title_for(source_rel: str, mapping: dict[str, str]) -> str:
    source = ROOT / source_rel
    if source.exists() and source.suffix.lower() == ".md":
        match = H1.search(source.read_text(encoding="utf-8"))
        if match:
            return re.sub(r"\s+\[[^\]]+\]\([^)]*\)", "", match.group(1)).strip()
    stem = Path(source_rel).stem
    if stem.upper() == "README":
        stem = Path(source_rel).parent.name
    return stem.replace("-", " ").replace("_", " ").title()


def folder_title(folder: Path) -> str:
    readme = ROOT / folder / "README.md"
    if readme.is_file():
        match = H1.search(readme.read_text(encoding="utf-8"))
        if match:
            return match.group(1).strip()
    return folder.name.replace("-", " ").replace("_", " ").title()


def nav_for_folder(folder: Path, mapping: dict[str, str]) -> list[object]:
    absolute = ROOT / folder
    items: list[object] = []
    readme = absolute / "README.md"
    if readme.is_file():
        rel = readme.relative_to(ROOT).as_posix()
        items.append({title_for(rel, mapping): mapping[rel]})

    files = [p for p in absolute.glob("*.md") if p.name != "README.md"]
    for file in sorted(files, key=lambda p: p.name.casefold()):
        rel = file.relative_to(ROOT).as_posix()
        items.append({title_for(rel, mapping): mapping[rel]})

    dirs = [p for p in absolute.iterdir() if p.is_dir() and p.name not in SKIP_DIRS]
    for subdir in sorted(dirs, key=lambda p: p.name.casefold()):
        if not any(subdir.rglob("*.md")):
            continue
        sub_rel = subdir.relative_to(ROOT)
        items.append({folder_title(sub_rel): nav_for_folder(sub_rel, mapping)})
    return items


def root_repo_docs(mapping: dict[str, str]) -> list[object]:
    all_root = [p.name for p in ROOT.glob("*.md") if p.name != "README.md"]
    ordered = [name for name in ROOT_REPOSITORY_ORDER if name in all_root]
    ordered += sorted([name for name in all_root if name not in ordered], key=str.casefold)
    return [{title_for(name, mapping): mapping[name]} for name in ordered]


def documentation_nav(mapping: dict[str, str]) -> list[object]:
    items: list[object] = []
    overview = "docs/README.md"
    if overview in mapping:
        items.append({title_for(overview, mapping): mapping[overview]})
    for folder in (Path("docs/maintainers"), Path("docs/repository")):
        if (ROOT / folder).is_dir() and any((ROOT / folder).rglob("*.md")):
            items.append({folder_title(folder): nav_for_folder(folder, mapping)})
    project_items = []
    for rel in ("docs/project/disclaimer.md", "docs/project/acknowledgements.md"):
        if rel in mapping:
            project_items.append({title_for(rel, mapping): mapping[rel]})
    if project_items:
        items.append({"Project": project_items})
    return items


def build_nav(mapping: dict[str, str]) -> list[object]:
    nav: list[object] = [{"Home": "index.md"}]
    nav.append(
        {
            "Start Here": [
                {title_for(name, mapping): mapping[name]}
                for name in START_HERE
                if name in mapping
            ]
        }
    )
    for label, folder in TOP_LEVEL_SECTIONS:
        nav.append({label: nav_for_folder(Path(folder), mapping)})

    nav.append({"Documentation": documentation_nav(mapping)})

    github_items: list[object] = []
    for folder in (Path(".github"), Path("tests"), Path("assets")):
        if (ROOT / folder).is_dir() and any((ROOT / folder).rglob("*.md")):
            github_items.append({folder_title(folder): nav_for_folder(folder, mapping)})
    nav.append({"Repository": root_repo_docs(mapping) + github_items})
    return nav


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_nav_yaml(nav: list[object]) -> str:
    lines = ["nav:"]

    def emit(value: object, indent: int) -> None:
        pad = " " * indent
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    key, child = next(iter(item.items()))
                    if isinstance(child, list):
                        lines.append(f"{pad}- {yaml_quote(str(key))}:")
                        emit(child, indent + 4)
                    else:
                        lines.append(f"{pad}- {yaml_quote(str(key))}: {yaml_quote(str(child))}")
                else:
                    lines.append(f"{pad}- {yaml_quote(str(item))}")
            return
        raise TypeError(f"Unexpected nav value: {value!r}")

    emit(nav, 2)
    return "\n".join(lines)


def generated_site_map(mapping: dict[str, str]) -> str:
    sources = sorted(mapping, key=str.casefold)
    rows = [
        "# Complete Documentation Map",
        "",
        "This generated page confirms that the public site includes every Markdown document in the repository.",
        "",
        f"**Total published Markdown pages: {len(sources)}**",
        "",
        "| Repository source | Website page |",
        "| --- | --- |",
    ]
    for source_rel in sources:
        website_rel = mapping[source_rel]
        web_target = "./" if website_rel == "index.md" else website_rel
        github = f"{repo_url()}/blob/main/{source_rel}"
        rows.append(
            f"| [`{source_rel}`]({github}) | [{title_for(source_rel, mapping)}]({web_target}) |"
        )
    rows.extend(
        [
            "",
            "The static website is generated from canonical repository files; edit the GitHub source rather than the temporary `.site-docs/` build tree.",
            "",
        ]
    )
    return "\n".join(rows)


def validate_mapping(sources: list[Path], mapping: dict[str, str]) -> None:
    expected = {p.relative_to(ROOT).as_posix() for p in sources}
    actual = set(mapping)
    if expected != actual:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise SystemExit(f"Documentation mapping mismatch: missing={missing}, extra={extra}")
    destinations = list(mapping.values())
    if len(destinations) != len(set(destinations)):
        raise SystemExit("Documentation mapping contains duplicate output paths")


def main() -> int:
    args = parse_args()
    docs_dir = (ROOT / args.docs_dir).resolve()
    config_path = (ROOT / args.config).resolve()
    if docs_dir == ROOT or ROOT not in docs_dir.parents:
        raise SystemExit("--docs-dir must be a generated subdirectory of the repository")

    if docs_dir.exists():
        shutil.rmtree(docs_dir)
    docs_dir.mkdir(parents=True)

    sources = markdown_sources()
    mapping = copy_markdown(docs_dir, sources)
    validate_mapping(sources, mapping)
    copy_linked_files(docs_dir, sources)
    copy_site_assets(docs_dir)

    site_map_rel = "complete-documentation-map.md"
    write_lf(docs_dir / site_map_rel, generated_site_map(mapping))

    nav = build_nav(mapping)
    nav.insert(1, {"Complete Map": site_map_rel})
    nav_yaml = render_nav_yaml(nav)

    base = BASE_CONFIG.read_text(encoding="utf-8")
    if not re.search(r"(?m)^nav:\s*\[\]\s*$", base):
        raise SystemExit("mkdocs-site.yml must contain exactly one 'nav: []' placeholder")
    generated = re.sub(r"(?m)^nav:\s*\[\]\s*$", nav_yaml, base, count=1)
    write_lf(config_path, generated)

    print(
        f"Prepared complete documentation site: {len(sources)} repository Markdown files + site map; "
        f"docs={docs_dir.relative_to(ROOT)}, config={config_path.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
