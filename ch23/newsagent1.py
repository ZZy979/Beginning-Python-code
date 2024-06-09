from base64 import b64decode
from nntplib import NNTP

servername = 'freenews.netfront.net'
group = 'comp.lang.python.announce'
server = NNTP(servername)
howmany = 10

resp, count, first, last, name = server.group(group)

start = last - howmany + 1

resp, overviews = server.over((start, last))

for id, over in overviews:
    subject = over['subject']
    resp, head_info = server.head(id)
    is_base64 = b'Content-Transfer-Encoding: base64' in head_info.lines
    resp, info = server.body(id)
    print(subject)
    print('-' * len(subject))
    for line in info.lines:
        if is_base64:
            print(b64decode(line).decode('latin1').replace('\r', ''), end='')
        else:
            print(line.decode('latin1'))
    print()

server.quit()
