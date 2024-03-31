from socketserver import ForkingTCPServer, StreamRequestHandler


class Handler(StreamRequestHandler):

    def handle(self):
        print('Got connection from', self.client_address)
        self.wfile.write(b'Thank you for connecting')


server = ForkingTCPServer(('', 1234), Handler)
server.serve_forever()
