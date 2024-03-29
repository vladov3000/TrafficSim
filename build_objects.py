import pygame as pg
import numpy as np
from abc import ABC, abstractmethod
from utils import calc_rel_pos


class Object(ABC):
    """ Interface for all rendered objects
    """

    @abstractmethod
    def __init__(self):
        self.dead = False

    @abstractmethod
    def render(self, screen: pg.Surface, **kwargs):
        pass

    @abstractmethod
    def update(self, **kwargs):
        pass


class Node(Object):
    """ A Node represents an intersection of streets. Intended to be used by other objects as
    reference points.
    """

    RADIUS = 5
    COLOR = pg.Color("lightskyblue")
    SEL_COLOR = pg.Color((70, 102, 255))
    selected = None

    def __init__(self, pos: np.ndarray):
        self.rel_radius = Node.RADIUS
        self.pos = pos
        self.x, self.y = self.pos
        self.rel_pos = self.pos
        super(Node, self).__init__()

    def render(self, screen: pg.Surface, **kwargs):
        """ Renders as a circle using Node.COLOR. Uses Node.SEL_COLOR if self is selected.

        :param screen: Screen to render on
        :param kwargs: none
        """
        if self is Node.selected:
            pg.draw.circle(screen, Node.SEL_COLOR, self.rel_pos, Node.RADIUS)
        else:
            pg.draw.circle(screen, Node.COLOR, self.rel_pos, Node.RADIUS)

    def update(self, **kwargs):
        """ Computes relative position and relative radius

        :param kwargs: Camera object passed as "camera"
        """
        camera = kwargs["camera"]
        self.rel_pos = calc_rel_pos(self.pos, camera)
        self.rel_radius = Node.RADIUS / camera.scale

    def is_touching(self, point: (int, int)) -> bool:
        """ Determine whether node is touching point

        :param point: (x, y) coordinate
        :return: whether node is touching point
        """
        px, py = point
        return (px - self.x) ** 2 + (py - self.y) ** 2 <= self.rel_radius ** 2


class Road(Object):
    """ Road that connects two nodes together.
    """

    COLOR = pg.Color("black")
    WIDTH = 20
    DEL_SLOPE = 2

    def __init__(self, endpoints: (Node, Node)):
        self.dead = False
        self.endpoints = endpoints
        self.left, self.right = self.endpoints
        if self.right.x < self.left.x:
            self.right, self.left = self.left, self.right
        super(Road, self).__init__()

    def render(self, screen: pg.Surface, **kwargs):
        """ Render road as line with two circles at endpoints

        :param screen: screen to render onto
        :param camera: Camera to
        :return:
        """
        pg.draw.circle(screen, Road.COLOR, self.left.rel_pos, Road.WIDTH // 2)
        pg.draw.line(screen, Road.COLOR, self.left.rel_pos, self.right.rel_pos, Road.WIDTH)
        pg.draw.circle(screen, Road.COLOR, self.right.rel_pos, Road.WIDTH // 2)

    def update(self, **kwargs):
        """ Checks if nodes are still active.
        """
        if self.left.dead or self.right.dead:
            self.dead = True

    def is_touching(self, point: (int, int)) -> bool:
        """ Returns whether road is touching point.
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
