class CallbackManager:

    def __init__(self, backend):
        self.backend = backend
        self.elements = Elements()

    def callback(self, *args):
        none, opcode, identifier, value1, value2, value3, value_str = args
        #print('Args:', args)

        if opcode == self.backend.ENGINE_CALLBACK_PATCHBAY_CLIENT_ADDED:
            element = CarlaClient(self.backend, identifier, value_str)
            self.elements[element.identifier] = element

        elif opcode == self.backend.ENGINE_CALLBACK_PATCHBAY_PORT_ADDED:
            element = self.elements[identifier]
            element.add_port(CarlaPort(self.backend, identifier=value1, name=value_str, type=value2))

        elif opcode == self.backend.ENGINE_CALLBACK_PLUGIN_ADDED \
          or opcode == self.backend.ENGINE_CALLBACK_PARAMETER_VALUE_CHANGED:
            # Audio plugin events not relevant now
            pass

        elif opcode == self.backend.ENGINE_CALLBACK_PATCHBAY_CONNECTION_ADDED \
          or opcode == self.backend.ENGINE_CALLBACK_PATCHBAY_CONNECTION_REMOVED:
            # effect connections
            pass

        elif opcode == self.backend.ENGINE_CALLBACK_ENGINE_STARTED \
          or opcode == self.backend.ENGINE_CALLBACK_ENGINE_STOPPED:
            # Relevant, but not about it implemented
            pass

        elif opcode == self.backend.ENGINE_CALLBACK_PATCHBAY_CLIENT_REMOVED \
          or opcode == self.backend.ENGINE_CALLBACK_PATCHBAY_PORT_REMOVED:
            # Occur when the engine is stoppend or a effect is removed
            pass

        else:
            print('Args:', args)


class Elements:
    def __init__(self):
        self.elements_by_id = {}
        self.elements_by_name = {}

    def __getitem__(self, item):
        return self.elements_by_id[item]

    def __setitem__(self, key, value):
        self.elements_by_id[key] = value
        self.elements_by_name[value.name] = value

    def by_name(self, name):
        return self.elements_by_name[name]


class CarlaCallbackObject:

    def __init__(self, backend, identifier, name):
        self.backend = backend
        self.identifier = identifier
        self.name = name.decode('utf-8')


class CarlaClient(CarlaCallbackObject):
    def __init__(self, backend, identifier, name):
        super().__init__(backend, identifier, name)

        self.inputs = {}
        self.outputs = {}
        self.midi_inputs = {}
        self.midi_outputs = {}

    def add_port(self, port: 'CarlaPort'):
        # https://github.com/moddevices/mod-ui/blob/master/mod/host_carla.py#L401
        if port.type & self.backend.PATCHBAY_PORT_TYPE_AUDIO:
            if port.type & self.backend.PATCHBAY_PORT_IS_INPUT:
                self.inputs[port.name] = port
            else:
                self.outputs[port.name] = port

        elif port.type & self.backend.PATCHBAY_PORT_TYPE_MIDI:
            if port.type & self.backend.PATCHBAY_PORT_IS_INPUT:
                self.midi_inputs[port.name] = port
            else:
                self.midi_outputs[port.name] = port


class CarlaPort(CarlaCallbackObject):
    def __init__(self, backend, identifier, name, type):
        super().__init__(backend, identifier, name)
        self.type = type
