from __future__ import annotations
from typing import Tuple, List, Optional
from Point import Point
import random as rd
import pygame

# ------------------- CONSTANTS -------------------

WHITE: Tuple[int, int, int] = (255, 255, 255)
RED: Tuple[int, int, int] = (255, 0, 0)
BLUE: Tuple[int,int,int] = (0,0,255)


# ------------------- RECTANGLE -------------------

class Rectangle:
    """
    Represents an axis-aligned rectangle using (x, y, width, height)
    """

    def __init__(self, boundary: Tuple[int, int, int, int]) -> None:
        self.x: int
        self.y: int
        self.w: int
        self.h: int

        self.x, self.y, self.w, self.h = boundary

    def intersects(self, other: Rectangle) -> bool:
        """
        Check if this rectangle intersects with another rectangle
        """
        x1, y1, w1, h1 = self
        x2, y2, w2, h2 = other

        return not (
            x1 + w1 < x2 or  # completely left
            x2 + w2 < x1 or  # completely right
            y1 + h1 < y2 or  # completely above
            y2 + h2 < y1     # completely below
        )

    def isPointInside(self, point: Point) -> bool:
        """
        Check if a point lies inside this rectangle
        """
        px, py = point
        x, y, w, h = self

        return x <= px <= x + w and y <= py <= y + h

    def to_tuple(self) -> Tuple[int, int, int, int]:
        """
        Convert to tuple format usable by pygame
        """
        return (self.x, self.y, self.w, self.h)

    def __iter__(self):
        """
        Allows unpacking like: x, y, w, h = rectangle
        """
        yield self.x
        yield self.y
        yield self.w
        yield self.h


# ------------------- QUADTREE -------------------

class Quadtree:
    """
    Quadtree for efficient spatial partitioning of 2D points
    """

    def __init__(
        self,
        boundary: Tuple[int, int, int, int],
        n: int
    ) -> None:
        # Region represented by this node
        self.boundary: Rectangle = Rectangle(boundary)

        # Maximum number of points before subdivision
        self.capacity: int = n

        # Points stored at this node (only if not subdivided)
        self.points: List[Point] = []

        # Child quadrants
        self.firstQuadrant: Optional["Quadtree"] = None
        self.secondQuadrant: Optional["Quadtree"] = None
        self.thirdQuadrant: Optional["Quadtree"] = None
        self.forthQuadrant: Optional["Quadtree"] = None

        # Indicates whether this node has been subdivided
        self.divided: bool = False

    def makeQuadrants(self) -> bool:
        """
        Subdivide this node into 4 quadrants
        Returns False if subdivision is not possible
        """
        x, y, w, h = self.boundary

        # Half dimensions (integer division for pygame compatibility)
        w_new: int = w // 2
        h_new: int = h // 2

        # Stop subdivision if too small
        if w_new < 2 or h_new < 2:
            return False

        midx: int = x + w_new
        midy: int = y + h_new

        # Create child nodes
        self.firstQuadrant  = Quadtree((midx, y, w_new, h_new), self.capacity)
        self.secondQuadrant = Quadtree((x, y, w_new, h_new), self.capacity)
        self.thirdQuadrant  = Quadtree((x, midy, w_new, h_new), self.capacity)
        self.forthQuadrant  = Quadtree((midx, midy, w_new, h_new), self.capacity)

        # Re-distribute existing points
        for point in self.points:
            self.insertInQuadrants(point)

        self.points = []
        self.divided = True
        return True

    def inBoundary(self, point: Point) -> bool:
        """
        Check if point lies inside this node's region
        """
        px, py = point
        x, y, w, h = self.boundary

        return x <= px <= x + w and y <= py <= y + h

    def insertInQuadrants(self, point: Point) -> bool:
        """
        Insert point into appropriate child quadrant
        """
        return (
            self.firstQuadrant.insert(point) or
            self.secondQuadrant.insert(point) or
            self.thirdQuadrant.insert(point) or
            self.forthQuadrant.insert(point)
        )

    def insert(self, point: Point) -> bool:
        """
        Insert a point into the quadtree
        """
        # Reject if outside boundary
        if not self.inBoundary(point):
            return False

        # Store locally if capacity not exceeded
        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
            return True

        # Subdivide if needed
        if not self.divided:
            if not self.makeQuadrants():
                return False

        # Insert into children
        return self.insertInQuadrants(point)

    def show(self, screen: pygame.Surface) -> None:
        """
        Render quadtree boundaries and points
        """
        # Draw boundary
        pygame.draw.rect(
            screen,
            WHITE,
            self.boundary.to_tuple(),
            1,
        )

        # Draw children recursively
        if self.divided:
            self.firstQuadrant.show(screen)
            self.secondQuadrant.show(screen)
            self.thirdQuadrant.show(screen)
            self.forthQuadrant.show(screen)

        # Draw points
        for pt in self.points:
            pt.show(screen)

    def query(self, area: Rectangle) -> List[Point]:
        """
        Return all points inside a given rectangular region
        """
        result: List[Point] = []

        # Skip if no intersection
        if not self.boundary.intersects(area):
            return result

        # If subdivided → search children
        if self.divided:
            result += self.firstQuadrant.query(area)
            result += self.secondQuadrant.query(area)
            result += self.thirdQuadrant.query(area)
            result += self.forthQuadrant.query(area)
        else:
            # Check points in this node
            query_rect = Rectangle(area)

            for p in self.points:
                if query_rect.isPointInside(p):
                    result.append(p)

        return result
    
    def getQuadTrees(self, area: Rectangle) -> List["Quadtree"]:
        trees: List["Quadtree"] = []

        # If no intersection → skip entirely
        if not self.boundary.intersects(area):
            return trees

        # If subdivided → collect from children
        if self.divided:
            trees.extend(self.firstQuadrant.getQuadTrees(area))
            trees.extend(self.secondQuadrant.getQuadTrees(area))
            trees.extend(self.thirdQuadrant.getQuadTrees(area))
            trees.extend(self.forthQuadrant.getQuadTrees(area))
        else:
            # Leaf node → add this tree
            trees.append(self)

        return trees


