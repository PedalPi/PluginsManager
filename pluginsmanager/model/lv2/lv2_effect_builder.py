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

import os
import json
import subprocess

from pluginsmanager.model.lv2.lv2_plugin import Lv2Plugin
from pluginsmanager.model.lv2.lv2_effect import Lv2Effect


class Lv2EffectBuilderError(Exception):
    pass


class Lv2EffectBuilder(object):
    """
    Generates lv2 audio plugins instance (as :class:`.Lv2Effect` object).

    .. note::

        In the current implementation, the data plugins are persisted
        in *plugins.json*.

    :param Path plugins_json: Plugins json path file
    :param bool ignore_unsupported_plugins: Not allows instantiation of uninstalled or unrecognized audio plugins?
    """

    plugins_json_file = os.path.dirname(os.path.abspath(__file__)) + '/plugins.json'
    """
    Informs the path of the `plugins.json` file. This file contains the lv2 plugins metadata info
    """

    def __init__(self, plugins_json=None, ignore_unsupported_plugins=True):
        self._plugins = {}

        if plugins_json is None:
            plugins_json = Lv2EffectBuilder.plugins_json_file

        with open(str(plugins_json)) as data_file:
            data = json.load(data_file)

        self.reload(data, ignore_unsupported_plugins=ignore_unsupported_plugins)

    def reload(self, metadata, ignore_unsupported_plugins=True):
        """
        Loads the metadata. They will be used so that it is possible to generate lv2 audio plugins.

        :param list metadata: lv2 audio plugins metadata
        :param bool ignore_unsupported_plugins: Not allows instantiation of uninstalled or unrecognized audio plugins?
        """
        supported_plugins = self._supported_plugins

        for plugin in metadata:
            if not ignore_unsupported_plugins \
            or plugin['uri'] in supported_plugins:
                self._plugins[plugin['uri']] = Lv2Plugin(plugin)

    @property
    def _supported_plugins(self):
        return str(subprocess.check_output(['lv2ls'])).split('\\n')

    @property
    def all(self):
        return self._plugins

    @property
    def plugins(self):
        return self._plugins.keys()

    def build(self, lv2_uri):
        """
        Returns a new :class:`.Lv2Effect` by the valid lv2_uri

        :param string lv2_uri:
        :return Lv2Effect: Effect created
        """
        try:
            plugin = self._plugins[lv2_uri]
        except KeyError:
            raise Lv2EffectBuilderError(
                "Lv2EffectBuilder not contains metadata information about the plugin '{}'. \n"
                "Try re-scan the installed plugins using the reload method::\n"
                "   >>> lv2_effect_builder.reload(lv2_effect_builder.lv2_plugins_data())".format(lv2_uri))

        return Lv2Effect(plugin)

    def lv2_plugins_data(self):
        """
        Generates a file with all plugins data info. It uses the `lilvlib`_ library.

        PluginsManager can manage lv2 audio plugins through previously obtained metadata
        from the lv2 audio plugins descriptor files.

        To speed up usage, data has been pre-generated and loaded into this piped packet.
        This avoids a dependency installation in order to obtain the metadata.

        However, this measure makes it not possible to manage audio plugins that were not
        included in the list.

        To work around this problem, this method - using the `lilvlib`_ library - can get
        the information from the audio plugins. You can use this data to generate a file
        containing the settings::

            >>> builder = Lv2EffectBuilder()
            >>> plugins_data = builder.lv2_plugins_data()

            >>> import json
            >>> with open('plugins.json', 'w') as outfile:
            >>>     json.dump(plugins_data, outfile)

        The next time you instantiate this class, you can pass the configuration file::

            >>> builder = Lv2EffectBuilder(os.path.abspath('plugins.json'))

        Or, if you want to load the data without having to create a new instance of this class::

            >>> builder.reload(builder.lv2_plugins_data())

        .. warning::

            To use this method, it is necessary that the system has the `lilv`_ in a version equal
            to or greater than `0.22.0`_. Many linux systems currently have previous versions on
            their package lists, so you need to compile them manually.

            In order to ease the work, Pedal Pi has compiled lilv for some versions of linux.
            You can get the list of .deb packages in https://github.com/PedalPi/lilvlib/releases.

            .. code-block:: bash

                # Example
                wget https://github.com/PedalPi/lilvlib/releases/download/v1.0.0/python3-lilv_0.22.1.git20160613_amd64.deb
                sudo dpkg -i python3-lilv_0.22.1+git20160613_amd64.deb


            If the architecture of your computer is not contemplated, moddevices provided
            a script to generate the package.
            Go to https://github.com/moddevices/lilvlib to get the script in its most up-to-date version.

        .. _lilvlib: https://github.com/moddevices/lilvlib
        .. _0.22.0: http://git.drobilla.net/cgit.cgi/lilv.git/tag/?id=v0.22.0
        .. _lilv: http://drobilla.net/software/lilv

        :return list: lv2 audio plugins metadata
        """
        import lilvlib

        return lilvlib.get_plugin_info_helper('')

if __name__ == '__main__':
    builder = Lv2EffectBuilder()
    print('Total plugins before reload:', len(builder.plugins))

    builder.reload(builder.lv2_plugins_data())
    print('Total plugins after reload:', len(builder.plugins))
