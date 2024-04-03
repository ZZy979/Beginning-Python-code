import socket

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = ''
port = 1234
s.bind((host, port))

s.listen(5)
while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    c.send(b'Thank you for connecting')
    c.close()
