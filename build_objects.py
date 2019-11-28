import pygame as pg
from view import Camera
import numpy as np
from abc import ABC, abstractmethod



class Object(ABC):
    """
    Interface for all rendered objects
    """
    @abstractmethod
    def __init__(self):
        self.dead = False

    @abstractmethod
    def render(self, screen: pg.Surface, camera: Camera):
        pass

    @abstractmethod
    def update(self):
        pass


class Node(Object):
    """
    Node represents an intersection of streets
    """

    RADIUS = 5
    COLOR = pg.Color("lightskyblue")
    SEL_COLOR = pg.Color((70, 102, 255))
    selected = None

    def __init__(self, pos: np.ndarray):
        self.pos = pos
        self.x, self.y = self.pos
        super(Node, self).__init__()

    def render(self, screen: pg.Surface, camera: Camera):
        """
        Renders as a circle. Uses SEL_COLOR if self is selected.
        """
        rel_pos = np.subtract(self.pos, camera.pos)
        if self is Node.selected:
            pg.draw.circle(screen, Node.SEL_COLOR, rel_pos, Node.RADIUS)
        else:
            pg.draw.circle(screen, Node.COLOR, rel_pos, Node.RADIUS)

    def update(self):
        pass

    def is_touching(self, point: (int, int)) -> bool:
        """
        Returns whether self is touching point
        """
        px, py = point
        return (px - self.x) ** 2 + (py - self.y) ** 2 <= Node.RADIUS ** 2


class Road(Object):
    """
    Road that connects two nodes together.
    """

    COLOR = pg.Color("black")
    WIDTH = 20
    DEL_SLOPE = 5

    def __init__(self, endpoints: (Node, Node)):
        self.dead = False
        self.endpoints = endpoints
        self.left, self.right = self.endpoints
        if self.right.x < self.left.x:
            self.right, self.left = self.left, self.right
        super(Road, self).__init__()

    def render(self, screen: pg.Surface, camera: Camera):
        """
        Renders as line using WIDTH and COLOR
        """
        rel_pos_left = np.subtract(self.left.pos, camera.pos)
        rel_pos_right = np.subtract(self.right.pos, camera.pos)
        pg.draw.circle(screen, Road.COLOR, rel_pos_left, Road.WIDTH // 2)
        pg.draw.line(screen, Road.COLOR, rel_pos_left, rel_pos_right, Road.WIDTH)
        pg.draw.circle(screen, Road.COLOR, rel_pos_right, Road.WIDTH // 2)


    def update(self):
        """
        Checks if nodes are still active
        """
        if self.left.dead or self.right.dead:
            self.dead = True

    def is_touching(self, point: (int, int)) -> bool:
        """
        Returns whether self is touching point
        """
        x, y = point
        x0, y0 = self.left.pos
        x1, y1 = self.right.pos

        if x0 < x < x1:
            # x is in appropriate range
            x -= x0
            y -= y0
            m = (y1 - y0) / (x1 - x0)
            if Road.DEL_SLOPE < np.abs(m):
                # if slope is steep enough, is_touching performs poorly without this special case
                return True
            if x * m - Road.WIDTH / 2 < y < x * m + Road.WIDTH / 2:
                # y is in appropriate range
                return True

        return False
