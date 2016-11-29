
class Lv2Plugin(object):

    def __init__(self, json):
        self._json = json

    def __getitem__(self, key):
        """
        :param string key: Property key
        :return: Returns a Plugin property
        """
        return self.json[key]

    @property
    def json(self):
        """
        Json decodable representation of this plugin based in moddevices `lilvlib`_.

        .. _lilvlib: https://github.com/moddevices/lilvlib
        """
        return self._json

    def __str__(self):
        return self['name']

    def __repr__(self):
        return "<{} object as {} at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            id(self)
        )
