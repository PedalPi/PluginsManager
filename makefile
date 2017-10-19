.RECIPEPREFIX +=
BROWSER=firefox

default: run

clean: clean-pyc clean-test clean-build

clean-build:
    rm -rf .eggs
    rm -rf build
    rm -rf dist

clean-pyc:
    find . -name '*.pyc' -exec rm --force {} +
    find . -name '*.pyo' -exec rm --force {} +

clean-test:
    rm -f .coverage
    rm -rf htmlcov
    rm -rf test/autosaver_data

clean-docs:
    rm -rf docs/build

docs: clean-docs
    cd docs && $(MAKE) html

docs-see: docs
    $(BROWSER) docs/build/html/index.html

install-tests-requirements:
    # For midi tests - https://github.com/x42/midifilter.lv2
    cd /tmp && git clone git://github.com/x42/midifilter.lv2.git && \
    cd midifilter.lv2 && \
    make && \
    sudo make install PREFIX=/usr

run:
    @echo "Run option isn't created =)"

test: clean-test
    mkdir test/autosaver_data
    coverage3 run --source=pluginsmanager setup.py test
    coverage3 report

test-details: test
    coverage3 html
    $(BROWSER) htmlcov/index.html

help:
    @echo "    clean"
    @echo "          Clean files"
    @echo "    docs"
    @echo "          Make the docs"
    @echo "    docs-see"
    @echo "          Make the docs and open it in BROWSER"
    @echo "    test"
    @echo "          Execute the tests"
    @echo "    test-details"
    @echo "          Execute the tests and shows the result in BROWSER"
    @echo "           - BROWSER=firefox"
    @echo "    help"
    @echo "          Show the valid commands"
