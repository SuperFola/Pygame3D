import pygame
from pygame.locals import *
from engine import load_image, Camera, WorldManager
import math


class View:
    def __init__(self, wm):
        self.wm = wm
    
    def move(self, keys, dt, worldMap):
        # speed modifiers
        moveSpeed = dt * 6.0  # the constant value is in squares / second
        rotSpeed = dt * 2.0  # the constant value is in radians / second
        
        if keys[K_UP]:
            # move forward if no wall in front of you
            moveX = self.wm.camera.x + self.wm.camera.dirx * moveSpeed
            if worldMap[int(moveX)][int(self.wm.camera.y)] == 0 and worldMap[int(moveX + 0.1)][int(self.wm.camera.y)] == 0:
                self.wm.camera.x += self.wm.camera.dirx * moveSpeed
            moveY = self.wm.camera.y + self.wm.camera.diry * moveSpeed
            if worldMap[int(self.wm.camera.x)][int(moveY)] == 0 and worldMap[int(self.wm.camera.x)][int(moveY + 0.1)] == 0:
                self.wm.camera.y += self.wm.camera.diry * moveSpeed
        if keys[K_DOWN]:
            # move backwards if no wall behind you
            moveX = self.wm.camera.x + self.wm.camera.dirx * moveSpeed
            if worldMap[int(moveX)][int(self.wm.camera.y)] == 0:
                self.wm.camera.x -= self.wm.camera.dirx * moveSpeed
            moveY = self.wm.camera.y + self.wm.camera.diry * moveSpeed
            if worldMap[int(self.wm.camera.x)][int(moveY)] == 0:
                self.wm.camera.y -= self.wm.camera.diry * moveSpeed
        if (keys[K_RIGHT] and not keys[K_DOWN]) or (keys[K_LEFT] and keys[K_DOWN]):
            # rotate to the right
            # both camera direction and camera plane must be rotated
            oldDirX = self.wm.camera.dirx
            self.wm.camera.dirx = self.wm.camera.dirx * math.cos(- rotSpeed) - self.wm.camera.diry * math.sin(- rotSpeed)
            self.wm.camera.diry = oldDirX * math.sin(- rotSpeed) + self.wm.camera.diry * math.cos(- rotSpeed)
            oldPlaneX = self.wm.camera.planex
            self.wm.camera.planex = self.wm.camera.planex * math.cos(- rotSpeed) - self.wm.camera.planey * math.sin(- rotSpeed)
            self.wm.camera.planey = oldPlaneX * math.sin(- rotSpeed) + self.wm.camera.planey * math.cos(- rotSpeed)
        if (keys[K_RIGHT] and keys[K_DOWN]) or (keys[K_LEFT] and not keys[K_DOWN]): 
            # rotate to the left
            # both camera direction and camera plane must be rotated
            oldDirX = self.wm.camera.dirx
            self.wm.camera.dirx = self.wm.camera.dirx * math.cos(rotSpeed) - self.wm.camera.diry * math.sin(rotSpeed)
            self.wm.camera.diry = oldDirX * math.sin(rotSpeed) + self.wm.camera.diry * math.cos(rotSpeed)
            oldPlaneX = self.wm.camera.planex
            self.wm.camera.planex = self.wm.camera.planex * math.cos(rotSpeed) - self.wm.camera.planey * math.sin(rotSpeed)
            self.wm.camera.planey = oldPlaneX * math.sin(rotSpeed) + self.wm.camera.planey * math.cos(rotSpeed)


class Demo:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.SysFont("arial", 12)
        self.worldMap =[
            [8,8,8,8,8,8,8,8,8,8,8,4,4,6,4,4,6,4,6,4,4,4,6,4],
            [8,0,0,0,0,0,0,0,0,0,8,4,0,0,0,0,0,0,0,0,0,0,0,4],
            [8,0,3,3,0,0,0,0,0,8,8,4,0,0,0,0,0,0,0,0,0,0,0,6],
            [8,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
            [8,0,3,3,0,0,0,0,0,8,8,4,0,0,0,0,0,0,0,0,0,0,0,4],
            [8,0,0,0,0,0,0,0,0,0,8,4,0,0,0,0,0,6,6,6,0,6,4,6],
            [8,8,8,8,0,8,8,8,8,8,8,4,4,4,4,4,4,6,0,0,0,0,0,6],
            [7,7,7,7,0,7,7,7,7,0,8,0,8,0,8,0,8,4,0,4,0,6,0,6],
            [7,7,0,0,0,0,0,0,7,8,0,8,0,8,0,8,8,6,0,0,0,0,0,6],
            [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,6,0,0,0,0,0,4],
            [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,6,0,6,0,6,0,6],
            [7,7,0,0,0,0,0,0,7,8,0,8,0,8,0,8,8,6,4,6,0,6,6,6],
            [7,7,7,7,0,7,7,7,7,8,8,4,0,6,8,4,8,3,3,3,0,3,3,3],
            [2,2,2,2,0,2,2,2,2,4,6,4,0,0,6,0,6,3,0,0,0,0,0,3],
            [2,2,0,0,0,0,0,2,2,4,0,0,0,0,0,0,4,3,0,0,0,0,0,3],
            [2,0,0,0,0,0,0,0,2,4,0,0,0,0,0,0,4,3,0,0,0,0,0,3],
            [1,0,0,0,0,0,0,0,1,4,4,4,4,4,6,0,6,3,3,0,0,0,3,3],
            [2,0,0,0,0,0,0,0,2,2,2,1,2,2,2,6,6,0,0,5,0,5,0,5],
            [2,2,0,0,0,0,0,2,2,2,0,0,0,2,2,0,5,0,5,0,0,0,5,5],
            [2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,5,0,5,0,5,0,5,0,5],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5],
            [2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,5,0,5,0,5,0,5,0,5],
            [2,2,0,0,0,0,0,2,2,2,0,0,0,2,2,0,5,0,5,0,0,0,5,5],
            [2,2,2,2,1,2,2,2,2,2,2,1,2,2,2,5,5,5,5,5,5,5,5,5]
        ]
        self.sprite_positions = [
          (20.5, 11.5, 2, 0,  0., 0.,  0),  # green light in front of playerstart
          # green lights in every room
          (18.5,  4.5, 2, 0,  0., 0.,  0),
          (10.0,  4.5, 2, 0,  0., 0.,  0),
          (10.0, 12.5, 2, 0,  0., 0.,  0),
          (3.5,   6.5, 2, 0,  0., 0.,  0),
          (3.5,  20.5, 2, 0,  0., 0.,  0),
          (3.5,  14.5, 2, 0,  0., 0.,  0),
          (14.5, 20.5, 2, 0,  0., 0.,  0),
          
          # row of pillars in front of wall: fisheye test
          (18.5, 10.5, 1, 0,  0., 0.,  0),
          (18.5, 11.5, 1, 0,  0., 0.,  0),
          (18.5, 12.5, 1, 0,  0., 0.,  0)
        ]
        sprites = [
              load_image("pics/items/barrel.png", False, colorKey=(0,0,0)),
              load_image("pics/items/pillar.png", False, colorKey=(0,0,0)),
              load_image("pics/items/greenlight.png", False, colorKey=(0,0,0)),
              load_image("pics/items/pinky_l.png", False, colorKey=(0,0,0)),
              load_image("pics/items/pinky_r.png", False, colorKey=(0,0,0)),
        ]
        images = [
              load_image("pics/walls/eagle.png", False),
              load_image("pics/walls/redbrick.png", False),
              load_image("pics/walls/purplestone.png", False),
              load_image("pics/walls/greystone.png", False),
              load_image("pics/walls/bluestone.png", False),
              load_image("pics/walls/mossy.png", False),
              load_image("pics/walls/wood.png", False),
              load_image("pics/walls/colorstone.png", False),
    
              load_image("pics/walls/eagle.png", True),
              load_image("pics/walls/redbrick.png", True),
              load_image("pics/walls/purplestone.png", True),
              load_image("pics/walls/greystone.png", True),
              load_image("pics/walls/bluestone.png", True),
              load_image("pics/walls/mossy.png", True),
              load_image("pics/walls/wood.png", True),
              load_image("pics/walls/colorstone.png", True),
        ]
        self.wm = WorldManager(self.worldMap, x=22, y=11.5, dirx=-1, diry=0, planex=0, planey=0.66, sprites=sprites, images=images)
        self.view = View(self.wm)
    
    def run(self):
        while 1:
            self.clock.tick(self.fps)
            
            frameTime = float(self.clock.get_time()) / 1000.0 # frameTime is the time this frame has taken, in seconds
            
            self.screen.fill(0)
            
            self.screen.blit(self.font.render(str(self.clock.get_fps()), 1, (180, 180, 255)), (0, 0))
            self.wm.draw(self.screen, self.sprite_positions)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
            
            keys = pygame.key.get_pressed()
            self.view.move(keys, frameTime, self.worldMap)
            
            pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    demo = Demo(screen)
    demo.run()