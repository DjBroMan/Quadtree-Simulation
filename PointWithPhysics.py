from __future__ import annotations
from Point import Point
from Vector2D import Vector2D
from Quadtree import Rectangle

class PointWithPhysics(Point):
    def __init__(self, cord, r):
        super().__init__(cord, r)
        self.vel = Vector2D(0,0)
        self.acc = Vector2D(0,0)

    def setVelocity(self,x,y):
        self.vel = Vector2D(x,y)

    def setAcceleration(self,x,y):
        self.acc = Vector2D(x,y)

    def update(self):
        self.vel += self.acc
        self.pos += self.vel
    
    def bounce(self, area: Rectangle) -> None:
        """
        Bounce when the EDGE of the circle touches the boundary
        """
        x, y, w, h = area

        # -------- RIGHT WALL --------
        if self.pos.x + self.r >= x + w:
            self.pos.x = x + w - self.r
            self.vel.x *= -1

        # -------- LEFT WALL --------
        elif self.pos.x - self.r <= x:
            self.pos.x = x + self.r
            self.vel.x *= -1

        # -------- BOTTOM WALL --------
        if self.pos.y + self.r >= y + h:
            self.pos.y = y + h - self.r
            self.vel.y *= -1

        # -------- TOP WALL --------
        elif self.pos.y - self.r <= y:
            self.pos.y = y + self.r
            self.vel.y *= -1
            
    def collide(self, other: "PointWithPhysics") -> None:
        if self is other:
            return

        # Vector from other → self
        dx = self.pos.x - other.pos.x
        dy = self.pos.y - other.pos.y

        dist_sq = dx * dx + dy * dy
        min_dist = self.r + other.r

        # No collision
        if dist_sq == 0:
            return  # avoid division by zero

        if dist_sq < min_dist * min_dist:
            dist = dist_sq ** 0.5

            # 🧠 Normalized direction
            nx = dx / dist
            ny = dy / dist

            # 📏 Overlap amount
            overlap = min_dist - dist

            # 🚀 Push both points away equally
            self.pos.x += nx * (overlap / 2)
            self.pos.y += ny * (overlap / 2)

            other.pos.x -= nx * (overlap / 2)
            other.pos.y -= ny * (overlap / 2)

            # -------- VELOCITY RESPONSE --------

            # Relative velocity
            rvx = self.vel.x - other.vel.x
            rvy = self.vel.y - other.vel.y

            # Velocity along normal
            vel_along_normal = rvx * nx + rvy * ny

            # If moving away → ignore
            if vel_along_normal > 0:
                return

            # Assume equal mass (m1 = m2 = 1)
            # Elastic collision → restitution = 1
            restitution = 1

            # Impulse scalar
            j = -(1 + restitution) * vel_along_normal
            j /= 2  # divide by sum of masses (1 + 1)

            # Apply impulse
            impulse_x = j * nx
            impulse_y = j * ny

            self.vel.x += impulse_x
            self.vel.y += impulse_y

            other.vel.x -= impulse_x
            other.vel.y -= impulse_y

            return True

        return False