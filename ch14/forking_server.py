from socketserver import ForkingTCPServer, StreamRequestHandler


class Handler(StreamRequestHandler):

    def handle(self):
        print('Got connection from', self.client_address)
        self.wfile.write(b'Thank you for connecting')


ForkingTCPServer.allow_reuse_address = True
server = ForkingTCPServer(('', 1234), Handler)
server.serve_forever()
