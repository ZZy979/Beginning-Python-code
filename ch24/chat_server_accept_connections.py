import asyncore
from asyncore import dispatcher


class ChatServer(dispatcher):

    def handle_accept(self):
        conn, addr = self.accept()
        print('Connection attempt from', addr[0])


s = ChatServer()
s.create_socket()
s.set_reuse_addr()
s.bind(('', 5005))
s.listen(5)
asyncore.loop()
