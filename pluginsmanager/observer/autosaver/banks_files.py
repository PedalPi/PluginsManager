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

from glob import glob
from pathlib import Path

from pluginsmanager.observer.autosaver.persistence import Persistence
from pluginsmanager.util.persistence_decoder import PersistenceDecoder


class BanksFiles(object):

    def __init__(self, data_path):
        """
        :param Path data_path: Path that contains the banks
        """
        self.data_path = data_path

    def load(self, system_effect):
        """
        Return a list if banks presents in data_path

        :param SystemEffect system_effect: SystemEffect used in pedalboards
        :return list[Bank]: List with Banks persisted in
                :attr:`~pluginsmanager.observer.autosaver.banks_files.BanksFiles.data_path`
        """
        persistence = PersistenceDecoder(system_effect)

        banks = []

        for file in glob(str(self.data_path) + "/*.json"):
            bank = persistence.read(Persistence.read(file))
            bank._uuid = file.split('/')[-1].split('.json')[0]
            banks.append(bank)

        return banks

    def save(self, banks_manager):
        for bank in banks_manager:
            self.save_bank(bank)

    def save_bank(self, bank):
        """
        Save the bank in your file

        :param Bank bank: Bank that will be persisted
        """
        path = self._bank_path(bank)
        Persistence.save(path, bank.json)

    def delete_bank(self, bank):
        """
        Delete the bank's file

        :param Bank bank: Bank that will be removed
        """
        path = self._bank_path(bank)
        Persistence.delete(path)

    def delete_all_banks(self):
        """
        Delete all banks files.

        Util for manual save, because isn't possible know which banks
        were removed
        """
        for file in glob(str(self.data_path) + "/*.json"):
            Persistence.delete(file)

    def _bank_path(self, bank):
        """
        :param Bank bank: Bank that will be generate your path

        :return string: Bank path .json
        """
        return self.data_path / Path('{}.json'.format(bank.uuid))
