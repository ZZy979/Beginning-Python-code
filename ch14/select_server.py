import select
import socket

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = ''
port = 1234
s.bind((host, port))

s.listen(5)
inputs = [s]
while True:
    rs, _, _ = select.select(inputs, [], [])
    for r in rs:
        if r is s:
            c, addr = s.accept()
            print('Got connection from', addr)
            inputs.append(c)
        else:
            try:
                data = r.recv(1024)
                disconnected = not data
            except socket.error:
                disconnected = True

            if disconnected:
                print(r.getpeername(), 'disconnected')
                inputs.remove(r)
            else:
                print(data.decode())
