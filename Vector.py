import math

class Vector:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y  # Z in this sense

    def normalize(self):
        magnitude = self.length()
        self.x /= magnitude
        self.y /= magnitude

    def length(self):
        return math.sqrt(math.pow(self[0], 2) + math.pow(self[1], 2))

    def dot(self, vector2):
        return (self.x * vector2.x) + (self.y * vector2.y)

    def __add__(self, vector2):
        return Vector(self[0] + vector2[0], self[1] + vector2[1])

    def __sub__(self, vector2):
        return Vector(self[0] - vector2[0], self[1] - vector2[1])

    def __mul__(self, scalar):
        return Vector(self[0] * scalar, self[1] * scalar)

    def __truediv__(self, scalar):
        return Vector(self[0] / scalar, self[1] / scalar)

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        return None