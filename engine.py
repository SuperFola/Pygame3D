import pygame
import os
from pygame.locals import *
import math
from random import randrange, randint
from operator import itemgetter
from constants import *
from basis import *


texWidth = 64
texHeight = 64


class WorldManager(object):
    def __init__(self, worldMap, x=22, y=11.5, dirx=-1, diry=0, planex=0, planey=0.66, sprites=None, images=None):
        self.sprites = sprites
        self.images = images
        
        self.camera = Camera(x, y, dirx, diry, planex, planey)
        self.worldMap = worldMap

    def draw(self, surface, sprite_positions):
        w = surface.get_width()
        h = surface.get_height()
        zBuffer = []
        
        for x in range(w):
            # calculate ray position and direction 
            cameraX = float(2 * x / float(w) - 1)  # x-coordinate in camera space
            rayPosX = self.camera.x
            rayPosY = self.camera.y
            rayDirX = self.camera.dirx + self.camera.planex * cameraX
            rayDirY = self.camera.diry + self.camera.planey * cameraX
            # which box of the map we're in  
            mapX = int(rayPosX)
            mapY = int(rayPosY)
       
            # length of ray from current position to next x or y-side
            sideDistX = 0.0
            sideDistY = 0.0
       
            # length of ray from one x or y-side to next x or y-side
            deltaDistX = math.sqrt(1 + (rayDirY * rayDirY) / (rayDirX * rayDirX))
            if rayDirY == 0:
                rayDirY = 0.00001
            deltaDistY = math.sqrt(1 + (rayDirX * rayDirX) / (rayDirY * rayDirY))
            perpWallDist = 0.0
       
            # what direction to step in x or y-direction (either +1 or -1)
            stepX = 0
            stepY = 0

            hit = 0  # was there a wall hit?
            side = 0  # was a NS or a EW wall hit?
            
            # calculate step and initial sideDist
            if rayDirX < 0:
                stepX = - 1
                sideDistX = (rayPosX - mapX) * deltaDistX
            else:
                stepX = 1
                sideDistX = (mapX + 1.0 - rayPosX) * deltaDistX
                
            if rayDirY < 0:
                stepY = - 1
                sideDistY = (rayPosY - mapY) * deltaDistY
            else:
                stepY = 1
                sideDistY = (mapY + 1.0 - rayPosY) * deltaDistY
                
            # perform DDA
            while hit == 0:
                # jump to next map square, OR in x - direction, OR in y - direction
                if sideDistX < sideDistY:
                    sideDistX += deltaDistX
                    mapX += stepX
                    side = 0
                else:
                    sideDistY += deltaDistY
                    mapY += stepY
                    side = 1
                # Check if ray has hit a wall
                if self.worldMap[mapX][mapY] > 0: 
                    hit = 1
            
            # Calculate distance projected on camera direction (oblique distance will give fisheye effect !)
            if not side:
                perpWallDist = abs((mapX - rayPosX + (1 - stepX) / 2) / rayDirX)
            else:
                perpWallDist = abs((mapY - rayPosY + (1 - stepY) / 2) / rayDirY)
      
            # Calculate height of line to draw on surface
            if perpWallDist == 0:
                perpWallDist = 0.000001
            lineHeight = abs(int(h / perpWallDist))
       
            # calculate lowest and highest pixel to fill in current stripe
            drawStart = - lineHeight / 2 + h / 2
            drawEnd = lineHeight / 2 + h / 2
        
            # texturing calculations
            texNum = self.worldMap[mapX][mapY] - 1  # 1 subtracted from it so that texture 0 can be used!
           
            # calculate value of wallX
            wallX = 0  # where exactly the wall was hit
            if side == 1:
                wallX = rayPosX + ((mapY - rayPosY + (1 - stepY) / 2) / rayDirY) * rayDirX
            else:
                wallX = rayPosY + ((mapX - rayPosX + (1 - stepX) / 2) / rayDirX) * rayDirY
            wallX -= math.floor((wallX))
           
            # x coordinate on the texture
            texX = int(wallX * float(texWidth))
            if not side and rayDirX > 0: 
                texX = texWidth - texX - 1
            if side == 1 and rayDirY < 0: 
                texX = texWidth - texX - 1

            if side == 1:
                texNum += 8
            if lineHeight > 10000:
                lineHeight = 10000
                drawStart = -10000 / 2 + h / 2
            surface.blit(pygame.transform.scale(self.images[texNum][texX], (1, lineHeight)), (x, drawStart))
            zBuffer.append(perpWallDist)
        
        for sprite in sprite_positions:
            #translate sprite position to relative to camera
            spriteX = sprite[0] - self.camera.x;
            spriteY = sprite[1] - self.camera.y;
             
            #transform sprite with the inverse camera matrix
            # [ self.camera.planex   self.camera.dirx ] -1                                       [ self.camera.diry      -self.camera.dirx ]
            # [               ]       =  1/(self.camera.planex*self.camera.diry-self.camera.dirx*self.camera.planey) *   [                 ]
            # [ self.camera.planey   self.camera.diry ]                                          [ -self.camera.planey  self.camera.planex ]
          
            invDet = 1.0 / (self.camera.planex * self.camera.diry - self.camera.dirx * self.camera.planey) #required for correct matrix multiplication
          
            transformX = invDet * (self.camera.diry * spriteX - self.camera.dirx * spriteY)
            transformY = invDet * (-self.camera.planey * spriteX + self.camera.planex * spriteY) #this is actually the depth inside the surface, that what Z is in 3D       
                
            spritesurfaceX = int((w / 2) * (1 + transformX / transformY))
          
            #calculate height of the sprite on surface
            spriteHeight = abs(int(h / (transformY))) #using "transformY" instead of the real distance prevents fisheye
            #calculate lowest and highest pixel to fill in current stripe
            drawStartY = -spriteHeight / 2 + h / 2
            drawEndY = spriteHeight / 2 + h / 2
          
            #calculate width of the sprite
            spriteWidth = abs( int (h / (transformY)))
            drawStartX = -spriteWidth / 2 + spritesurfaceX
            drawEndX = spriteWidth / 2 + spritesurfaceX
            
            if spriteHeight < 1000:
                for stripe in range(int(drawStartX), int(drawEndX)):
                    texX = int(256 * (stripe - (-spriteWidth / 2 + spritesurfaceX)) * texWidth / spriteWidth) / 256
                    #the conditions in the if are:
                    ##1) it's in front of camera plane so you don't see things behind you
                    ##2) it's on the surface (left)
                    ##3) it's on the surface (right)
                    ##4) ZBuffer, with perpendicular distance
                    if(transformY > 0 and stripe > 0 and stripe < w and transformY < zBuffer[stripe]):
                        surface.blit(pygame.transform.scale(self.sprites[sprite[2]+sprite[3]][int(texX)], (1, spriteHeight)), (stripe, drawStartY))


def load_image(path, darken, colorKey=None):
    image = pygame.image.load(path).convert()
    ret = []
    if colorKey is not None:
        image.set_colorkey(colorKey)
    if darken:
        image.set_alpha(127)
    for i in range(image.get_width()):
        s = pygame.Surface((1, image.get_height())).convert()
        s.blit(image, (-i, 0))
        if colorKey is not None:
            s.set_colorkey(colorKey)
        ret.append(s)
    return ret


class Mesh:
    def __init__(self, path_to_image, colorKey=None):
        self.path = path_to_image
        self.mesh = []
        self.colorKey = colorKey
    
    def load(self):
        if os.path.exists(self.path):
            self.mesh = [
                load_image(self.path, False, self.colorKey),
                load_image(self.path, True, self.colorKey)
            ]
        else:
            raise UnboundLocalError("Impossible to load an undefined image from 'path_to_image' !")
    
    def apply(self):
        pass
    
    def get_mesh(self, darken=-1, index=-1):
        if index == -1 and darken == -1:
            return self.mesh
        return self.mesh[darken][index]


class Square:
    def __init__(self, color=WHITE, size=256, xpos=0, ypos=0, zpos=0):
        self.color = color
        self.square_size = size
        self.size = 2
        self.points = [
            Point3D(0, 0, 0),
            Point3D(1, 0, 0),
            Point3D(1, 1, 0),
            Point3D(0, 1, 0)
        ]
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0
    
    def draw(self, screen, var=0):
        t = []
        for v in self.points:
            r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
            p = r.project(screen.get_width(), screen.get_height(), self.square_size, 4 + self.zpos)
            if not var:
                screen.fill(self.color, (p.x + self.xpos, p.y + self.ypos, self.size, self.size))
            t.append(p)
        if var == 1:
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos), (t[1].x + self.xpos, t[1].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[1].x + self.xpos, t[1].y + self.ypos), (t[2].x + self.xpos, t[2].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[2].x + self.xpos, t[2].y + self.ypos), (t[3].x + self.xpos, t[3].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[3].x + self.xpos, t[3].y + self.ypos), (t[0].x + self.xpos, t[0].y + self.ypos))
        if var == 2:
            points = [
                (t[0].x + self.xpos, t[0].y + self.ypos),
                (t[1].x + self.xpos, t[1].y + self.ypos),
                (t[2].x + self.xpos, t[2].y + self.ypos),
                (t[3].x + self.xpos, t[3].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, points)
        if var == 3:
            # apply mesh
            raise NotImplementedError
    
    def rotateX(self, dir=1):
        self.angleX += dir
    
    def rotateY(self, dir=1):
        self.angleY += dir
    
    def rotateZ(self, dir=1):
        self.angleZ += dir
    
    def moveX(self, dir=1):
        self.xpos += dir
    
    def moveY(self, dir=1):
        self.ypos += dir
    
    def moveZ(self, dir=1):
        self.zpos += dir
    
    def set_vertices(self, x, y, z):
        self.points = [
            Point3D(x, y, z),
            Point3D(x+1, y, z),
            Point3D(x+1, y+1, z),
            Point3D(x, y+1, z)
        ]
    
    def get_vertices(self):
        return [(i[0] + self.xpos, i[1] + self.ypos, i[2] + self.zpos) for i in self.vertices]
    
    def get_2D_pos(self, screen):
        return [tuple(v.project(screen.get_width(), screen.get_height(), self.crate_size, 4 + self.zpos)) for v in self.vertices]
    
    def get_size(self):
        return self.square_size


class Line:
    def __init__(self, color=WHITE, size=64, xpos=0, ypos=0, zpos=0, xdir=1, ydir=1, zdir=1):
        self.vertices = [
            Point3D(0, 0, 0),
            Point3D(xdir, ydir, zdir)
        ]
        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        self.color = color
        self.line_size = size
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
    
    def draw(self, screen, var=0):
        t = []
        for v in self.vertices:
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
            # Transform the point from 3D to 2D
            p = r.project(screen.get_width(), screen.get_height(), self.line_size, 4 + self.zpos)
            if not var:
                screen.fill(self.color, (p.x + self.xpos, p.y + self.ypos, self.line_size, self.line_size))
            t.append(p)
        if var == 1 or var == 2:
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos), (t[1].x + self.xpos, t[1].y + self.ypos))
    
    def rotateX(self, dir=1):
        self.angleX += dir
    
    def rotateY(self, dir=1):
        self.angleY += dir
    
    def rotateZ(self, dir=1):
        self.angleZ += dir
    
    def moveX(self, dir=1):
        self.xpos += dir
    
    def moveY(self, dir=1):
        self.ypos += dir
    
    def moveZ(self, dir=1):
        self.zpos += dir
    
    def set_vertices(self, x, y, z, xd=1, yd=1, zd=1):
        self.vertices = [
            Point3D(x, y, z),
            Point3D(x+xd, y+yd, z+zd)
        ]

    def point_to2D(self, x, y):
        self.vertices[1] = Point3D(x, y, self.line_size)
    
    def get_vertices(self):
        return [(i[0] + self.xpos, i[1] + self.ypos, i[2] + self.zpos) for i in self.vertices]
    
    def get_2D_pos(self, screen):
        return [tuple(v.project(screen.get_width(), screen.get_height(), self.line_size, 4 + self.zpos)) for v in self.vertices]
    
    def get_size(self):
        return self.line_size


class Pyramide:
    def __init__(self, color=WHITE, size=256, xpos=0, ypos=0, zpos=0):
        self.vertices = [
            Point3D(0, +1, 0),
            Point3D(-1, -1, 1),
            Point3D(-1, -1, -1),
            Point3D(1, -1, 1),
            Point3D(1, -1, -1)
        ]
        
        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        self.size = 2
        self.color = color
        self.pyra_size = size
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
        
    def draw(self, screen, var=0):
        t = []
        for v in self.vertices:
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
            # Transform the point from 3D to 2D
            p = r.project(screen.get_width(), screen.get_height(), self.pyra_size, 4 + self.zpos)
            if not var:
                screen.fill(self.color, (p.x + self.xpos, p.y + self.ypos, self.size, self.size))
            t.append(p)
        if var == 1:
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos), (t[1].x + self.xpos, t[1].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos), (t[2].x + self.xpos, t[2].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos), (t[3].x + self.xpos, t[3].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos), (t[4].x + self.xpos, t[4].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[1].x + self.xpos, t[1].y + self.ypos), (t[2].x + self.xpos, t[2].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[2].x + self.xpos, t[2].y + self.ypos), (t[4].x + self.xpos, t[4].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[3].x + self.xpos, t[3].y + self.ypos), (t[4].x + self.xpos, t[4].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[1].x + self.xpos, t[1].y + self.ypos), (t[3].x + self.xpos, t[3].y + self.ypos))
        if var == 2:
            points = [
                (t[0].x + self.xpos, t[0].y + self.ypos), (t[1].x + self.xpos, t[1].y + self.ypos), (t[2].x + self.xpos, t[2].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, points)
            points = [
                (t[0].x + self.xpos, t[0].y + self.ypos), (t[2].x + self.xpos, t[2].y + self.ypos), (t[4].x + self.xpos, t[4].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, points)
            points = [
                (t[0].x + self.xpos, t[0].y + self.ypos), (t[3].x + self.xpos, t[3].y + self.ypos), (t[4].x + self.xpos, t[4].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, points)
            points = [
                (t[0].x + self.xpos, t[0].y + self.ypos), (t[1].x + self.xpos, t[1].y + self.ypos), (t[2].x + self.xpos, t[2].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, points)
            points = [
                (t[1].x + self.xpos, t[1].y + self.ypos), (t[2].x + self.xpos, t[2].y + self.ypos),
                (t[4].x + self.xpos, t[4].y + self.ypos), (t[3].x + self.xpos, t[3].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, points)
        
    def rotateX(self, dir=1):
        self.angleX += dir
    
    def rotateY(self, dir=1):
        self.angleY += dir
    
    def rotateZ(self, dir=1):
        self.angleZ += dir
    
    def moveX(self, dir=1):
        self.xpos += dir
    
    def moveY(self, dir=1):
        self.ypos += dir
    
    def moveZ(self, dir=1):
        self.zpos += dir
    
    def set_vertices(self, x, y, z):
        self.vertices = [
            Point3D(x, y+1, z),
            Point3D(x-1, y-1, z+1),
            Point3D(x-1, y-1, z-1),
            Point3D(x+1, y-1, z+1),
            Point3D(x+1, y-1, z-1)
        ]
    
    def get_vertices(self):
        return [(i[0] + self.xpos, i[1] + self.ypos, i[2] + self.zpos) for i in self.vertices]
    
    def get_2D_pos(self, screen):
        return [tuple(v.project(screen.get_width(), screen.get_height(), self.crate_size, 4 + self.zpos)) for v in self.vertices]
    
    def get_size(self):
        return self.pyra_size


class Crate:
    def __init__(self, color=WHITE, size=256, xpos=0, ypos=0, zpos=0):
        self.vertices = [
            Point3D(-1, +1, -1),
            Point3D(+1, +1, -1),
            Point3D(+1, -1, -1),
            Point3D(-1, -1, -1),
            Point3D(-1, +1, +1),
            Point3D(+1, +1, +1),
            Point3D(+1, -1, +1),
            Point3D(-1, -1, +1)
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
        self.crate_size = size
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
    
    def draw(self, screen, var=0):
        t = []
        for v in self.vertices:
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
            # Transform the point from 3D to 2D
            p = r.project(screen.get_width(), screen.get_height(), self.crate_size, 4 + self.zpos)
            if not var:
                screen.fill(self.color, (p.x + self.xpos, p.y + self.ypos, self.size, self.size))
            t.append(p)
        if var == 1:
            for f in self.faces:
                pygame.draw.line(screen, self.color, (t[f[0]].x + self.xpos, t[f[0]].y + self.ypos), (t[f[1]].x + self.xpos, t[f[1]].y + self.ypos))
                pygame.draw.line(screen, self.color, (t[f[1]].x + self.xpos, t[f[1]].y + self.ypos), (t[f[2]].x + self.xpos, t[f[2]].y + self.ypos))
                pygame.draw.line(screen, self.color, (t[f[2]].x + self.xpos, t[f[2]].y + self.ypos), (t[f[3]].x + self.xpos, t[f[3]].y + self.ypos))
                pygame.draw.line(screen, self.color, (t[f[3]].x + self.xpos, t[f[3]].y + self.ypos), (t[f[0]].x + self.xpos, t[f[0]].y + self.ypos))
        if var == 2:
            avg_z = []
            i = 0
            for f in self.faces:
                z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
                avg_z.append([i, z])
                i += 1
            for tmp in sorted(avg_z, key=itemgetter(1), reverse=True):
                face_index = tmp[0]
                f = self.faces[face_index]
                points = [
                    (t[f[0]].x + self.xpos, t[f[0]].y + self.ypos), (t[f[1]].x + self.xpos, t[f[1]].y + self.ypos),
                    (t[f[1]].x + self.xpos, t[f[1]].y + self.ypos), (t[f[2]].x + self.xpos, t[f[2]].y + self.ypos),
                    (t[f[2]].x + self.xpos, t[f[2]].y + self.ypos), (t[f[3]].x + self.xpos, t[f[3]].y + self.ypos),
                    (t[f[3]].x + self.xpos, t[f[3]].y + self.ypos), (t[f[0]].x + self.xpos, t[f[0]].y + self.ypos)
                ]
                pygame.draw.polygon(screen, self.color, points)
        if var == 3:
            #apply a mesh
            raise NotImplementedError
    
    def rotateX(self, dir=1):
        self.angleX += dir
    
    def rotateY(self, dir=1):
        self.angleY += dir
    
    def rotateZ(self, dir=1):
        self.angleZ += dir
    
    def moveX(self, dir=1):
        self.xpos += dir
    
    def moveY(self, dir=1):
        self.ypos += dir
    
    def moveZ(self, dir=1):
        self.zpos += dir
    
    def set_vertices(self, x, y, z):
        self.vertices = [
            Point3D(x-1, y+1, z-1),
            Point3D(x+1, y+1, z-1),
            Point3D(x+1, y-1, z-1),
            Point3D(x-1, y-1, z-1),
            Point3D(x-1, y+1, z+1),
            Point3D(x+1, y+1, z+1),
            Point3D(x+1, y-1, z+1),
            Point3D(x-1, y-1, z+1)
        ]
    
    def get_vertices(self):
        return [(i[0] + self.xpos, i[1] + self.ypos, i[2] + self.zpos) for i in self.vertices]
    
    def get_2D_pos(self, screen):
        return [tuple(v.project(screen.get_width(), screen.get_height(), self.crate_size, 4 + self.zpos)) for v in self.vertices]
    
    def get_size(self):
        return self.crate_size


class Hypercube:
    def __init__(self, color=WHITE, size=256, xpos=0, ypos=0, zpos=0, lwidth=2):
        self.vertices = [
            Point3D(-1, +1, -1),
            Point3D(+1, +1, -1),
            Point3D(+1, -1, -1),
            Point3D(-1, -1, -1),
            Point3D(-1, +1, +1),
            Point3D(+1, +1, +1),
            Point3D(+1, -1, +1),
            Point3D(-1, -1, +1),
            
            Point3D(1-1, 1+1, -1),
            Point3D(1+1, 1+1, -1),
            Point3D(1+1, 1-1, -1),
            Point3D(1-1, 1-1, -1),
            Point3D(1-1, 1+1, +1),
            Point3D(1+1, 1+1, +1),
            Point3D(1+1, 1-1, +1),
            Point3D(1-1, 1-1, +1),
        ]
        # Define the vertices that compose each of the 6 faces. These numbers are
        # indices to the vertices list defined above.
        self.faces = [
            (0, 1, 2, 3),
            (1, 5, 6, 2),
            (5, 4, 7, 6),
            (4, 0, 3, 7),
            (0, 4, 5, 1),
            (3, 2, 6, 7),
            
            (8, 9, 10, 11),
            (9, 13, 14, 10),
            (13, 12, 15, 14),
            (12, 8, 11, 15),
            (8, 12, 13, 9),
            (11, 10, 14, 15),
            
            (0, 8, 11, 3),
            (1, 9, 10, 2),
            (4, 12, 15, 7),
            (5, 13, 14, 6)
        ]
        
        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        self.size = 2
        self.color = color
        self.crate_size = size
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
        self.lwidth = lwidth
    
    def draw(self, screen, var=0):
        t = []
        i = 0
        for v in self.vertices:
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
            # Transform the point from 3D to 2D
            p = r.project(screen.get_width(), screen.get_height(), self.crate_size, 4 + self.zpos)
            if not var:
                screen.fill(self.color, (p.x + self.xpos, p.y + self.ypos, self.size, self.size))
            t.append(p)
            i += 1
        if var == 1:
            for f in self.faces:
                pygame.draw.line(screen, self.color, (t[f[0]].x + self.xpos, t[f[0]].y + self.ypos), (t[f[1]].x + self.xpos, t[f[1]].y + self.ypos), self.lwidth)
                pygame.draw.line(screen, self.color, (t[f[1]].x + self.xpos, t[f[1]].y + self.ypos), (t[f[2]].x + self.xpos, t[f[2]].y + self.ypos), self.lwidth)
                pygame.draw.line(screen, self.color, (t[f[2]].x + self.xpos, t[f[2]].y + self.ypos), (t[f[3]].x + self.xpos, t[f[3]].y + self.ypos), self.lwidth)
                pygame.draw.line(screen, self.color, (t[f[3]].x + self.xpos, t[f[3]].y + self.ypos), (t[f[0]].x + self.xpos, t[f[0]].y + self.ypos), self.lwidth)
        if var == 2:
            avg_z = []
            i = 0
            for f in self.faces:
                z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
                avg_z.append([i, z])
                i += 1
            for tmp in sorted(avg_z, key=itemgetter(1), reverse=True):
                face_index = tmp[0]
                f = self.faces[face_index]
                points = [
                    (t[f[0]].x + self.xpos, t[f[0]].y + self.ypos), (t[f[1]].x + self.xpos, t[f[1]].y + self.ypos),
                    (t[f[1]].x + self.xpos, t[f[1]].y + self.ypos), (t[f[2]].x + self.xpos, t[f[2]].y + self.ypos),
                    (t[f[2]].x + self.xpos, t[f[2]].y + self.ypos), (t[f[3]].x + self.xpos, t[f[3]].y + self.ypos),
                    (t[f[3]].x + self.xpos, t[f[3]].y + self.ypos), (t[f[0]].x + self.xpos, t[f[0]].y + self.ypos)
                ]
                pygame.draw.polygon(screen, self.color, points)
        if var == 3:
            #apply a mesh
            raise NotImplementedError
    
    def rotateX(self, dir=1):
        self.angleX += dir
    
    def rotateY(self, dir=1):
        self.angleY += dir
    
    def rotateZ(self, dir=1):
        self.angleZ += dir
    
    def moveX(self, dir=1):
        self.xpos += dir
    
    def moveY(self, dir=1):
        self.ypos += dir
    
    def moveZ(self, dir=1):
        self.zpos += dir
    
    def get_vertices(self):
        return [(i[0] + self.xpos, i[1] + self.ypos, i[2] + self.zpos) for i in self.vertices]
    
    def set_vertices(self, x, y, z):
        raise NotImplementedError
    
    def get_2D_pos(self, screen):
        return [tuple(v.project(screen.get_width(), screen.get_height(), self.crate_size, 4 + self.zpos)) for v in self.vertices]
    
    def get_size(self):
        return self.crate_size


class Sphere:
    def __init__(self, color=WHITE, size=256, xpos=0, ypos=0, zpos=0, radius=2):
        self.center = Point3D(xpos, ypos, zpos)
        self.radius = radius
        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        self.size = 2
        self.color = color
        self.sphere_size = size
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
    
    def draw(self, screen, var=0):
        r = self.center.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
        p = r.project(screen.get_width(), screen.get_height(), self.sphere_size, 4 + self.zpos)
        radius = abs(-self.radius * (self.sphere_size / (4 - self.zpos)))
        if not var:
            screen.fill(self.color, (p.x + self.xpos, p.y + self.ypos, self.size, self.size))
        if var == 1:
            pygame.draw.circle(screen, self.color, (int(p.x) + self.xpos, int(p.y) + self.ypos), int(radius), 1)
        if var == 2:
            pygame.draw.circle(screen, self.color, (int(p.x) + self.xpos, int(p.y) + self.ypos), int(radius), 0)

    def rotateX(self, dir=1):
        self.angleX += dir
    
    def rotateY(self, dir=1):
        self.angleY += dir
    
    def rotateZ(self, dir=1):
        self.angleZ += dir
    
    def moveX(self, dir=1):
        self.xpos += dir
    
    def moveY(self, dir=1):
        self.ypos += dir
    
    def moveZ(self, dir=1):
        self.zpos += dir
    
    def set_vertices(self, x, y, z):
        self.center = Point3D(x, y, z)
    
    def get_vertices(self):
        return [(i[0] + self.xpos, i[1] + self.ypos, i[2] + self.zpos) for i in self.vertices]
    
    def get_2D_pos(self, screen):
        return [tuple(self.center.project(screen.get_width(), screen.get_height(), self.sphere_size, 4 + self.zpos))]
    
    def get_size(self):
        return self.sphere_size


class Plan3D:
    def __init__(self, xpos=0, ypos=0, zpos=0):
        self.objects = []
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
        self.axis = [
            Point3D(0, 0, 0),
            Point3D(1, 0, 0),
            Point3D(0, 1, 0),
            Point3D(0, 0, 1)
        ]
        self.angleX = 0
        self.angleY = 0
        self.angleZ = 0
        self.font = pygame.font.SysFont("arial", 12)
        self.axeX = self.font.render("X", 1, WHITE)
        self.axeY = self.font.render("Y", 1, WHITE)
        self.axeZ = self.font.render("Z", 1, WHITE)
    
    def add(self, *objects):
        for object in objects:
            self.objects.append(object)
    
    def draw_axis(self, screen):
        t = []
        for axe in self.axis:
            r = axe.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
            p = r.project(screen.get_width(), screen.get_height(), 256, 4)
            t.append(p)
        pygame.draw.line(screen, RED, (t[0].x, t[0].y), (t[1].x, t[1].y))
        screen.blit(self.axeX, (t[1].x, t[1].y))
        pygame.draw.line(screen, GREEN, (t[0].x, t[0].y), (t[2].x, t[2].y))
        screen.blit(self.axeY, (t[2].x, t[2].y))
        pygame.draw.line(screen, BLUE, (t[0].x, t[0].y), (t[3].x, t[3].y))
        screen.blit(self.axeZ, (t[3].x, t[3].y))
    
    def get_objects(self):
        return self.objects
    
    def draw(self, screen, var=0, only_visible=False):
        for object in self.objects:
            if only_visible:
                p = sorted(object.get_2D_pos(screen))[0]
                if 0 <= p[0] <= screen.get_width() and 0 <= p[1] <= screen.get_height():
                    object.draw(screen, var)
            else:
                object.draw(screen, var)
    
    def rotateX(self, dir=1):
        self.angleX += dir
        for object in self.objects:
            object.rotateX(dir)
    
    def rotateY(self, dir=1):
        self.angleY += dir
        for object in self.objects:
            object.rotateY(dir)
    
    def rotateZ(self, dir=1):
        self.angleZ += dir
        for object in self.objects:
            object.rotateZ(dir)
    
    def moveX(self, dir=1):
        for object in self.objects:
            object.moveX(dir)
    
    def moveY(self, dir=1):
        for object in self.objects:
            object.moveY(dir)
    
    def moveZ(self, dir=1):
        for object in self.objects:
            object.moveZ(dir)


class Scene:
    def __init__(self, screen, perpetual_rotation=(0, 1, 0), rotate=True, fps=100, method=1, axis=True):
        pygame.font.init()
        self.screen = screen
        self.p_rotat = perpetual_rotation
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.plan = Plan3D()
        self.method = method
        self.axis = axis
        self.dt = -1
        self.rotate = rotate
        self.running = True
        self.static_objects = []
    
    def add_prefab(self, *objects):
        self.plan.add(*objects)
    
    def draw(self):
        self.plan.draw(self.screen, self.method, only_visible=True)
        if self.axis:
            self.plan.draw_axis(self.screen)
        for static_object in self.static_objects:
            static_object.draw(self.screen, self.method)

    def add_static_object(self, *objects):
        for object in objects:
            self.static_objects.append(object)

    def rotateX(self, dir):
        self.plan.rotateX(dir)

    def rotateY(self, dir):
        self.plan.rotateY(dir)

    def rotateZ(self, dir):
        self.plan.rotateZ(dir)
    
    def rotate_objects(self):
        self.plan.rotateY(self.p_rotat[0])
        self.plan.rotateX(self.p_rotat[1])
        self.plan.rotateZ(self.p_rotat[2])
    
    def get_ticks(self):
        return self.dt

    def process_event(self, event):
        if event.type == QUIT:
            self.running = False
        if event.type == KEYDOWN and event.key == K_SPACE:
            self.rotate = not self.rotate
    
    def run(self):
        while self.running:
            self.dt = self.clock.tick(self.fps)
            
            event = pygame.event.poll()
            self.process_event(event)
            
            self.screen.fill((0, 0, 0))
            self.draw()
            if self.rotate:
                self.rotate_objects()
            
            pygame.display.flip()