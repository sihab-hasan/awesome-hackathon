# Documentation Site

The public documentation website publishes the **complete repository knowledge base**, not only the participant handbook. GitHub remains the canonical source of truth; the site is generated from the repository at build time.

## Published content

The site includes every Markdown document in the repository, including:

- the participant and engineering handbook;
- all curated resource-category pages and resource packs;
- architecture, product-specification, implementation-pattern, and reference-build blueprints;
- 24/48/72-hour and recovery playbooks;
- planning, engineering, security, testing, deployment, presentation, and submission checklists;
- AI, data, mobile, web, hardware, beginner, and social-impact tracks;
- project-idea briefs and structured prompts;
- organizer and judge operations manuals;
- community, curation, governance, maintenance, security, release, validation, and repository documentation;
- GitHub automation, asset, and repository-test documentation.

Each generated page contains a **View on GitHub** link to its canonical source file. The generated **Complete Map** page lists every published Markdown source and its website counterpart.

## Architecture

```text
canonical GitHub Markdown/files
        |
        v
scripts/prepare_docs_site.py
        |
        +--> .site-docs/                # temporary generated source tree
        +--> mkdocs-site.generated.yml  # generated complete navigation
        |
        v
Zensical strict build
        |
        v
site/                                  # static public website
        |
        v
GitHub Pages
```

`.site-docs/`, `mkdocs-site.generated.yml`, and `site/` are generated outputs and are intentionally excluded from version control.

`mkdocs.yml` remains the compact handbook-only configuration used by repository structural validation. `mkdocs-site.yml` is the public full-site template used by GitHub Pages.

## Theme behavior

The public documentation site includes a three-state appearance control next to search:

1. **System** — follows the operating-system light/dark preference and reacts when it changes;
2. **Light** — forces the `default` light palette; and
3. **Dark** — forces the `slate` dark palette.

The theme selection uses the documentation engine's native palette control, so the visitor's explicit choice is retained by the site rather than being implemented through a custom one-off toggle.

## Local preview

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-docs.txt
python3 scripts/prepare_docs_site.py
zensical serve --config-file mkdocs-site.generated.yml
```

Open `http://localhost:8000/`.

On Windows PowerShell, activate the environment with `.venv\\Scripts\\Activate.ps1` before running the remaining commands.

## Strict production build

```bash
python3 scripts/prepare_docs_site.py
zensical build --strict --config-file mkdocs-site.generated.yml
```

The final static website is written to `site/`.

## GitHub Pages publishing

`.github/workflows/pages.yml` automatically:

1. checks out the repository;
2. installs the pinned documentation dependency;
3. generates the complete documentation source tree and navigation;
4. runs a strict Zensical build;
5. uploads the `site/` artifact; and
6. deploys through GitHub Pages using least-privilege permissions.

Before the first deployment, open **GitHub → Settings → Pages** and set **Source** to **GitHub Actions**. After that, pushes to `main` that change documentation, site assets, catalog data, or site-build configuration trigger a new deployment.

## Repository identity

For a fork or a new owner, configure repository URLs before the first push:

```bash
python3 scripts/configure_github.py --owner YOUR_GITHUB_USERNAME --repo awesome-hackathon
```

This updates both the repository metadata and the public documentation-site URLs.

## Hosting elsewhere

The output in `site/` is a self-contained static website. It can also be hosted on Cloudflare Pages, Netlify, Vercel static hosting, an object-storage/CDN setup, nginx, Apache, or any host that serves static files.

## Content maintenance rule

Do **not** edit `.site-docs/`, `mkdocs-site.generated.yml`, or `site/`. Edit the canonical repository Markdown or data, regenerate catalog views when required, run repository validation, and let the documentation build regenerate the public site.
