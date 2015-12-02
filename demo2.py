from engine import Plan3D, Sphere, Crate, Square, Pyramide, Mesh
import random
import pygame
from pygame.locals import *


class Demo:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 12)
        self.fps = 600
        self.clock = pygame.time.Clock()
        self.plan = Plan3D()
    
    def create_squares(self):
        print("Creating squares ...")
        for _ in range(10):
            self.plan.add(Square(color=(150, 150, 255), size=64, xpos=random.randrange(0, 300, 32)))
    
    def create_crates(self):
        print("Creating crates ...")
        for _ in range(100):
            self.plan.add(Crate(size=64, color=(255, 150, 255), ypos=random.randrange(0, 300, 32), mesh=Mesh("pics/walls/redbrick.png")))
    
    def create_pyramides(self):
        print("Creating pyramides ...")
        for _ in range(10):
            self.plan.add(Pyramide(size=64, color=(150, 255, 255), xpos=random.randrange(0, 300, 32), ypos=random.randrange(0, 300, 32)))
    
    def create_spheres(self):
        print("Creating spheres ...")
        for _ in range(10):
            self.plan.add(Sphere(size=64, color=(255, 255, 150), xpos=random.randrange(0, 300, 32), ypos=random.randrange(0, 300, 32)))
    
    def draw_objects(self):
        self.plan.draw(self.screen, 1)
    
    def rotate_objects(self):
        self.plan.rotateY(1)
        self.plan.rotateX(-1)
    
    def run(self):
        while 1:
            self.clock.tick(self.fps)
            
            event = pygame.event.poll()
            if event.type == QUIT:
                break
            
            self.screen.fill((0, 0, 0))
            self.draw_objects()
            self.rotate_objects()
            
            self.screen.blit(self.font.render("FPS:" + str(self.clock.get_fps()), 1, (180, 255, 255)), (0, 0))
            
            pygame.display.flip()


def main():
    import time
    print("Starting ...")
    start = time.time()
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((640, 640))
    demo = Demo(screen)
    #demo.create_squares()
    #demo.create_pyramides()
    demo.create_crates()
    #demo.create_spheres()
    print("Generation took %3f" % (time.time() - start))
    print("Running demo ...")
    demo.run()
    pygame.quit()
    print("Exited cleanly")


if __name__ == '__main__':
    main()