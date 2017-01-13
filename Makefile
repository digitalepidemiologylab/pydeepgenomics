BUILDDIR      = build
(phony all): init test clean

init:
	@echo "\nInstall dependencies ..."
	pip install -r requirements.txt

buildreqs:
	@echo "\nBuilding requirements.txt ..."
	pip install pipreqs
	pipreqs --force ./

test:
	@echo "\nRun the tests ..."
	python3 -m pytest --doctest-modules --verbose

clean-pycs:
	@echo "\n\nCleaning up ..."
	find . \( -name \*.pyc -o -name \*.pyo -o -name __pycache__ -o -name playground \) -prune -exec rm -rf {} +	


.PHONY: init clean-pycs test clean-pycs