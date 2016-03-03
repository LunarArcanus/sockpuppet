from socket import AF_INET,SOCK_STREAM
import asyncore
from .ai import BotFactory

class BotSocketHandler(asyncore.dispatcher):
    bytes_read = 1024

    def __init__(self, address=('localhost', 1337)):
        self.super().__init__(address)

    def set_addr(self, address):
        self.address = address

    def handle_read(self):
        self.buffer = self.recv(self.bytes_read)
        if not self.buffer:
            return
        else:
            message = self.buffer.decode()
            incoming_sock = self.address[0]
            response = bot_dict.get(incoming_sock).respond(message)

            self.send(bytes(response, "utf-8"))

    def handle_close(self):
        self.close()


class BotSocket(asyncore.dispatcher):
    clients = []
    _max_connections = 3
    _botdict = {}

    _kbfile = "std-startup.xml"
    _init_query = (
        "load std",
        "load other"
        )

    def __init__(self, address=('localhost', 1337), **bot_predicates):
        super().__init__()
        self.host, self.port = address
        self.create_socket(AF_INET, SOCK_STREAM)
        self.bind(address)
        self.listen(self._max_connections)
        self._predicates = bot_predicates

    def handle_accept(self):
        client = self.accept()
        BotSocket.clients.append(client)
        if not client:
            raise(Exception, "Error.")
        client_sock = client[0]
        print("Connection received: {0}:{1}".format(*client))

        bot = BotFactory()
        bot.learn(BotSocket._kbfile)
        for query in BotSocket._init_query:
            bot.respond(query)

        BotSocket._botdict.update({client_sock:bot})

        handler = BotSocketHandler(client_sock)
        handler.set_addr(client)

    def handle_close(self):
        self.close()
