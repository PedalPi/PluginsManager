

class ProtocolParser:
    """
    Prepare the objects to
    <a href="https://github.com/moddevices/mod-host">mod-parse</a> string command
    """

    @staticmethod
    def add(effect):
        """
        add <lv2_uri> <instance_number>

        add a LV2 plugin encapsulated as a jack client
        e.g.: add http://lv2plug.in/plugins/eg-amp 0
        instance_number must be any value between 0 ~ 9999, inclusively

        :param Lv2Effect effect:
        """
        plugin = effect.plugin
        return "add {} {}".format(plugin['uri'], effect.instance)

    @staticmethod
    def remove(effect):
        """
        remove <instance_number>

        remove a LV2 plugin instance (and also the jack client)
        e.g.: remove 0
        """
        return 'remove {}'.format(effect.instance)

    @staticmethod
    def connect_input_in(effect_input, index_in=1):
        """
        Connect system input (indexed in 'index_in') in 'plugin'
        """
        return ProtocolParser._connect_message(
            'system:capture_{}'.format(index_in),
            ProtocolParser._get_in_name_of(effect_input)
        )

    @staticmethod
    def connect_on_output(effect_output, index_out=1):
        """
        Connect 'plugin' on system output indexed in 'index_out'
        """
        return ProtocolParser._connect_message(
            ProtocolParser._get_out_name_of(effect_output),
            'system:playback_{}'.format(index_out)
        )

    @staticmethod
    def connect(connection):
        """
        connect <origin_port> <destination_port>

        connect two plugin audio ports
        e.g.: connect system:capture_1 plugin_0:in
        """
        return ProtocolParser._connect_message(
            ProtocolParser._get_out_name_of(connection.output),
            ProtocolParser._get_in_name_of(connection.input)
        )

    @staticmethod
    def _connect_message(origin_port, destination_port):
        return 'connect {} {}'.format(origin_port, destination_port)

    @staticmethod
    def _get_out_name_of(effect_output):
        effect = effect_output.effect
        symbol = effect_output._output['symbol']

        return 'effect_{}:{}'.format(effect.instance, symbol)

    @staticmethod
    def _get_in_name_of(effect_input):
        effect = effect_input.effect
        symbol = effect_input._input['symbol']

        return 'effect_{}:{}'.format(effect.instance, symbol)

    @staticmethod
    def disconnect(connection):
        """
        disconnect <origin_port> <destination_port>

        disconnect two plugin audio ports
        e.g.: disconnect system:capture_1 plugin_0:in
        """
        return 'disconnect {} {}'.format(
            ProtocolParser._get_out_name_of(connection.output),
            ProtocolParser._get_in_name_of(connection.input)
        )

    @staticmethod
    def preset_load():
        """
        preset_load <instance_number> <preset_uri>

        load a preset state to given plugin instance
        e.g.: preset_load 0 "http://drobilla.net/plugins/mda/presets#JX10-moogcury-lite"
        """
        return None

    @staticmethod
    def preset_save():
        """
        preset_save <instance_number> <preset_name> <dir> <file_name>

        save a preset state from given plugin instance
        e.g.: preset_save 0 "My Preset" /home/user/.lv2/my-presets.lv2 mypreset.ttl
        """
        return None

    @staticmethod
    def preset_show():
        """
        preset_show <instance_number> <preset_uri>

        show the preset information of requested instance / URI
        e.g.: preset_show 0 http://drobilla.net/plugins/mda/presets#EPiano-bright
        """
        return None

    @staticmethod
    def param_set(param):
        """
        param_set <instance_number> <param_symbol> <param_value>

        set a value to given control
        e.g.: param_set 0 gain 2.50

        :param Lv2Param param:
        """
        instance = param.effect
        symbol = param._param['symbol']
        value = str(param.value)

        return 'param_set {} {} {}'.format(instance, symbol, value)

    @staticmethod
    def param_get(plugin, param):
        """
        param_get <instance_number> <param_symbol>

        get the value of the request control
        e.g.: param_get 0 gain
        """
        return 'param_get {} {}'.format(plugin, param['symbol'])

    @staticmethod
    def param_monitor():
        """
        param_monitor <instance_number> <param_symbol> <cond_op> <value>

        do monitoring a plugin instance control port according given condition
        e.g: param_monitor 0 gain > 2.50
        """
        return None

    @staticmethod
    def monitor():
        """
        monitor <addr> <port> <status>

        open a socket port to monitoring parameters
        e.g: monitor localhost 12345 1
        if status = 1 start monitoring
        if status = 0 stop monitoring
        """
        return None

    @staticmethod
    def midi_learn(self, plugin, param):
        """
        midi_learn <instance_number> <param_symbol>

        This command maps starts MIDI learn for a parameter
        e.g.: midi_learn 0 gain
        """
        pass

    @staticmethod
    def midi_map(plugin, param, midi_chanel, midi_cc):
        """
        midi_map <instance_number> <param_symbol> <midi_channel> <midi_cc>

        This command maps a MIDI controller to a parameter
        e.g.: midi_map 0 gain 0 7
        """
        pass

    @staticmethod
    def midi_unmap(plugin, param):
        """
        midi_unmap <instance_number> <param_symbol>

        This command unmaps the MIDI controller from a parameter
        e.g.: unmap 0 gain
        """

    @staticmethod
    def bypass(effect):
        """
        bypass <instance_number> <bypass_value>

        toggle plugin processing
        e.g.: bypass 0 1
        if bypass_value = 1 bypass plugin
        if bypass_value = 0 process plugin
        """
        return 'bypass {} {}'.format(
            effect.instance,
            1 if effect.active else 0
        )

    @staticmethod
    def load(filename):
        """
        load <file_name>

        load a history command file
        dummy way to save/load workspace state
        e.g.: load my_setup
        """
        return 'load {}'.format(filename)

    @staticmethod
    def save(filename):
        """
        save <file_name>

        saves the history of typed commands
        dummy way to save/load workspace state
        e.g.: save my_setup
        """
        return 'save '.format(filename)

    @staticmethod
    def help():
        """
        help

        show a help message
        """
        return 'help'

    @staticmethod
    def quit():
        """
        quit

        bye!
        """
        return 'quit'
