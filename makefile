env:
	python3 -m venv ./env
	./env/bin/pip3 install -r requirements.txt

install: env
	./env/bin/python3 install.py


PHONY: env
