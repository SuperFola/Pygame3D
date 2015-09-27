#starfield with parallax

import pygame
from random import randrange, choice
 
MAX_STARS  = 250
STAR_SPEED = 2
 
def init_stars(screen):
  """ Create the starfield """
  global stars
  stars = []
  for i in range(MAX_STARS):
    # A star is represented as a list with this format: [X,Y,speed]
    star = [randrange(0,screen.get_width() - 1),
            randrange(0,screen.get_height() - 1),
            choice([1,2,3])]
    stars.append(star)
 
def move_and_draw_stars(screen):
  """ Move and draw the stars in the given screen """
  global stars
  for star in stars:
    star[1] += star[2]
    # If the star hit the bottom border then we reposition
    # it in the top of the screen with a random X coordinate.
    if star[1] >= screen.get_height():
      star[1] = 0
      star[0] = randrange(0,639)
      star[2] = choice([1,2,3])
 
    # Adjust the star color acording to the speed.
    # The slower the star, the darker should be its color.
    if star[2] == 1:
      color = (100,100,100)
    elif star[2] == 2:
      color = (190,190,190)
    elif star[2] == 3:
      color = (255,255,255)
 
    # Draw the star as a rectangle.
    # The star size is proportional to its speed.
    screen.fill(color,(star[0],star[1],star[2],star[2]))
 
def main():
  # Pygame stuff
  pygame.init()
  screen = pygame.display.set_mode((640,480))
  pygame.display.set_caption("Parallax Starfield Simulation")
  clock = pygame.time.Clock()
 
  init_stars(screen)
 
  while True:
    # Lock the framerate at 50 FPS
    clock.tick(50)
 
    # Handle events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return
 
    screen.fill((0,0,0))
    move_and_draw_stars(screen)
    pygame.display.flip()
 
if __name__ == "__main__":
  main()