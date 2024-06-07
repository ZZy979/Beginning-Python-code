from xml.sax import ContentHandler, parse


class TestHandler(ContentHandler):

    def startElement(self, name, attrs):
        print(name, attrs.keys())


if __name__ == '__main__':
    parse('website.xml', TestHandler())
