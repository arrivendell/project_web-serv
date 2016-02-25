SHELL=/bin/bash

virtualenv:
	@echo "--> Building virtual env"
	@-rm -rf ./build
	@virtualenv ./build/venv/ --no-site-packages
	@echo "--->  Installing dependencies in Virtual env"
	@./build/venv/bin/pip install --upgrade wheel pex -r requirements.txt

pex_packaging:
	@echo "---> Installing local modules"
	@-rm -rf ~/.pex/install/webito*
	@-rm -rf ~/.pex/build/webito* 
	@-rm -rf dist/
	@./build/venv/bin/python setup.py bdist_wheel
	@echo "--> Building pex package"
	@./build/venv/bin/pex --repo ./dist/  webito --cache-dir  build/pex-cache -r requirements.txt -m src.run:main --python=./build/venv/bin/python2.7 -o ./build/webito.pex