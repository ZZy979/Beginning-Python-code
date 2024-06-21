import asyncore
from asyncore import dispatcher

PORT = 5005


class ChatServer(dispatcher):

    def __init__(self, port):
        super().__init__()
        self.create_socket()
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)

    def handle_accept(self):
        conn, addr = self.accept()
        print('Connection attempt from', addr[0])


if __name__ == '__main__':
    s = ChatServer(PORT)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass
