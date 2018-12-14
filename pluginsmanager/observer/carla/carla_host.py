import sys
from pathlib import Path

from pluginsmanager.model.effect import Effect
from pluginsmanager.model.param import Param
from pluginsmanager.observer.carla.callback_manager import CallbackManager


class CarlaError(Exception):
    pass


class CarlaHost(object):

    def __init__(self, path: Path, client_name):
        self.backend = self._lazy_import(path)
        self.callback_manager = CallbackManager(self.backend)

        self.host_dll = self._init_host(path)

        self._path = path
        self.client_name = client_name

        self.pedalboard_metadata = {}

    def _lazy_import(self, path_carla: Path):
        path_carla_python = path_carla / 'source/frontend/'
        sys.path.append(path_carla_python.as_posix())

        import carla_backend as backend
        return backend

    def _init_host(self, path_carla: Path):
        path_carla_bin = path_carla / "bin"

        host = self.backend.CarlaHostDLL(path_carla_bin / "libcarla_standalone2.so", loadGlobal=False)
        host.set_engine_callback(lambda *args: self.callback_manager.callback(*args))
        host.set_engine_option(self.backend.ENGINE_OPTION_PATH_BINARIES, 0, path_carla_bin.as_posix())

        return host

    def start(self):
        if not self.host_dll.engine_init("JACK", "Pedal Pi"):
            raise CarlaError(f"Engine failed to initialize, possible reasons:\n{self.host_dll.get_last_error()}")

    def stop(self):
        self.host_dll.engine_close()

    def add_effect(self, plugin_bin, plugin_uri, effect_name, effect):
        self.pedalboard_metadata[effect] = effect_name

        if not self.host_dll.add_plugin(
                self.backend.BINARY_NATIVE, self.backend.PLUGIN_LV2,
                plugin_bin, effect_name,
                plugin_uri,
                0, None, 0x0
            ):
            raise CarlaError(f"Failed to load plugin, possible reasons:\n{self.host_dll.get_last_error()}")

    def remove_effect(self, effect: Effect):
        effect_id = self._effect_id(effect)

        if not self.host_dll.remove_plugin(effect_id):
            raise CarlaError(f"Failed to remove effect, possible reasons:\n{self.host_dll.get_last_error()}")

    def connect(self, output_port, input_port):
        output_effect_name = self.pedalboard_metadata[output_port.effect]
        output_effect_carla = self.callback_manager.elements.by_name(output_effect_name)

        input_effect_name = self.pedalboard_metadata[input_port.effect]
        input_effect_carla = self.callback_manager.elements.by_name(input_effect_name)

        output_port_carla = output_effect_carla.outputs[str(output_port)]
        input_port_carla = input_effect_carla.inputs[str(input_port)]

        if not self.host_dll.patchbay_connect(
            output_effect_carla.identifier, output_port_carla.identifier,
            input_effect_carla.identifier, input_port_carla.identifier
        ):
            raise CarlaError(f"Failed to connect effects, possible reasons:\n{self.host_dll.get_last_error()}")

    def disconnect(self, output_port, input_port):
        output_effect_name = self.pedalboard_metadata[output_port.effect]
        output_effect_carla = self.callback_manager.elements.by_name(output_effect_name)

        input_effect_name = self.pedalboard_metadata[input_port.effect]
        input_effect_carla = self.callback_manager.elements.by_name(input_effect_name)

        output_port_carla = output_effect_carla.outputs[str(output_port)]
        input_port_carla = input_effect_carla.inputs[str(input_port)]

        name = f"{output_effect_carla.identifier}:{output_port_carla.identifier}:{input_effect_carla.identifier}:{input_port_carla.identifier}"

        identifier = self.callback_manager.connections[name].identifier

        if not self.host_dll.patchbay_disconnect(identifier):
            raise CarlaError(f"Failed to disconnect effects ports, possible reasons:\n{self.host_dll.get_last_error()}")

        del self.callback_manager.connections[name]

    def set_active(self, effect: Effect, active: bool):
        effect_id = self._effect_id(effect)

        # Returns None
        self.host_dll.set_active(effect_id, active)

    def _effect_id(self, effect: Effect):
        effect_name = self.pedalboard_metadata[effect]
        effect_id = effect_name.split('_')[-1]
        return int(effect_id)

    def set_parameter_value(self, param: Param):
        effect_id = self._effect_id(param.effect)
        param_id = param.index

        # Returns None
        self.host_dll.set_parameter_value(effect_id, param_id, param.value)
