import json
from nntplib import NNTP

server = NNTP('freenews.netfront.net')
d = {}

resp, count, first, last, name = server.group('comp.lang.python.announce')
d['group'] = {'response': resp, 'count': count, 'first': first, 'last': last, 'name': name}

resp, overviews = server.over((last - 9, last))
d['over'] = {'response': resp, 'overviews': overviews}

ad = d['article'] = {}
for id, _ in overviews:
    resp, info = server.article(id)
    lines = [line.decode() for line in info.lines]
    ad[id] = {'response': resp, 'info': {'number': info.number, 'message_id': info.message_id, 'lines': lines}}

with open('nntp_response.json', 'w') as f:
    json.dump(d, f)
