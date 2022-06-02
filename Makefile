install:
	poetry install
build:
	poetry build
package-install:
	python -m pip install --user --force-reinstall dist/*.whl
test:
	poetry run pytest -vv
test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml
lint:
	poetry run flake8 page_loader
.PHONY: install build package-install test test-coverage lint 