from pluginsmanager.mod_host.connection import Connection
from pluginsmanager.mod_host.protocol_parser import ProtocolParser


class Host:

    def __init__(self, address='localhost'):
        # mod-host works only exists 2 connections:
        #  - For communication
        self.connection = Connection(5555, address)
        #  - For callback?
        self.connection_fd = Connection(5556, address)

        self.instance_index = 0

    def add(self, effect):
        """
        :param Lv2Effect effect:
        """
        effect.instance = self.instance_index
        self.instance_index += 1

        self.connection.send(ProtocolParser.add(effect))

    def remove(self, effect):
        self.connection.send(ProtocolParser.remove(effect))

    def connect_input_in(self, effect_input):
        self.connection.send(ProtocolParser.connect_input_in(effect_input))

    def connect_on_output(self, effect_output, index_out):
        self.connection.send(ProtocolParser.connect_on_output(effect_output, index_out))

    def connect(self, connection):
        self.connection.send(ProtocolParser.connect(connection))

    def disconnect(self, connection):
        self.connection.send(ProtocolParser.disconnect(connection))

    def set_param_value(self, param):
        self.connection.send(ProtocolParser.param_set(param))

    def set_status(self, plugin):
        self.connection.send(ProtocolParser.bypass(plugin))
