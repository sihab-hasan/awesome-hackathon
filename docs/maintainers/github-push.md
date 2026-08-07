# GitHub Push Guide

## 0. Start from a clean first-release directory

For the first public release, extract this archive into a new empty directory. Do **not** overlay it onto an older checkout that already contains a `.git` directory or previous commits. The distributed archive intentionally contains no Git history.

If you intentionally want a brand-new history in an existing working folder, back up anything important first, remove the old `.git` directory, and then continue with `git init`.

## 1. Configure repository identity

The distributed repository currently uses `sihab-hasan/awesome-hackathon` in badges, CODEOWNERS, citation metadata, maintainer links, and documentation-site settings. Keep it unchanged only when that is the destination repository.

For another account or organization, run:

```bash
python3 scripts/configure_github.py --owner YOUR_GITHUB_USERNAME --repo awesome-hackathon
```

Use `--maintainer USERNAME` when the primary maintainer differs from the repository owner.

## 2. Run local validation

```bash
python3 -m pip install --requirement requirements-validation.txt
python scripts/check_all.py
```

## 3. Create the repository and push

Create an empty GitHub repository without an auto-generated README, license, or `.gitignore`, then run:

```bash
git init
git add .
git commit -m "release: Awesome Hackathon v1.0.0"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/awesome-hackathon.git
git push -u origin main
```

## 4. Repository settings

After the first push:

1. Enable GitHub Actions.
2. Configure GitHub Pages to use **GitHub Actions** as its source.
3. Enable branch protection for `main`.
4. Require the CI, lint, link, and security checks appropriate for the repository plan.
5. Enable secret scanning, Dependabot alerts, and code scanning where available.
6. Add repository topics such as `awesome-list`, `hackathon`, `developer-resources`, and `open-source`.
7. After the first Pages workflow succeeds, open the published site and verify the **Complete Map** page and GitHub source links.

## 5. First release

After CI is green, create and push the first release tag:

```bash
git tag -a v1.0.0 -m "Awesome Hackathon v1.0.0"
git push origin v1.0.0
```

If Git tag signing is already configured, you may use `git tag -s` instead of `git tag -a`. The release workflow creates the source archive, checksum, source manifest, and provenance attestation.
