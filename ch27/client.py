import sys
from cmd import Cmd
from random import choices
from string import ascii_lowercase
from threading import Thread
from time import sleep
from xmlrpc.client import ServerProxy, Fault

from server import Node, UNHANDLED

HEAD_START = 0.1  # Seconds
SECRET_LENGTH = 100


def random_string(length):
    """
    Returns a random string of letters with the given length.
    """
    return ''.join(choices(ascii_lowercase, k=length))


class Client(Cmd):
    """
    A simple text-based interface to the Node class.
    """

    prompt = '> '

    def __init__(self, url, dirname, urlfile):
        """
        Sets the url, dirname, and urlfile, and starts the Node
        Server in a separate thread.
        """
        super().__init__()
        self.secret = random_string(SECRET_LENGTH)
        n = Node(url, dirname, self.secret)
        t = Thread(target=n._start)
        t.daemon = True
        t.start()
        # Give the server a head start:
        sleep(HEAD_START)
        self.server = ServerProxy(url)
        for line in open(urlfile):
            self.server.hello(line.strip())

    def do_fetch(self, arg):
        """Call the fetch method of the Server."""
        try:
            self.server.fetch(arg, self.secret)
        except Fault as f:
            if f.faultCode != UNHANDLED:
                raise
            print("Couldn't find the file", arg)

    def do_exit(self, arg):
        """Exit the program."""
        print()
        sys.exit()

    do_EOF = do_exit  # End-Of-File is synonymous with 'exit'


def main():
    urlfile, directory, url = sys.argv[1:]
    client = Client(url, directory, urlfile)
    client.cmdloop()


if __name__ == '__main__':
    main()
