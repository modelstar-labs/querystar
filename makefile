# Path: makefile

.ONESHELL:

.PHONY: publish
publish:
	poetry publish --build --username __token__ --password $$PYPI_QUERYSTAR_KEY --build --skip-existing
