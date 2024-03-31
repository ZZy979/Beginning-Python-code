from socketserver import TCPServer, StreamRequestHandler


class Handler(StreamRequestHandler):

    def handle(self):
        print('Got connection from', self.client_address)
        self.wfile.write(b'Thank you for connecting')


server = TCPServer(('', 1234), Handler)
server.serve_forever()
