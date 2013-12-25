init-dev:
	pip install -r requirements.txt

init-data:
	python tools/init_data.py

web: clean_pyc
	python server.py

clean_pyc:
	@find `pwd` \( -name '*.pyc' -o -name '*.ptlc' \) -type f -delete

test: clean_pyc
	py.test tests/
