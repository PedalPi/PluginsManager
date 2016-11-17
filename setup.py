from setuptools import setup, find_packages

def readme():
    with open('Readme.md') as f:
        return f.read()

setup(
    name='PedalPi - PluginsManager',
    version='0.0.1',
    long_description=readme(),
    #packages=find_packages('pluginsmanager'),
    packages=[
        'pluginsmanager',

        'pluginsmanager/mod_host',
        'pluginsmanager/model',
        'pluginsmanager/model/lv2',
        'pluginsmanager/model/system',

        'pluginsmanager/util',
    ],
    test_suite='test',
    install_requires=['JACK-Client'],
    tests_require=['JACK-Client'],
    keywords='pedalpi mod-host lv2 audio plugin manager',
    url='https://github.com/PedalPi/PluginsManager',
    author='SrMouraSilva',
)
