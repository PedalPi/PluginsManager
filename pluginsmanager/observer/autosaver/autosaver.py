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

from pathlib import Path

from pluginsmanager.banks_manager import BanksManager
from pluginsmanager.observer.autosaver.banks_files import BanksFiles
from pluginsmanager.observer.autosaver.index_file import IndexFile
from pluginsmanager.observer.update_type import UpdateType
from pluginsmanager.observer.updates_observer import UpdatesObserver


class Autosaver(UpdatesObserver):
    """
    The UpdatesObserver :class:`.Autosaver` allows save any changes
    automatically in json data files.
    Save all plugins changes in json files in a specified path.

    It also allows loading of saved files::

        >>> system_effect = SystemEffect('system', ('capture_1', 'capture_2'), ('playback_1', 'playback_2'))
        >>>
        >>> autosaver = Autosaver('my/path/data/')
        >>> banks_manager = autosaver.load(system_effect)

    When loads data with :class:`.Autosaver`, the autosaver
    has registered in observers of the banks_manager generated::

        >>> autosaver in banks_manager.observers
        True

    For manual registering in :class:`.BanksManager` uses
    :func:`~pluginsmanager.banks_manager.BanksManager.register()`::

        >>> banks_manager = BanksManager()
        >>> autosaver = Autosaver('my/path/data/')
        >>> autosaver in banks_manager.observers
        False
        >>> banks_manager.register(autosaver)
        >>> autosaver in banks_manager.observers
        True

    After registered, any changes in :class:`.Bank`, :class:`.Pedalboard`, :class:`.Effect`,
    :class:`~pluginsmanager.model.connection.Connection` or :class:`.Param` which belong
    to the structure of :class:`.BanksManager` instance are persisted automatically
    by :class:`.Autosaver`::

        >>> banks_manager = BanksManager()
        >>> banks_manager.register(autosaver)
        >>> my_bank = Bank('My bank')
        >>> banks_manager.append(my_bank)
        >>> # The bank will be added in banksmanger
        >>> # and now is observable (and persisted) by autosaver

    It's possible disables autosaver for saves manually::

        >>> autosaver.auto_save = False
        >>> autosaver.save(banks_manager)  # save() method saves all banks data

    :param string data_path: Path that banks will be saved (each bank in one file)
    :param bool auto_save: Auto save any change?
    """
    def __init__(self, data_path, auto_save=True):
        super().__init__()
        self.data_path = Path(data_path)

        self.index_file = IndexFile(self.data_path / Path('index_file'))
        self.banks_files = BanksFiles(self.data_path)

        self.auto_save = auto_save

    def load(self, system_effect):
        """
        Return a :class:`.BanksManager` instance contains the banks present in
        :attr:`~pluginsmanager.observer.autosaver.autosaver.Autosaver.data_path`

        :param SystemEffect system_effect: SystemEffect used in pedalboards
        :return BanksManager: :class:`.BanksManager` with banks persisted in
                :attr:`~pluginsmanager.observer.autosaver.autosaver.Autosaver.data_path`
        """
        banks = self.banks_files.load(system_effect)
        banks_ordered = self.index_file.load(banks)

        manager = BanksManager()
        manager.register(self)

        for bank in banks_ordered:
            manager.append(bank)
            bank.manager = manager

        return manager

    def save(self, banks_manager):
        """
        Save all data from a banks_manager

        :param BanksManager banks_manager: BanksManager that your banks data will be persisted
        """
        self.banks_files.delete_all_banks()
        self.banks_files.save(banks_manager)
        self.index_file.save(banks_manager)

    def on_bank_updated(self, bank, update_type, index, origin, **kwargs):
        if not self.auto_save:
            return

        if update_type == UpdateType.DELETED:
            self.banks_files.delete_bank(bank)

        elif update_type == UpdateType.CREATED:
            self.banks_files.save_bank(bank)

        elif update_type == UpdateType.UPDATED:
            self.banks_files.save_bank(bank)
            old_bank = kwargs['old']

            if old_bank.manager is None:
                self.banks_files.delete_bank(old_bank)

        self.index_file.save(origin)

    def on_pedalboard_updated(self, pedalboard, update_type, index, origin, **kwargs):
        if not self.auto_save:
            return

        if update_type == UpdateType.DELETED:
            self.banks_files.save_bank(origin)
        else:
            self.banks_files.save_bank(pedalboard.bank)

    def on_effect_updated(self, effect, update_type, index, origin, **kwargs):
        if not self.auto_save:
            return

        pedalboard = origin
        self.banks_files.save_bank(pedalboard.bank)

    def on_effect_status_toggled(self, effect, **kwargs):
        if not self.auto_save:
            return

        self.banks_files.save_bank(effect.pedalboard.bank)

    def on_param_value_changed(self, param, **kwargs):
        if not self.auto_save:
            return

        self.banks_files.save_bank(param.effect.pedalboard.bank)

    def on_connection_updated(self, connection, update_type, pedalboard, **kwargs):
        if not self.auto_save:
            return

        self.banks_files.save_bank(pedalboard.bank)
