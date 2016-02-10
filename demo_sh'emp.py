from engine import *
import pygame
from pygame.locals import *


class Demo(Scene):
    def __init__(self, screen):
        super().__init__(screen, perpetual_rotation=(0, 0, 0))
        self.gun = Line(color=RED)
        self.add_static_object(self.gun)

    def process_event(self, event):
        if event.type == QUIT:
            self.running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                self.rotate = not self.rotate
            if event.key == K_RIGHT:
                self.rotateY(5)
            if event.key == K_LEFT:
                self.rotateY(-5)
            if event.key == K_UP:
                self.rotateX(5)
            if event.key == K_DOWN:
                self.rotateX(-5)
        if event.type == MOUSEBUTTONUP and event.button == 1:
            self.gun.point_to2D(event.pos[0] - self.screen.get_width() // 2,
                                event.pos[1] - self.screen.get_height() // 2)


if __name__ == '__main__':
    import time
    print("Starting ...")
    start = time.time()
    pygame.init()
    pygame.font.init()
    pygame.key.set_repeat(200, 100)
    screen = pygame.display.set_mode((640, 640))
    demo = Demo(screen)
    print("Generation took %3f" % (time.time() - start))
    print("Running demo ...")
    demo.run()
    pygame.quit()
    print("Exited cleanly")