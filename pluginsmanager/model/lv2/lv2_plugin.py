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

    def __str__(self):
        return self['name']

    def __repr__(self):
        return "<{} ({}) at 0x{:x}>".format(
            self.__class__.__name__,
            self,
            id(self)
        )

    @property
    def json(self):
        """
        :return: JSON encodable representation of this plugin.
        """
        return self._json

    data = json

    @property
    def version(self):
        return self.json.get('version', '')
