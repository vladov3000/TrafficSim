import pygame as pg
import numpy as np
import os
import sys
from build_objects import Node, Road
from run_objects import Vehicle
from view import Background, Camera
from utils import calc_abs_pos


class App(object):
    """ A class to manage constants and overall program flow.
    """
    BACK_COLOR = pg.Color("white")
    CAPTION = "Traffic Simulator"
    SCREEN_SIZE = np.array((800, 600))
    RENDER_ORDER = ["Road", "Node", "Vehicle"]
    CAMERA_MOVE_SPEED = 20
    CAMERA_SCALE_SPEED = 0.1
    FPS = 60

    def __init__(self):
        """ Get a reference to the display surface; set up required attributes;
        """
        pg.display.set_caption(App.CAPTION)
        pg.display.set_mode(App.SCREEN_SIZE)

        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()

        self.done = False
        self.print_dict = {}

        self.background = Background('./backgrounds/small_city.jpg', np.array((0, 0)))
        self.camera = Camera(np.array((0, 0)), Camera.MIN_SCALE, App.SCREEN_SIZE)
        # key: obj.__name__(); value: list of all instances
        self.app_objects = {"Node": [], "Road": [], "Vehicle": []}
        self.state = "build"

    def build_event_loop(self):
        """ Handle inputs during build mode
        """

        # process keyboard inputs
        keys = pg.key.get_pressed()

        if keys[pg.K_DOWN]:
            self.camera.move(np.array((0, App.CAMERA_MOVE_SPEED)))
        if keys[pg.K_UP]:
            self.camera.move(np.array((0, -App.CAMERA_MOVE_SPEED)))
        if keys[pg.K_LEFT]:
            self.camera.move(np.array((-App.CAMERA_MOVE_SPEED, 0)))
        if keys[pg.K_RIGHT]:
            self.camera.move(np.array((App.CAMERA_MOVE_SPEED, 0)))

        # process pygame events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True

                elif event.key == pg.K_SPACE:
                    self.app_objects["Vehicle"].append(Vehicle(self.app_objects["Road"][0], "car_sprites/Audi.png"))
                    self.state = "run"

            elif event.type == pg.MOUSEBUTTONDOWN:
                # Process mouse actions

                # scroll to zoom
                if event.button == 4:
                    self.camera.change_scale(App.CAMERA_SCALE_SPEED)
                if event.button == 5:
                    self.camera.change_scale(-App.CAMERA_SCALE_SPEED)

                click_found = False
                abs_event_pos = calc_abs_pos(np.array(event.pos), self.camera)
                for n in self.app_objects["Node"]:
                    if n.is_touching(abs_event_pos):
                        # user has clicked node n
                        click_found = True

                        if event.button == 3:
                            # delete node if user clicks on node
                            n.dead = True

                        elif Node.selected is n:
                            # deselect if user clicks selected node
                            Node.selected = None

                        elif Node.selected:
                            # create road between selected and next node
                            self.app_objects["Road"].append(Road((Node.selected, n)))
                            # and deselect
                            Node.selected = None

                        elif event.button == 1:
                            # left click to select node
                            Node.selected = n
                        break

                for r in self.app_objects["Road"]:
                    if r.is_touching(abs_event_pos):
                        # user has clicked road r
                        click_found = True

                        if event.button == 3:
                            # delete road if user clicks on node
                            r.dead = True
                        break

                if not click_found and event.button == 1:
                    new = Node(abs_event_pos)
                    self.app_objects["Node"].append(new)
                    if Node.selected:
                        self.app_objects["Road"].append(Road((Node.selected, new)))
                    Node.selected = None

    def run_event_loop(self):
        """ Handle inputs during run mode
        """

        # process keyboard inputs held
        keys = pg.key.get_pressed()

        if keys[pg.K_DOWN]:
            self.camera.move(np.array((0, App.CAMERA_MOVE_SPEED)))
        if keys[pg.K_UP]:
            self.camera.move(np.array((0, -App.CAMERA_MOVE_SPEED)))
        if keys[pg.K_LEFT]:
            self.camera.move(np.array((-App.CAMERA_MOVE_SPEED, 0)))
        if keys[pg.K_RIGHT]:
            self.camera.move(np.array((App.CAMERA_MOVE_SPEED, 0)))

        # handle pygame events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True

                elif event.key == pg.K_SPACE:
                    self.state = "build"

            elif event.type == pg.MOUSEBUTTONDOWN:
                # Process mouse actions

                # scroll to zoom
                if event.button == 4:
                    self.camera.change_scale(App.CAMERA_SCALE_SPEED)
                if event.button == 5:
                    self.camera.change_scale(-App.CAMERA_SCALE_SPEED)

    def render(self):
        """ Render all objects
        """
        # render background
        self.screen.fill(App.BACK_COLOR)
        self.background.render(self.screen)

        # order to render objects in
        for objs in App.RENDER_ORDER:
            for obj in self.app_objects[objs]:
                obj.render(self.screen)
        pg.display.update()

    def update(self):
        """ Update all objects
        """
        self.background.update(self.camera)

        # Delete dead objects
        for obj in sum(self.app_objects.values(), []):
            obj.update(**{"camera": self.camera})
            if obj.dead:
                self.app_objects[type(obj).__name__].remove(obj)

    def main_loop(self):
        """ Runs event loops, updates, and renders while App not done
        """
        while not self.done:
            if str(self) != "":
                print(self)
            if self.state == "build":
                self.build_event_loop()
            elif self.state == "run":
                self.run_event_loop()
            self.update()
            self.render()
            self.clock.tick(App.FPS)

    def __str__(self):
        """ Formats the values in self.print_values

        :return: string
        """
        s = ""
        for name, field in self.print_dict.items():
            val = getattr(field[0], field[1])
            if callable(val):
                val = val()
            s += "%s: %s " % (name, str(val))
        return s


def main():
    """
    Prepare environment, create a display, and start the program.
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    app = App()
    # app.print_dict["fps"] = (app.clock, "get_fps")
    # app.print_dict["scale"] = (app.camera, "scale")
    app.main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
