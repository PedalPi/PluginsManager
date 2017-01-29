from pluginsmanager.model.updates_observer import UpdatesObserver
from pluginsmanager.model.update_type import UpdateType

import json
import asyncio
import os


class Autosaver(UpdatesObserver):
    """
    Save all plugins changes in json files in a specified path.

    :param string data_path: Path that banks (one in one file)
    """
    def __init__(self, data_path):
        self.data_path = data_path

    def bank_path(self, bank):
        """
        :param Bank bank:
        :return string: Bank path .json
        """
        return self.data_path + bank.uuid + ".json"

    def save(self, bank):
        """
        Save the bank in your current path
        :param Bank bank: Bank that will be saved
        """
        bank.index = bank.manager.banks.index(bank)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(Autosaver._save(self.bank_path(bank), bank.json))

    def delete(self, bank):
        """
        Delete the bank's file
        :param Bank bank: Bank that will be removed
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(Autosaver._delete(self.bank_path(bank)))

    @staticmethod
    @asyncio.coroutine
    def _save(url, data):
        json_file = open(url, "w+")
        json_file.write(json.dumps(data))
        json_file.close()

    @staticmethod
    @asyncio.coroutine
    def _delete(url):
        os.remove(url)

    def on_bank_updated(self, bank, update_type, origin=None, **kwargs):
        if update_type == UpdateType.DELETED:
            return self.delete(bank)

        self.save(bank)

    def on_pedalboard_updated(self, pedalboard, update_type, origin=None, **kwargs):
        if update_type == UpdateType.DELETED:
            self.save(origin)
        else:
            self.save(pedalboard.bank)

    def on_effect_updated(self, effect, update_type, **kwargs):
        self.save(effect.pedalboard.bank)

    def on_effect_status_toggled(self, effect):
        self.save(effect.pedalboard.bank)

    def on_param_value_changed(self, param):
        self.save(param.effect.pedalboard.bank)

    def on_connection_updated(self, connection, update_type):
        print(connection)
        self.save(connection.output.effect.pedalboard.bank)
