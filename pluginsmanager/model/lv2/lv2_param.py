from pluginsmanager.model.param import Param


class Lv2Param(Param):
    """
    Representation of a Lv2 `input control port`_ instance.

    For general input use, see :class:`Param` class documentation.

    :param Lv2Effect effect:
    :param dict param: *input control port* json representation

    .. _input control port: http://lv2plug.in/ns/lv2core/#Parameter
    """

    def __init__(self, effect, param):
        super(Lv2Param, self).__init__(effect, param['ranges']['default'])
        self._param = param

    @property
    def maximum(self):
        return self._param['ranges']['maximum']

    @property
    def minimum(self):
        return self._param['ranges']['minimum']

    @property
    def symbol(self):
        return self._param['symbol']

    @property
    def __dict__(self):
        dictionary = super(Lv2Param, self).__dict__
        dictionary['index'] = self._param['index'];

        return dictionary
