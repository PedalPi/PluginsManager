from setuptools import setup

def readme():
    with open('Readme.md') as f:
        return f.read()

setup(
    name='PedalPi - PluginsManager',
    version='0.0.1',
    long_description=readme(),
    packages=['pluginsmanager'],
    test_suite='test',
    keywords='pedalpi mod-host lv2 audio plugin manager',
    url='https://github.com/PedalPi/PluginsManager',
    author='SrMouraSilva',
)

