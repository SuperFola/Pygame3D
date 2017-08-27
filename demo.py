from engine import *
import random


X_LIM, Y_LIM = 20, 20
PAD = 2


class Demo:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 12)
        self.fps = 600
        self.clock = pygame.time.Clock()
        self.plan = Plan3D()
    
    def create_squares(self, nb=10):
        print("Creating squares ...")
        for _ in range(nb):
            self.plan.add(Square(color_=(150, 150, 255), size=64, xpos=random.randrange(-X_LIM, X_LIM, PAD)))
    
    def create_crates(self, nb=10):
        print("Creating crates ...")
        for _ in range(nb):
            self.plan.add(Crate(size=64, color_=(255, 150, 255), ypos=random.randrange(-Y_LIM, Y_LIM, PAD)))
    
    def create_pyramides(self, nb=10):
        print("Creating pyramides ...")
        for _ in range(nb):
            self.plan.add(Pyramid(size=64, color_=(150, 255, 255), xpos=random.randrange(-X_LIM, X_LIM, PAD), ypos=random.randrange(-Y_LIM, Y_LIM, PAD)))
    
    def create_spheres(self, nb=10):
        print("Creating spheres ...")
        for _ in range(nb):
            self.plan.add(Sphere(size=64, color_=(255, 255, 150), xpos=random.randrange(-X_LIM, X_LIM, PAD), ypos=random.randrange(-Y_LIM, Y_LIM, PAD)))
    
    def draw_objects(self):
        self.plan.draw(self.screen, 1)
    
    def rotate_objects(self):
        self.plan.rot_y(1)
        self.plan.rot_x(-1)
        self.plan.rot_z(1)
    
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
    demo.create_squares(5)
    demo.create_pyramides(5)
    demo.create_crates(5)
    demo.create_spheres(5)
    print("Generation took %3f" % (time.time() - start))
    print("Running demo ...")
    demo.run()
    pygame.quit()
    print("Exited cleanly")


if __name__ == '__main__':
    main()