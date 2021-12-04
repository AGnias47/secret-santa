PYTHON=python3

.PHONY: help format clean static test

help:    ## Show this help message
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

format:  ## Format all Python code using black
	black -l 120 .

clean:   ## Clean the directory
	git clean -dxf

static:  ## Lint Python files using pylint
	pylint --disable=C0103,C0301,C0411,R1711,R1705,R1734,R1735,R0903 main.py secret_santa/ || true

test:    ## Test the file(s)
	coverage run -m pytest && coverage report && ./test_main.py
