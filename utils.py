import pygame as pg
import numpy as np
import view


def calc_rel_pos(pos: np.ndarray, camera: view.Camera) -> np.ndarray:
    """ Converts absolute to relative position using camera

    :param pos: absolute position
    :param camera: Camera that describes the screen
    :return: relative position as an integer np array
    """
    return ((pos - camera.pos) * camera.scale).astype(int)


def calc_abs_pos(pos: np.ndarray, camera: view.Camera) -> np.ndarray:
    """ Converts relative to absolute position using camera

    :param pos: relative position
    :param camera: Camera that describes the screen
    :return: absolute position as an integer np array
    """
    return (pos / camera.scale + camera.pos).astype(int)


def calc_rel_rect(rect: pg.Rect, camera: view.Camera):
    """ Converts and scales absolute rectangle to relative rectangle

    :param rect: absolute rectangle
    :param camera: Camera that describes the screen
    :return: relative rectangle
    """

    rel_rect = pg.Rect(rect)
    rel_rect.left, rel_rect.top = calc_rel_pos(np.array((rect.left, rect.top)), camera)
    rel_rect.width = int(rect.width * camera.scale)
    rel_rect.height = int(rect.height * camera.scale)

    return rel_rect;
