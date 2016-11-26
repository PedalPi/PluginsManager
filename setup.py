from setuptools import setup


def readme():
    with open('Readme.rst') as f:
        return f.read()

setup(
    name='PedalPi-PluginsManager',
    version='0.0.2',
    long_description=readme(),
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
