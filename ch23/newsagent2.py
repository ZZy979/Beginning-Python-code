import re
import textwrap
from base64 import b64decode
from nntplib import NNTP, decode_header
from urllib.request import urlopen


class NewsAgent:
    """
    An object that can distribute news items from news sources to news
    destinations.
    """

    def __init__(self):
        self.sources = []
        self.destinations = []

    def add_source(self, source):
        self.sources.append(source)

    def add_destination(self, dest):
        self.destinations.append(dest)

    def distribute(self):
        """
        Retrieve all news items from all sources, and Distribute them to all
        destinations.
        """
        items = []
        for source in self.sources:
            items.extend(source.get_items())
        for dest in self.destinations:
            dest.receive_items(items)


class NewsItem:
    """
    A simple news item consisting of a title and body text.
    """

    def __init__(self, title, body):
        self.title = title
        self.body = body


class NNTPSource:
    """
    A news source that retrieves news items from an NNTP group.
    """

    def __init__(self, servername, group, howmany):
        self.servername = servername
        self.group = group
        self.howmany = howmany

    def get_items(self):
        server = NNTP(self.servername)
        resp, count, first, last, name = server.group(self.group)
        start = last - self.howmany + 1
        resp, overviews = server.over((start, last))
        for id, over in overviews:
            title = decode_header(over['subject'])
            resp, head_info = server.head(id)
            is_base64 = b'Content-Transfer-Encoding: base64' in head_info.lines
            resp, info = server.body(id)
            if is_base64:
                body = ''.join(b64decode(line).decode('latin1').replace('\r', '') for line in info.lines) + '\n\n'
            else:
                body = '\n'.join(line.decode('latin1') for line in info.lines) + '\n\n'
            yield NewsItem(title, body)
        server.quit()


class SimpleWebSource:
    """
    A news source that extracts news items from a web page using regular
    expressions.
    """

    def __init__(self, url, title_pattern, body_pattern, encoding='utf8'):
        self.url = url
        self.title_pattern = re.compile(title_pattern)
        self.body_pattern = re.compile(body_pattern)
        self.encoding = encoding

    def get_items(self):
        text = urlopen(self.url).read().decode(self.encoding)
        titles = self.title_pattern.findall(text)
        bodies = self.body_pattern.findall(text)
        for title, body in zip(titles, bodies):
            yield NewsItem(title, textwrap.fill(body) + '\n')


class PlainDestination:
    """
    A news destination that formats all its news items as plain text.
    """

    def receive_items(self, items):
        for item in items:
            print(item.title)
            print('-' * len(item.title))
            print(item.body,)


class HTMLDestination:
    """
    A news destination that formats all its news items as HTML.
    """

    def __init__(self, filename):
        self.filename = filename

    def receive_items(self, items):
        out = open(self.filename, 'w', encoding='utf8')
        print("""
        <html>
          <head>
            <title>Today's News</title>
          </head>
          <body>
          <h1>Today's News</h1>
        """, file=out)

        print('<ul>', file=out)
        for id, item in enumerate(items, start=1):
            print('  <li><a href="#{}">{}</a></li>'.format(id, item.title), file=out)
        print('</ul>', file=out)

        for id, item in enumerate(items, start=1):
            print('<h2><a id="{}">{}</a></h2>'.format(id, item.title), file=out)
            print('<pre>{}</pre>'.format(item.body), file=out)

        print("""
          </body>
        </html>
        """, file=out)


def run_default_setup():
    """
    A default setup of sources and destination. Modify to taste.
    """
    agent = NewsAgent()

    # A SimpleWebSource that retrieves news from NBC News:
    nbc_news_url = 'https://www.nbcnews.com/world'
    nbc_news_title = r'<h2 class="wide-tease-item__headline" data-testid="wide-tease-headline">(.*?)</h2>'
    nbc_news_body = r'<div class="wide-tease-item__description" data-testid="wide-tease-dek">(.*?)</div>'
    nbc_news = SimpleWebSource(nbc_news_url, nbc_news_title, nbc_news_body)

    agent.add_source(nbc_news)

    # An NNTPSource that retrieves news from comp.lang.python.announce:
    clpa_server = 'freenews.netfront.net'
    clpa_group = 'comp.lang.python.announce'
    clpa_howmany = 10
    clpa = NNTPSource(clpa_server, clpa_group, clpa_howmany)

    agent.add_source(clpa)

    # Add plain-text destination and an HTML destination:
    agent.add_destination(PlainDestination())
    agent.add_destination(HTMLDestination('news.html'))

    # Distribute the news items:
    agent.distribute()


if __name__ == '__main__':
    run_default_setup()
