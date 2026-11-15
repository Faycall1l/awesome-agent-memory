PYTHON ?= python3

.PHONY: help build validate links lint check refresh clean

help:
	@echo "make build     regenerate README.md from data/entries.csv"
	@echo "make validate  check entries.csv structure (sections, kinds, URLs, duplicates)"
	@echo "make links     check every link in entries.csv (slow, polite)"
	@echo "make lint      run awesome-lint on README.md (requires npx)"
	@echo "make check     validate and fail if README.md is stale (what CI runs)"
	@echo "make refresh   re-query the arXiv API for data/arxiv_meta.json"
	@echo "make clean     remove generated caches"

build:
	$(PYTHON) scripts/build_readme.py

validate:
	$(PYTHON) scripts/validate.py

links:
	$(PYTHON) scripts/check_links.py

lint:
	npx --yes awesome-lint

check: validate
	$(PYTHON) scripts/build_readme.py
	@git diff --quiet -- README.md || { \
		echo "README.md is stale: run 'make build' and commit the result."; \
		git diff --stat -- README.md; \
		exit 1; \
	}

refresh:
	$(PYTHON) scripts/gen_entries.py --refresh
	$(PYTHON) scripts/build_readme.py

clean:
	rm -rf scripts/__pycache__
