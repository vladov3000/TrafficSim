import pygame as pg
import numpy as np
import utils


class Camera:
    """ Camera object used to render and scale correct objects
    """

    MIN_SCALE = 0.2
    MAX_SCALE = 1.0  # frames drop if self.scale > MAX_SCALE

    def __init__(self, pos: np.ndarray, scale: float, size: np.ndarray):
        self.size = size
        self.pos = pos
        self.scale = scale

    def move(self, delta: np.ndarray):
        """ Move by delta
        """
        self.pos += delta

    def change_scale(self, delta: float):
        """ Change scale by delta
        """
        if Camera.MIN_SCALE < self.scale + delta < Camera.MAX_SCALE:
            #self.pos += (delta / 2 * self.size * self.scale).astype(int)
            self.scale += delta


class Background(pg.sprite.Sprite):
    """ Background for App screen
    """

    def __init__(self, image_file: str, pos: np.ndarray):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pg.image.load(image_file)
        self.scaled_img = self.image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos
        self.rel_rect = self.rect

    def render(self, screen: pg.Surface):
        """ Renders background image onto screen

        :param screen: screen to render onto
        """
        screen.blit(self.scaled_img, self.rel_rect)

    def update(self, camera: Camera):
        """ Updates self.rel_rect, self.scaled_img

        :param camera: camera used to determine relative positions/sizes
        """
        self.rel_rect = pg.Rect(self.rect)
        self.rel_rect.left, self.rel_rect.top = utils.calc_rel_pos(np.array((self.rect.left, self.rect.top)), camera)
        self.rel_rect.width = int(self.rect.width * camera.scale)
        self.rel_rect.height = int(self.rect.height * camera.scale)

        if self.rel_rect != self.rect:
            self.scaled_img = pg.transform.smoothscale(self.image, (self.rel_rect.width, self.rel_rect.height))
