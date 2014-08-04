.PHONY: test clean clean_all lint

PWD=$(shell pwd)
all: setup develop lint coverage

develop: setup venv/lib/python*/site-packages/module-symbols.egg-link
venv/lib/python*/site-packages/module-symbols.egg-link:
	venv/bin/python setup.py develop

sysdeps:
	sudo apt-get install -y python-dev libyaml-dev python-virtualdev

setup: venv/bin/python
	venv/bin/pip install -q -r requirements.test.txt

venv/bin/python:
	virtualenv venv --system-site-packages
	venv/bin/pip install 'distribute>=0.6.45'

test: develop
	echo "XXX test stub"

coverage: develop clean
	echo "XXX coverage stub"

lint: develop
	echo "XXX lint stub"

clean:
	find . -name \*.pyc -delete
	find . -name '*.bak' -delete
	rm -f .coverage

clean_all: clean
	rm -rf venv
