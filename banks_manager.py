from model.updates_observer import UpdatesObserver


class BanksManager(object):
    """
    :param dict data:
    """

    def __init__(self, data=None):
        self.banks = []
        self.observer_manager = ObserverManager()

        data = {'banks': []} if data is None else data
        #for bank_data in data['banks']:
        #    self.banks.append(bank_data)

    def register(self, observer):
        self.observer_manager.append(observer)

    def append(self, bank):
        bank.observer = self.observer_manager


class ObserverManager(UpdatesObserver):
    def __init__(self):
        super(ObserverManager, self).__init__()
        self.observers = []

    def append(self, observer):
        self.observers.append(observer)

    def on_current_patch_change(self, patch, token=None):
        for observer in self.observers:
            observer.on_current_patch_change(patch, token)

    def on_bank_update(self, bank, update_type, token=None):
        for observer in self.observers:
            observer.on_bank_update(bank, update_type, token)

    def on_patch_updated(self, patch, update_type, token=None):
        for observer in self.observers:
            observer.on_patch_updated(patch, update_type, token)

    def on_effect_updated(self, effect, update_type, token=None):
        for observer in self.observers:
            observer.on_effect_updated(effect, update_type, token)

    def on_effect_status_toggled(self, effect, token=None):
        for observer in self.observers:
            observer.on_effect_status_toggled(effect, token)

    def on_param_value_changed(self, param, token=None):
        for observer in self.observers:
            observer.on_param_value_changed(param, token)

    def on_connection_updated(self, connection, update_type, token=None):
        for observer in self.observers:
            observer.on_connection_updated(connection, update_type, token)
