
class Lv2Plugin(object):

    def __init__(self, json):
        self._json = json

    def __getitem__(self, key):
        """
        :param string key: Property key
        :return: Returns a Plugin property
        """
        return self._json[key]

    def __str__(self):
        return self['name']

    def __repr__(self):
        return "<{} object as {} at 0x{:x}>".format(
            self.__class__.__name__,
            str(self),
            id(self)
        )
