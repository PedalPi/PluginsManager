BROWSER=firefox
BOLD=\033[1m
NORMAL=\033[0m

default: help

clean: clean-pyc clean-test clean-build clean-docs

clean-build:
	rm -rf .eggs
	rm -rf build
	rm -rf dist

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +

clean-test:
	rm -rf .cache
	rm -f .coverage
	rm -rf htmlcov
	rm -rf test/autosaver_data

clean-docs:
	rm -rf docs/build

docs: clean-docs
	cd docs && $(MAKE) html

docs-see: docs
	$(BROWSER) docs/build/html/index.html

install-docs-requirements:
	pip install sphinx_rtd_theme

install-tests-requirements:
	# For midi tests - https://github.com/x42/midifilter.lv2
	cd /tmp && git clone git://github.com/x42/midifilter.lv2.git --depth=1 && \
	cd midifilter.lv2 && \
	make && \
	sudo make install PREFIX=/usr

run:
	@echo "Run option isn't created =)"

test: clean-test
	mkdir test/autosaver_data
	pytest --cov=pluginsmanager

test-docs:
	python -m doctest *.rst -v
	python -m doctest docs/*/*.rst -v

test-details: test
	coverage3 html
	$(BROWSER) htmlcov/index.html

help: cabecalho
	@echo ""
	@echo "Commands"
	@echo "    $(BOLD)clean$(NORMAL)"
	@echo "          Clean files"
	@echo "    $(BOLD)docs$(NORMAL)"
	@echo "          Make the docs"
	@echo "    $(BOLD)docs-see$(NORMAL)"
	@echo "          Make the docs and open it in BROWSER"
	@echo "    $(BOLD)install-docs-requirements$(NORMAL)"
	@echo "          Install the docs requirements"
	@echo "    $(BOLD)install-tests-requirements$(NORMAL)"
	@echo "          Install the tests requirements"
	@echo "    $(BOLD)test$(NORMAL)"
	@echo "          Execute the tests"
	@echo "    $(BOLD)test-details$(NORMAL)"
	@echo "          Execute the tests and shows the result in BROWSER"
	@echo "           - BROWSER=firefox"
	@echo "    $(BOLD)help$(NORMAL)"
	@echo "          Show the valid commands"

cabecalho:
	@echo "$(BOLD) _____  _            _            _____"
	@echo "|  _  || | _ _  ___ |_| ___  ___ |     | ___  ___  ___  ___  ___  ___"
	@echo "|   __|| || | || . || ||   ||_ -|| | | || .'||   || .'|| . || -_||  _|"
	@echo "|__|   |_||___||_  ||_||_|_||___||_|_|_||__,||_|_||__,||_  ||___||_|"
	@echo "               |___|                                   |___|"
	@echo "Github$(NORMAL): https://pypi.org/project/PedalPi-PluginsManager/"
