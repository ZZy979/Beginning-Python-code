import re

import requests

p = re.compile(r'<a href="(/jobs/\d+/)">(.*?)</a>')
text = requests.get('https://www.python.org/jobs/').text
for url, name in p.findall(text):
    print(f'{name} ({url})')
