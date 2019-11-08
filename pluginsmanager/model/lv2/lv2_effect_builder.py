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

import logging
import json
from os.path import abspath, dirname, join

import lilv

from pluginsmanager.model.lv2.lv2_effect import Lv2Effect
from pluginsmanager.model.lv2.lv2_plugin import Lv2Plugin
from pluginsmanager.model.lv2.lv2_plugin_info import get_plugins_info


log = logging.getLogger(__name__)


class Lv2EffectBuilderError(Exception):
    pass


class Lv2EffectBuilder(object):
    """Generate LV2 plugin instances (as :class:`.Lv2Effect` object).

    .. note::

        In the current implementation, the plugins metatdata is cached
        in the file *plugins.json* inside the package
        :mod:`pluginsmanager.model.lv2`.

    :param Path plugins_json: Plugins json path file
    :param bool allow_uninstalled_plugins: allow instantiation of uninstalled
        or unrecognized audio plugins?

    """

    plugins_json_file = join(dirname(abspath(__file__)), 'plugins.json')
    """
    Stores the path of the `plugins.json` file. This file contains the LV2 plugins metadata.
    """

    def __init__(self, plugins_json=None, allow_uninstalled_plugins=False):
        self._plugins = {}
        self._lilv_world = None
        self._installed_plugins = None

        if plugins_json is None:
            plugins_json = Lv2EffectBuilder.plugins_json_file

        with open(str(plugins_json)) as data_file:
            data = json.load(data_file)

        self.reload(data, allow_uninstalled_plugins=allow_uninstalled_plugins)

    def reload(self, metadata, allow_uninstalled_plugins=False):
        """Load data of all LV2 plugins listed in given metadata.

        :param list metadata: LV2 plugins metadata
        :param bool allow_uninstalled_plugins: allow instantiation of
            uninstalled or unrecognized audio plugins?

        """
        installed_plugins = set(self.installed_plugins)
        log.debug("Installed plugins: %r", installed_plugins)

        for plugin in metadata:
            uri = plugin['uri']
            msg = "Checking for '%s'... %s"
            if allow_uninstalled_plugins or uri in installed_plugins:
                self._plugins[uri] = Lv2Plugin(plugin)
                log.info(msg, uri, "found")
            else:
                log.info(msg, uri, "NOT found")

    @property
    def installed_plugins(self):
        if self._lilv_world is None:
            self._lilv_world = lilv.World()

        if self._installed_plugins is None:
            log.info("Discovering installed plugins...")
            self._lilv_world.load_all()
            self._installed_plugins = [str(p.get_uri())
                                       for p in self._lilv_world.get_all_plugins()]

        return self._installed_plugins

    @property
    def all(self):
        return self._plugins

    @property
    def plugins(self):
        return self._plugins.keys()

    def build(self, lv2_uri):
        """Return a new :class:`.Lv2Effect` instance given by lv2_uri.

        :param string lv2_uri:
        :return Lv2Effect: Effect created
        :raises Lv2EffectBuilderError: plugin with given lv2_uri was not found

        """
        try:
            plugin = self._plugins[lv2_uri]
        except KeyError:
            raise Lv2EffectBuilderError(
                "Lv2EffectBuilder does not have metadata information about the plugin '{}'.\n"
                "Try re-scanning the installed plugins using the reload method:\n\n"
                "   >>> lv2_effect_builder.reload(lv2_effect_builder.lv2_plugins_data())"
                .format(lv2_uri))

        return Lv2Effect(plugin)

    def lv2_plugins_data(self):
        """Generate metadata with information about all installed LV2 plugins.

        PluginsManager can only use LV2 plugins it knows about, i.e. those, about which it has
        stored metadata, which was generated from the LV2 TTL descriptor files of the installed
        plugins.

        To speed up usage, the metadata is pre-generated and stored as JSON data in a file in
        the package. The cached data is loaded from this file into this class on instantiation.
        This reduces the loading time considerably, especially if there are many (i.e. hundreds of)
        LV2 plugins installed.

        However, this makes it impossible to use plugins that were not installed when the meta
        data cache file was generated.

        So in order to use all installed plugins, you have to generate a new plugin metadata cache
        file with::

            >>> import json
            >>> builder = Lv2EffectBuilder()
            >>> plugins_data = builder.lv2_plugins_data()
            >>> with open('plugins.json', 'w') as outfile:
            >>>     json.dump(plugins_data, outfile)

        The next time you instantiate this class, you can pass the path of the cache file like
        this::

            >>> builder = Lv2EffectBuilder('plugins.json')

        Or, to generate the data on-the-fly and load it into an existing instance of this class
        (this may take a while), do this::

            >>> builder.reload(builder.lv2_plugins_data())

        .. warning::

            To query the plugin metadata, the Python bindings for the `lilv`_ C library are used.
            This requires lilv version `>= 0.24.0`.

        .. _lilv: http://drobilla.net/software/lilv

        :return list: lv2 audio plugins metadata

        """
        log.info("Scanning metadata of installed plugins...")
        return get_plugins_info()


if __name__ == '__main__':
    import sys

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if len(sys.argv) >= 2:
        cache_path = sys.argv[1]
    else:
        cache_path = join(abspath(dirname(__file__)), 'plugins.json')

    builder = Lv2EffectBuilder()
    log.info('Total plugins before re-scan: %i', len(builder.plugins))

    plugins_data = builder.lv2_plugins_data()
    builder.reload(plugins_data)
    log.info('Total plugins after re-scan: %i', len(builder.plugins))

    with open(cache_path, 'w') as outfile:
         json.dump(plugins_data, outfile, sort_keys=True)
