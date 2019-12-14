import pygame as pg
import numpy as np
from build_objects import Object, Node, Road
from utils import calc_rel_pos,calc_rel_rect


class Vehicle(Object, pg.sprite.Sprite):
    """ A Vehicle moves from a start node to end node using roads
    """

    LENGTH = 20
    WIDTH = 10
    COLOR = pg.Color("red")
    SCALE = 0.5

    def __init__(self, road: Road, image_file: str):
        Object.__init__(self)
        pg.sprite.Sprite.__init__(self)

        self.start, self.goto = road.endpoints
        self.travel_angle = np.arctan(self.goto.pos - self.start.pos) [0]

        self.pos = np.array(self.start.pos)

        self.vel = 0.001

        self.image = pg.image.load(image_file)
        self.image = pg.transform.rotate(self.image, self.travel_angle)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.pos
        self.rect.width *= Vehicle.SCALE
        self.rect.height *= Vehicle.SCALE

        self.image = pg.transform.smoothscale(self.image, (self.rect.width, self.rect.height))
        self.scaled_img = pg.transform.smoothscale(self.image, (self.rel_rect.width, self.rel_rect.height))
        self.scaled_img = pg.transform.rotate(self.scaled_img, self.travel_angle)
        self.rel_rect = self.scaled_img.get_rect()


    def render(self, screen: pg.Surface, **kwargs):
        screen.blit(self.scaled_img, self.rel_rect)

    def update(self, **kwargs):
        self.pos = self.pos + self.vel * np.tan(self.travel_angle)

        camera = kwargs["camera"]
        self.rect.left, self.rect.top = self.pos
        self.rel_rect = calc_rel_rect(self.rect, camera)

        if self.rel_rect != self.rect:
            self.scaled_img = pg.transform.smoothscale(self.image, (self.rel_rect.width, self.rel_rect.height))
