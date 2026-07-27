.PHONY: help build check validate refresh lint

help:
	@echo "make build     Regenerate every Markdown surface + data/tools.json from data/"
	@echo "make check     Fail if generated files are out of date (what CI runs)"
	@echo "make validate  Check data/tools.yaml and data/categories.yaml for errors"
	@echo "make refresh   Pull stars/freshness/license from the GitHub API, then rebuild"
	@echo "make lint      Run awesome-lint on AWESOME.md (needs Node)"

build: validate
	@python3 scripts/build.py

check: validate
	@python3 scripts/build.py --check

validate:
	@python3 scripts/validate.py

refresh:
	@python3 scripts/refresh_metadata.py
	@python3 scripts/build.py

lint:
	@npx --yes awesome-lint AWESOME.md
