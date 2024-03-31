import socket
import sys
from telnetlib import Telnet

with Telnet(socket.gethostname(), 1234) as tn:
    tn.write(sys.stdin.read().encode())
