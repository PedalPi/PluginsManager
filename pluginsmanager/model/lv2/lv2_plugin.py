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


class Lv2Plugin(object):

    def __init__(self, json):
        self._json = json

    def __getitem__(self, key):
        """
        :param string key: Property key
        :return: Returns a Plugin property
        """
        return self.json[key]

    @property
    def json(self):
        """
        :return: Json decodable representation of this plugin based in moddevices `lilvlib`_.

        .. _lilvlib: https://github.com/moddevices/lilvlib
        """
        return self._json

    @property
    def data(self):
        """
        :return: Json decodable representation of this plugin based in moddevices `lilvlib`_.

        .. _lilvlib: https://github.com/moddevices/lilvlib
        """
        return self.json

    def __str__(self):
        return self['name']

    def __repr__(self):
        return "<{} object as {} at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            id(self)
        )

    @property
    def version(self):
        return '' if 'version' not in self.json else self.json['version']
