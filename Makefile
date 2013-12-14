init-dev:
	pip install -r requirements.txt

web:
	python -W ignore server.py

test:
	py.test tests/
