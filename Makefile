(phony all): init test clean
init:
	@echo "\nBuilding requirements.txt ..."
	pip install pipreqs
	pipreqs ./alltests
	pipreqs ./pydeepgenomics
	@echo "\nInstall dependencies ..."
	pip install -r requirements.txt
test:
	@echo "\nRun the tests ..."
	python3 -m unittest discover
clean:
	@echo "\n\nCleaning up ..."
	find . \( -name \*.pyc -o -name \*.pyo -o -name __pycache__ -o -name playground \) -prune -exec rm -rf {} +	

.PHONY: init clean test clean
