.PHONY: install generate validate test check search docs clean

install:
	python3 -m pip install --requirement requirements-validation.txt

generate:
	python3 scripts/generate_catalog.py

validate:
	python3 scripts/check_all.py

test:
	python3 -m unittest discover -s tests -v

check:
	python3 scripts/check_all.py

search:
	python3 scripts/catalog_query.py $(QUERY)

docs:
	zensical build --strict

clean:
	python3 -c "import shutil,pathlib; r=pathlib.Path('.'); [shutil.rmtree(p,ignore_errors=True) for p in r.rglob('__pycache__')]; [p.unlink(missing_ok=True) for pat in ('*.pyc','*.pyo') for p in r.rglob(pat)]"
