import asyncore
from asyncore import dispatcher


class ChatServer(dispatcher): pass


s = ChatServer()
asyncore.loop()
