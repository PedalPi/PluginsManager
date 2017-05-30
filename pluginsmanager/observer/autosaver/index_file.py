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

from pluginsmanager.observer.autosaver.persistence import Persistence


class IndexFile(object):

    def __init__(self, path):
        """
        :param Path path: Index file path
        """
        self.path = path

    def load(self, indexables):
        """
        Load the index file and reorder the banks based in order listed in index

        :param list[Indexable] indexables: Banks that will be reordered based in index file
        :return list[Bank]: Banks reordered
        """
        try:
            data = Persistence.read(self.path, create_file=True)
        except ValueError:
            data = {}

        return self.load_data(data, indexables)

    def load_data(self, json_data, indexables):
        new_list = []
        indexables_hash = {uuid: bank for (uuid, bank) in map(lambda bank: (bank.uuid, bank), indexables)}

        for indexable in json_data:
            if indexable['uuid'] in indexables_hash:
                new_list.append(indexables_hash[indexable['uuid']])
                del indexables_hash[indexable['uuid']]

        return new_list + sorted(indexables_hash.values(), key=lambda indexable: indexable.simple_identifier)

    def save(self, indexables):
        data = self.generate_data(indexables)
        Persistence.save(self.path, data)

    def generate_data(self, indexables):
        data = []

        for index, indexable in enumerate(indexables):
            item = self.generate_index_data(index, indexable)
            data.append(item)

        return data

    def generate_index_data(self, index, indexable):
        item = {
            'index': index,
            'uuid': indexable.uuid,
            'identifier': indexable.simple_identifier
        }
        return item

