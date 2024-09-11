.ONESHELL:

# Run MegaLinter
lint:
	npx mega-linter-runner -e 'SHOW_ELAPSED_TIME=true'

flake8: venv
	venv/bin/pip3 install flake8
	venv/bin/flake8 --config=./.flake8 --exclude=venv,__pycache__,.pytest_cache,.venv .

trivy-scan:
	@echo "Running Trivy scan..."
	docker build -t localbuild/testimage:latest .
	trivy image --severity HIGH,CRITICAL localbuild/testimage:latest

all:

.PHONY: trivy-scan lint all
