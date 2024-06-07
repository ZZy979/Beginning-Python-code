from xml.sax import ContentHandler, parse


class HeadlineHandler(ContentHandler):
    in_headline = False

    def __init__(self, headlines):
        super().__init__()
        self.headlines = headlines
        self.data = []

    def startElement(self, name, attrs):
        if name == 'h1':
            self.in_headline = True

    def endElement(self, name):
        if name == 'h1':
            text = ''.join(self.data)
            self.data = []
            self.headlines.append(text)
            self.in_headline = False

    def characters(self, content):
        if self.in_headline:
            self.data.append(content)


if __name__ == '__main__':
    headlines = []
    parse('website.xml', HeadlineHandler(headlines))

    print('The following <h1> elements were found:')
    for h in headlines:
        print(h)
