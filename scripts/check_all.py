#!/usr/bin/env python3
"""Run the complete repository validation suite on Windows, macOS, or Linux."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_TOP_LEVEL_DIRS={'.git','.venv','venv','site','.pytest_cache','.mypy_cache','.ruff_cache'}


def clean_python_cache() -> None:
    for path in ROOT.rglob("__pycache__"):
        rel=path.relative_to(ROOT)
        if rel.parts and rel.parts[0] in LOCAL_TOP_LEVEL_DIRS:
            continue
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
    for pattern in ("*.pyc", "*.pyo"):
        for path in ROOT.rglob(pattern):
            rel=path.relative_to(ROOT)
            if rel.parts and rel.parts[0] in LOCAL_TOP_LEVEL_DIRS:
                continue
            try:
                path.unlink()
            except FileNotFoundError:
                pass


def run(*args: str) -> None:
    command = [sys.executable, *args]
    print("\n>", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    clean_python_cache()
    checks = [
        ("scripts/generate_catalog.py", "--check"),
        ("scripts/check_placeholders.py",),
        ("scripts/review_due.py", "--strict"),
        ("scripts/validate_structured_files.py",),
        ("scripts/validate_repository.py",),
        ("-m", "unittest", "discover", "-s", "tests", "-v"),
    ]
    try:
        for check in checks:
            run(*check)
    except subprocess.CalledProcessError as exc:
        print(f"\nVALIDATION FAILED (exit code {exc.returncode})", file=sys.stderr)
        return exc.returncode or 1
    finally:
        clean_python_cache()
    print("\nALL REPOSITORY CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
