from .connection import Connection
from .protocol_parser import ProtocolParser


class Host:

    def __init__(self, address='localhost'):
        # mod-host works only exists 2 connections:
        #  - For communication
        self.connection = Connection(5555, address)
        #  - For callback?
        self.connection_fd = Connection(5556, address)

        self.effects = []

        self.instance_index = 0

    def add(self, effect):
        """
        :param Lv2Effect effect:
        """
        effect.instance = self.instance_index
        self.instance_index += 1

        self.effects.append(effect)
        self.connection.send(ProtocolParser.add(effect))

    def remove(self, plugin):
        if plugin not in self.effects:
            raise Exception("Plugin " + plugin.uri + " has'nt added!")

        self.connection.send(ProtocolParser.remove(plugin))

    def connect_input_in(self, effect_input):
        if effect_input.effect not in self.effects:
            raise Exception("Plugin " + str(effect_input.effect) + " has'nt added!")

        self.connection.send(ProtocolParser.connect_input_in(effect_input))

    def connect_on_output(self, effect_output, index_out):
        if effect_output.effect not in self.effects:
            raise Exception("Plugin " + str(effect_output.effect) + " has'nt added!")

        self.connection.send(ProtocolParser.connect_on_output(effect_output, index_out))

    def connect(self, connection):
        if connection.output.effect not in self.effects \
        or connection.input.effect not in self.effects:
            raise Exception("An plugin has'nt added!")

        self.connection.send(ProtocolParser.connect(connection))

    def disconnect(self, connection):
        if connection.output.effect not in self.effects \
        or connection.input.effect not in self.effects:
            raise Exception("An plugin has'nt added!")

        self.connection.send(ProtocolParser.disconnect(connection))

    def set_param_value(self, param):
        if param.effect not in self.effects:
            raise Exception("Has a plugin not added!")

        self.connection.send(ProtocolParser.param_set(param))

    def set_status(self, plugin):
        if plugin not in self.effects:
            raise Exception("Has a plugin not added!")

        self.connection.send(ProtocolParser.bypass(plugin))
