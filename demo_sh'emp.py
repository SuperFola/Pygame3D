from engine import *
import pygame
from pygame.locals import *


class Demo(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.gun = Line(color=RED)

    def process_event(self, event):
        if event.type == QUIT:
            self.running = False
        if event.type == KEYDOWN and event.key == K_SPACE:
            self.rotate = not self.rotate
        if event.type == MOUSEBUTTONUP and event.button == 1:
            self.gun.point_to2D(*event.pos)


if __name__ == '__main__':
    import time
    print("Starting ...")
    start = time.time()
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((640, 640))
    demo = Demo(screen)
    print("Generation took %3f" % (time.time() - start))
    print("Running demo ...")
    demo.run()
    pygame.quit()
    print("Exited cleanly")