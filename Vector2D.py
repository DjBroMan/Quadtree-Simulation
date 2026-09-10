from __future__ import annotations

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self,other: Vector2D):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
    
    def scalarMult(self,num):
        self.x *= num
        self.y *= num

    def magSq(self):
        return self.x*self.x + self.y*self.y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    