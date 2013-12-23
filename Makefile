init-dev:
	pip install -r requirements.txt

init-data:
	python tools/init_data.py

web:
	python server.py

test:
	py.test tests/
