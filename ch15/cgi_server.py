from http.server import ThreadingHTTPServer, CGIHTTPRequestHandler

server = ThreadingHTTPServer(('', 8000), CGIHTTPRequestHandler)
server.serve_forever()
