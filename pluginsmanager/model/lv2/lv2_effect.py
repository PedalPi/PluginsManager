from pluginsmanager.model.effect import Effect
from pluginsmanager.model.lv2.lv2_param import Lv2Param
from pluginsmanager.model.lv2.lv2_input import Lv2Input
from pluginsmanager.model.lv2.lv2_output import Lv2Output


class Lv2Effect(Effect):
    """
    Representation of a Lv2 audio plugin instance.

    Effect contains a `active` status (off=bypass), a list of :class:`Param`,
    a list of :class:`Input` and a list of :class:`Connection`

    :param Lv2Plugin plugin:
    """

    def __init__(self, plugin):
        super(Lv2Effect, self).__init__()

        self.plugin = plugin

        self._params = tuple([Lv2Param(self, param) for param in plugin["ports"]["control"]["input"]])
        self._inputs = tuple([Lv2Input(self, effect_input) for effect_input in plugin['ports']['audio']['input']])
        self._outputs = tuple([Lv2Output(self, effect_output) for effect_output in plugin['ports']['audio']['output']])

        self.instance = None

    @property
    def params(self):
        """
        :return list[Param]: Params of effect
        """
        return self._params

    @property
    def inputs(self):
        """
        :return list[Input]: Inputs of effect
        """
        return self._inputs

    @property
    def outputs(self):
        """
        :return list[Output]: Outputs of effect
        """
        return self._outputs

    def __str__(self):
        return str(self.plugin)

    def __repr__(self):
        return "<{} object as '{}'{} active at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            '' if self.active else 'not',
            id(self)
        )

    @property
    def __dict__(self):
        return {
            'technology': 'lv2',
            'plugin': self.plugin['uri'],
            'active': self.active,
            'params': [param.json for param in self.params],
        }
