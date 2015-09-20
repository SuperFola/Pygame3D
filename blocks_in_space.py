import pygame
from pygame.locals import *
import math
from random import randrange, randint


class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
 
    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = math.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)
 
    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = math.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)
 
    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = math.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)
 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)


class Crate:
    def __init__(self, color=(255, 255, 255), crate_size=256, xpos=0, ypos=0):
        self.vertices = [
            Point3D(-1, 1, -1),
            Point3D(1, 1, -1),
            Point3D(1, -1, -1),
            Point3D(-1, -1, -1),
            Point3D(-1, 1, 1),
            Point3D(1, 1, 1),
            Point3D(1, -1, 1),
            Point3D(-1, -1, 1)
        ]
        # Define the vertices that compose each of the 6 faces. These numbers are
        # indices to the vertices list defined above.
        self.faces = [
            (0, 1, 2, 3),
            (1, 5, 6, 2),
            (5, 4, 7, 6),
            (4, 0, 3, 7),
            (0, 4, 5, 1),
            (3, 2, 6, 7)
        ]
        
        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        self.size = 2
        self.color = color
        self.crate_size = crate_size
        self.xpos = xpos
        self.ypos = ypos
    
    def draw(self, screen):
        t = []
        for v in self.vertices:
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
            # Transform the point from 3D to 2D
            p = r.project(screen.get_width(), screen.get_height(), self.crate_size, 4)
            t.append(p)
        for f in self.faces:
            pygame.draw.line(screen, self.color, (t[f[0]].x + self.xpos, t[f[0]].y + self.ypos), (t[f[1]].x + self.xpos, t[f[1]].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[f[1]].x + self.xpos, t[f[1]].y + self.ypos), (t[f[2]].x + self.xpos, t[f[2]].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[f[2]].x + self.xpos, t[f[2]].y + self.ypos), (t[f[3]].x + self.xpos, t[f[3]].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[f[3]].x + self.xpos, t[f[3]].y + self.ypos), (t[f[0]].x + self.xpos, t[f[0]].y + self.ypos))

    def rotateX(self, dir=1):
        self.angleX += dir
    
    def rotateY(self, dir=1):
        self.angleY += dir
    
    def rotateZ(self, dir=1):
        self.angleZ += dir
    
    def moveX(self, dir=1):
        pass
    
    def moveY(self, dir=1):
        pass
    
    def moveZ(self, dir=1):
        pass

 
class Simulation:
    def __init__(self, num_blocks, screen, auto=False): 
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.num_blocks = num_blocks
        self.done = False
        self.blocks = []
        self.auto = auto
 
    def init_blocks(self):
        """ Create the blockfield """
        for i in range(self.num_blocks):
            block = Crate(color=(randrange(50, 255), randrange(50, 255), randrange(50, 255)),
                          crate_size=randrange(50, (self.screen.get_size()[0] // self.screen.get_size()[1] + 30) * 15),
                          xpos=randint(-100, 100),
                          ypos=randint(-100, 100))
            self.blocks.append(block)
    
    def draw_blocks(self, axis, dir=1):
        """ Draw the crates on the screen and rotate them """
        ax = axis

        for block in self.blocks:
            block.draw(self.screen)

        for i in range(len(self.blocks)):
            if isinstance(axis, int) and isinstance(dir, int):
                if ax == 0:
                    # X axis
                    self.blocks[i].rotateX(dir)
                if ax == 1:
                    # Y axis
                    self.blocks[i].rotateY(dir)
                if ax == 2:
                    # Z axis
                    self.blocks[i].rotateZ(dir)
            else:
                self.blocks[i].rotateX(dir[0])
                self.blocks[i].rotateY(dir[1])
                self.blocks[i].rotateZ(dir[2])
 
    def run(self):
        """ Main Loop """
        axis = 0
        dir = 0
        
        while not self.done:
            # Lock the framerate at 50 FPS.
            self.clock.tick(50)
 
            # Handle events.
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.done = True
                if not self.auto:
                    if event.type == KEYDOWN:
                        if event.key == K_UP:
                            axis = 0
                            dir = 1
                        if event.key == K_DOWN:
                            axis = 0
                            dir = -1
                        if event.key == K_RIGHT:
                            axis = 1
                            dir = -1
                        if event.key == K_LEFT:
                            axis = 1
                            dir = 1
                    if event.type == KEYUP:
                        if event.key in (K_UP, K_DOWN, K_RIGHT, K_LEFT):
                            dir = 0

            if self.auto:
                axis = (0, 1, 2)
                dir = (-1, 1, -1)
            
            self.screen.fill((0, 0, 0))
            self.draw_blocks(axis, dir)
            pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0))
    pygame.display.set_caption("Test")
    s = Simulation(16, screen, True)
    s.init_blocks()
    s.run()
    pygame.quit()

 
if __name__ == "__main__":
    main()