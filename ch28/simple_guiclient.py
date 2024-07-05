import sys
import tkinter as tk
from threading import Thread
from time import sleep
from xmlrpc.client import ServerProxy, Fault

from client import random_string, HEAD_START, SECRET_LENGTH
from server import Node, UNHANDLED


class Client(tk.Frame):

    def __init__(self, master, url, dirname, urlfile):
        super().__init__(master)
        self.node_setup(url, dirname, urlfile)
        self.pack()
        self.create_widgets()

    def node_setup(self, url, dirname, urlfile):
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

    def create_widgets(self):
        self.input = input = tk.Entry(self)
        input.pack(side='left')

        self.submit = submit = tk.Button(self)
        submit['text'] = 'Fetch'
        submit['command'] = self.fetch_handler
        submit.pack()

    def fetch_handler(self):
        query = self.input.get()
        try:
            self.server.fetch(query, self.secret)
        except Fault as f:
            if f.faultCode != UNHANDLED:
                raise
            print("Couldn't find the file", query)


def main():
    urlfile, directory, url = sys.argv[1:]

    root = tk.Tk()
    root.title('File Sharing Client')

    client = Client(root, url, directory, urlfile)
    client.mainloop()


if __name__ == '__main__':
    main()
