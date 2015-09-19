#starfield without parallax

import pygame, math
from random import randrange
 
class Simulation:
    def __init__(self, num_stars, max_depth):
        pygame.init()
 
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("3D Starfield Simulation (visit codeNtronix.com)")
 
        self.clock = pygame.time.Clock()
        self.num_stars = num_stars
        self.max_depth = max_depth
 
        self.init_stars()
 
    def init_stars(self):
        """ Create the starfield """
        self.stars = []
        for i in range(self.num_stars):
            # A star is represented as a list with this format: [X,Y,Z]
            star = [randrange(-25,25), randrange(-25,25), randrange(1, self.max_depth)]
            self.stars.append(star)
 
    def move_and_draw_stars(self):
        """ Move and draw the stars """
        origin_x = self.screen.get_width() / 2
        origin_y = self.screen.get_height() / 2
 
        for star in self.stars:
            # The Z component is decreased on each frame.
            star[2] -= 0.19
 
            # If the star has past the screen (I mean Z<=0) then we
            # reposition it far away from the screen (Z=max_depth)
            # with random X and Y coordinates.
            if star[2] <= 0:
                star[0] = randrange(-25,25)
                star[1] = randrange(-25,25)
                star[2] = self.max_depth
 
            # Convert the 3D coordinates to 2D using perspective projection.
            k = 128.0 / star[2]
            x = int(star[0] * k + origin_x)
            y = int(star[1] * k + origin_y)
 
            # Draw the star (if it is visible in the screen).
            # We calculate the size such that distant stars are smaller than
            # closer stars. Similarly, we make sure that distant stars are
            # darker than closer stars. This is done using Linear Interpolation.
            if 0 <= x < self.screen.get_width() and 0 <= y < self.screen.get_height():
                size = (1 - float(star[2]) / self.max_depth) * 5
                shade = (1 - float(star[2]) / self.max_depth) * 255
                self.screen.fill((shade,shade,shade),(x,y,size,size))
 
    def run(self):
        """ Main Loop """
        while 1:
            # Lock the framerate at 50 FPS.
            self.clock.tick(50)
 
            # Handle events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
 
            self.screen.fill((0,0,0))
            self.move_and_draw_stars()
            pygame.display.flip()
 
if __name__ == "__main__":
    Simulation(512, 32).run()