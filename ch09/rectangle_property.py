class Rectangle:

    def __init__(self):
        self.width = 0
        self.height = 0

    @property
    def size(self):
        return self.width, self.height

    @size.setter
    def size(self, s):
        self.width, self.height = s
