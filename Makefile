# `make check` recounts every number this repository states about itself.
# No dependencies: scripts/check.py is standard library only.

.PHONY: check
check:
	python scripts/check.py --verbose

.DEFAULT_GOAL := check
