import socket


class Connection(object):
    client = None

    def __init__(self, socket_port=5555, address='localhost'):
        self.client = socket.socket()
        self.client.connect((address, socket_port))
        self.client.settimeout(5)

    def send(self, message):
        print(message.encode('utf-8'))
        self.client.send(message.encode('utf-8'))
        received = self.client.recv(1024)

        return received
