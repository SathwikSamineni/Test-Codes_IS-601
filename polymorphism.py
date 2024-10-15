class Shape:
    def area(self):
        pass
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

class Triangle(Shape):
    def  __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return  self.base * self.height / 2

class Square(Shape):
    def  __init__(self, side):
        self.side = side
    def  area(self):  
        return self.side ** 2


shapes = [Circle(2), Square(5), Triangle(10,20)]

for Shape in shapes:
    print(Shape.area())



