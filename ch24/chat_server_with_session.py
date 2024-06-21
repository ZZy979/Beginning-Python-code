import asyncore
from asynchat import async_chat
from asyncore import dispatcher

PORT = 5005


class ChatSession(async_chat):

    def __init__(self, sock):
        super().__init__(sock)
        self.set_terminator(b'\r\n')
        self.data = []

    def collect_incoming_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        line = b''.join(self.data)
        self.data = []
        # Do something with the line...
        print(line.decode())


class ChatServer(dispatcher):

    def __init__(self, port):
        super().__init__()
        self.create_socket()
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
        self.sessions = []

    def handle_accept(self):
        conn, addr = self.accept()
        self.sessions.append(ChatSession(conn))


if __name__ == '__main__':
    s = ChatServer(PORT)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print()
