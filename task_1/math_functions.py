from math import hypot, ceil
import csv
from collections import namedtuple


Point = namedtuple('Point', ['x', 'y', 'color'])

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'<Vector(x={self.x}, y={self.y})>'

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(self.x or self.y)

    def __add__(self, other):
        if type(other) == Point:
            return Point(other.x+self.x, other.y+self.y)
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def __mul__(self, scalar):
        return Vector(int(self.x * scalar), int(self.y * scalar))


def export_coordinates(coordinates):
    with open('coordinates.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(('x', 'y'))
        for point in coordinates:
            writer.writerow((str(point.x), str(point.y)))


def calculate_move_vector(v, px):
    v_dots_amount = abs(v) / px
    return (v / v_dots_amount, int(v_dots_amount))
