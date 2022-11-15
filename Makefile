PYTHON=python3

.PHONY: help format clean static test docs_new_modules docs

help:              ## Show this help message
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

format:            ## Format all Python code using black
	black -l 120 .

clean:             ## Clean the directory
	git clean -dxf -e pii/ -e venv/

static:            ## Lint Python files using pylint
	pylint --disable=C0103,C0301,C0411,R1711,R1705,R1734,R1735,R0903 main.py secret_santa/ || true

test:              ## Test the file(s)
	coverage run -m pytest && coverage report && ./test_main.py

docs_new_modules:  ## Generate new sphinx documentation templates when new modules are added
	sphinx-apidoc -f -o sphinx/source/ .

docs:              ## Update Sphinx documentation
	cd sphinx && bash update_documentation.bash

