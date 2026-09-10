import pygame
import random as rd
from typing import List
from Quadtree import Quadtree, Rectangle
from Point import Point
from PointWithPhysics import PointWithPhysics

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

POINT_MODE = 1
RECT_MODE = 2

NO_OF_PARTICLE = 1000

def main():
    pygame.init()

    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Quadtree Moving Points")

    clock = pygame.time.Clock()

    w, h = screen.get_width(), screen.get_height()

    capacity = 10
    radius = 5
    max_vel = 2

    # ------------------- CREATE POINTS -------------------
    points: List[PointWithPhysics] = []

    for _ in range(NO_OF_PARTICLE):
        p = PointWithPhysics(
            (rd.randint(0, w), rd.randint(0, h)),
            radius,
        )

        # Random velocity (-2 to 2)
        vx = rd.uniform(-max_vel, max_vel)
        vy = rd.uniform(-max_vel, max_vel)

        p.setVelocity(vx, vy)
        points.append(p)

    # ------------------- GAME LOOP -------------------
    running = True
    while running:
        clock.tick(60)  # 60 FPS
        screen.fill((0, 0, 0))

        # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # -------- UPDATE + BUILD QUADTREE --------
        qt = Quadtree((0, 0, w, h), capacity)
        energy = 0
        for p in points:
            p.update()
            p.bounce(qt.boundary)
            # p.color = WHITE

            # for point in points:
            #     p.collide(point)

            r = p.r
            trees = qt.getQuadTrees(Rectangle((p.pos.x - r / 2,p.pos.y - r / 2,2*r,2*r)))
            for tree in trees:
                for point in tree.points:
                    p.collide(point)
                        
            energy += p.vel.magSq()
            qt.insert(p)

        print(energy)
        # -------- DRAW --------
        qt.show(screen)

        for p in points:
            p.show(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()