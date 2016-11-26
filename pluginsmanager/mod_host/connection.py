import socket


class Connection(object):
    """
    Class responsible for managing an API connection to the mod-host process via socket
    """
    client = None

    def __init__(self, socket_port=5555, address='localhost'):
        self.client = socket.socket()
        self.client.connect((address, socket_port))
        self.client.settimeout(5)

    def send(self, message):
        """
        Sends message to *mod-host*.

        .. note::

            Uses :class:`ProtocolParser` for a high-level management.
            As example, view :class:`Host`

        :param string message: Message that will be sent for *mod-host*
        """
        print(message.encode('utf-8'))
        self.client.send(message.encode('utf-8'))
        received = self.client.recv(1024)

        return received
