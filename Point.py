import pygame
import random as rd
from typing import Tuple
from Vector2D import Vector2D

class Point:
    def __init__(self, cord: Tuple[int, int], r: int):
        self.pos = Vector2D(*cord)
        self.r: int = r

        # 🎨 Each point stores its own color
        # self.color: Tuple[int, int, int] = (255, 0, 0)
        self.color: Tuple[int, int, int] = (rd.randint(0,255), rd.randint(0,255), rd.randint(0,255))
        print(self.color)

    def to_tuple(self) -> Tuple[int, int]:
        return (self.pos.x, self.pos.y)

    def show(self, screen: pygame.Surface) -> None:
        """
        Draw the point using its current color
        """
        pygame.draw.circle(screen, self.color, self.to_tuple(), self.r)

    def __iter__(self):
        yield self.pos.x
        yield self.pos.y