from abc import abstractmethod


class Shape:

    @abstractmethod
    def draw(self):
        pass

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, c):
        self._color = c


class Rectangle(Shape):

    def __init__(self, top_left, width, height):
        self.top_left = top_left
        self.width = width
        self.height = height

    def draw(self):
        print(f'Draw a {self.color.name} rectangle: top left {self.top_left}, width {self.width}, height {self.height}')


class Circle(Shape):

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def draw(self):
        print(f'Draw a {self.color.name} circle: center {self.center}, radius {self.radius}')
