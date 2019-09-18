from math import hypot
import csv

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(self.x or self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)


    def __div__(self, scalar):
        return Vector(self.x // scalar, self.y // scalar)

def export_coordinates(coordinates):
    with open('coordinates.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(('x', 'y'))
        for point in coordinates:
            writer.writerow((str(point.x), str(point.y)))
