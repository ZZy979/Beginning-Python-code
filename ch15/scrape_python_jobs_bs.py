import requests
from bs4 import BeautifulSoup

text = requests.get('https://www.python.org/jobs/').text
soup = BeautifulSoup(text, 'html.parser')

for job in soup.body.section('h2'):
    print('{} ({})'.format(job.a.string, job.a['href']))
