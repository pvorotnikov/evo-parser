init:
	pip install -r requirements.txt

start:
	PYTHONPATH=$(PWD)/src python src/main.py

.PHONY: init start