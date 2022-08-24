from math import sqrt


class Point:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def dist(self, point):
        return sqrt((point.a - self.a) ** 2 + (point.b - self.b) ** 2)