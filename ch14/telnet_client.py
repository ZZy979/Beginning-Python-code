import sys
from telnetlib import Telnet

with Telnet('localhost', 1234) as tn:
    tn.write(sys.stdin.read().encode())
