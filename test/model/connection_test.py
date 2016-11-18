import unittest
from pluginsmanager.model.connection import Connection, ConnectionError

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder


class ConnectionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.builder = Lv2EffectBuilder()

    def test__init__(self):
        reverb = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        fuzz = self.builder.build('http://guitarix.sourceforge.net/plugins/gx_fuzzfacefm_#_fuzzfacefm_')

        connection = Connection(reverb.outputs[0], fuzz.inputs[0])

        self.assertEqual(reverb.outputs[0], connection.output)
        self.assertEqual(fuzz.inputs[0], connection.input)

    def test__init__error(self):
        reverb = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')

        with self.assertRaises(ConnectionError):
            Connection(reverb.outputs[0], reverb.inputs[0])

    def test__eq__(self):
        reverb = self.builder.build('http://calf.sourceforge.net/plugins/Reverb')
        fuzz = self.builder.build('http://guitarix.sourceforge.net/plugins/gx_fuzzfacefm_#_fuzzfacefm_')

        connection = Connection(reverb.outputs[0], fuzz.inputs[0])
        connection2 = Connection(reverb.outputs[0], fuzz.inputs[0])

        self.assertEqual(connection, connection2)
