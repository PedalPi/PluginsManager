# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import path
from setuptools import setup


def readme():
    here = path.abspath(path.dirname(__file__))

    with open(path.join(here, 'README.rst'), encoding='UTF-8') as f:
        return f.read()

setup(
    name='PedalPi-PluginsManager',
    version='0.2.0',

    description='Pythonic management of LV2 audio plugins with mod-host.',
    long_description=readme(),

    url='https://github.com/PedalPi/PluginsManager',
    download_url='https://github.com/PedalPi/PluginsManager/tarball/v0.2.0',

    author='Paulo Mateus Moura da Silva (SrMouraSilva)',
    author_email='mateus.moura@hotmail.com',
    maintainer='Paulo Mateus Moura da Silva (SrMouraSilva)',
    maintainer_email='mateus.moura@hotmail.com',

    license="Apache Software License v2",

    packages=[
        'pluginsmanager',

        'pluginsmanager/mod_host',
        'pluginsmanager/model',
        'pluginsmanager/model/lv2',
        'pluginsmanager/model/system',

        'pluginsmanager/util',
    ],
    package_data={
        'pluginsmanager/model/lv2': ['plugins.json']
    },
    install_requires=['JACK-Client'],

    test_suite='test',
    tests_require=['JACK-Client'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Multimedia :: Sound/Audio',
        'Programming Language :: Python :: 3'
    ],
    keywords='pedal-pi mod-host lv2 audio plugin-manager',

    platforms='Linux',
)
