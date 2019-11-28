import pygame as pg
import numpy as np

class Camera():
    """
    Camera object used to render and scale correct objects
    """

    MIN_SCALE = 0.4
    MAX_SCALE = 1.8 # frames drop if scale > MAX_SCALE

    def __init__(self, pos: (int, int), scale: float, size: (int, int)):
        self.size = size
        self.pos = pos
        self.scale = scale

    def move(self, dpos: (int, int)):
        self.pos = np.add(self.pos, np.multiply(dpos, self.scale))

    def change_scale(self, delta):
        if Camera.MIN_SCALE < self.scale + delta < Camera.MAX_SCALE:
            self.scale += delta
            self.pos = np.add(self.pos, np.multiply(self.size, delta))


class Background(pg.sprite.Sprite):
    """
    Background for App screen
    """
    def __init__(self, image_file: str, location: (int, int)):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def render(self, screen: pg.Surface, camera: Camera):
        rel_rect = pg.Rect(self.rect)
        rel_rect.left, rel_rect.top = np.subtract((self.rect.left, self.rect.top), camera.pos)
        rel_rect.width = int(self.rect.width * camera.scale)
        rel_rect.height = int(self.rect.height * camera.scale)
        scaled_img = pg.transform.smoothscale(self.image, (rel_rect.width, rel_rect.height))
        screen.blit(scaled_img, rel_rect)
