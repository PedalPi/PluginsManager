import os
import json

from pluginsmanager.model.lv2.lv2_plugin import Lv2Plugin
from pluginsmanager.model.lv2.lv2_effect import Lv2Effect


class Lv2EffectBuilder(object):
    """
    Generate lv2 audio plugins instance (as :class:`Lv2Effect` object).

    .. note::

        In the current implementation, the data plugins are persisted
        in *plugins.json*.
    """

    def __init__(self, plugins_json=None):
        self.plugins = {}

        if plugins_json is None:
            plugins_json = os.path.dirname(__file__) + '/plugins.json'

        with open(plugins_json) as data_file:
            data = json.load(data_file)

        for plugin in data:
            self.plugins[plugin['uri']] = Lv2Plugin(plugin)

    @property
    def all(self):
        return self.plugins

    def build(self, lv2_uri):
        """
        Returns a new :class:`Lv2Effect` by the valid lv2_uri

        :param string lv2_uri:
        :return Lv2Effect: Effect created
        """
        return Lv2Effect(self.plugins[lv2_uri])
