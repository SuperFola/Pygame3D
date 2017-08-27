from engine import *
from constants import *
import pygame
from pygame.locals import *


def main():
    pygame.font.init()
    s = pygame.display.set_mode((600, 600))
    scene = Scene(s, perpetual_rotation=(0.4, 0, 0), fps=10000)
    hyper = Hypercube(color_=PBLUE, lwidth=4)
    scene.add_prefab(hyper)
    scene.run()


if __name__ == '__main__':
    main()