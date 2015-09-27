import pygame
from pygame.locals import *
import math
from random import randrange, randint
from operator import itemgetter


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
        return Point3D(x, y, self.z)


class Vector2:
    def __init__(self, *args):
        self.vector2 = tuple(args)
        self.size = self.vector2[0] if self.vector2[0] > self.vector2[1] else self.vector2[1]
    
    def rotate(self, **kwargs):
        if 'right' in kwargs.keys():
            if kwargs['right']:
                if self.vector2 == (0, self.size):
                    self.vector2 = (self.size, 0)
                elif self.vector2 == (self.size, 0):
                    self.vector2 = (0, -self.size)
                elif self.vector2 == (0, -self.size):
                    self.vector2 = (-self.size, 0)
                elif self.vector2 == (-self.size, 0):
                    self.vector2 = (0, self.size)
        if 'left' in kwargs.keys():
            if kwargs['left']:
                if self.vector2 == (0, self.size):
                    self.vector2 = (-self.size, 0)
                elif self.vector2 == (-self.size, 0):
                    self.vector2 = (0, -self.size)
                elif self.vector2 == (0, -self.size):
                    self.vector2 = (self.size, 0)
                elif self.vector2 == (self.size, 0):
                    self.vector2 = (0, self.size)
    
    def get(self):
        return self.vector2
    
    def addget(self, to_add):
        return self.vector2[0] + to_add[0], self.vector2[1] + to_add[1]
    
    def gresize(self, scale):
        return self.vector2[0] * scale, self.vector2[1] * scale
    
    def from_pos(self, pos):
        return self.vector2[0] + pos[0], self.vector2[1] + pos[1]


class Square:
    def __init__(self, color=(255, 255, 255), size=256, xpos=0, ypos=0, zpos=0, default=0):
        self.color = color
        self.square_size = size
        self.size = 2
        self.points = [
            Point3D(default, default, default),
            Point3D(default+1, default, default),
            Point3D(default+1, default+1, default),
            Point3D(default, default+1, default)
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
    
    def set_default(self, default):
        self.points = [
            Point3D(default, default, default),
            Point3D(default+1, default, default),
            Point3D(default+1, default+1, default),
            Point3D(default, default+1, default)
        ]


class Pyramide:
    def __init__(self, color=(255, 255, 255), pyra_size=256, xpos=0, ypos=0, zpos=0, default=0):
        self.vertices = [
            Point3D(default, default+1, default),
            Point3D(default-1, default-1, default+1),
            Point3D(default-1, default-1, default-1),
            Point3D(default+1, default-1, default+1),
            Point3D(default+1, default-1, default-1)
        ]
        
        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        self.size = 2
        self.color = color
        self.pyra_size = pyra_size
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
    
    def set_default(self, default):
        self.vertices = [
            Point3D(default, default+1, default),
            Point3D(default-1, default-1, default+1),
            Point3D(default-1, default-1, default-1),
            Point3D(default+1, default-1, default+1),
            Point3D(default+1, default-1, default-1)
        ]


class Crate:
    def __init__(self, color=(255, 255, 255), crate_size=256, xpos=0, ypos=0, zpos=0, default=0):
        self.vertices = [
            Point3D(default-1, default+1, default-1),
            Point3D(default+1, default+1, default-1),
            Point3D(default+1, default-1, default-1),
            Point3D(default-1, default-1, default-1),
            Point3D(default-1, default+1, default+1),
            Point3D(default+1, default+1, default+1),
            Point3D(default+1, default-1, default+1),
            Point3D(default-1, default-1, default+1)
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
    
    def set_default(self, default):
        self.vertices = [
            Point3D(default-1, default+1, default-1),
            Point3D(default+1, default+1, default-1),
            Point3D(default+1, default-1, default-1),
            Point3D(default-1, default-1, default-1),
            Point3D(default-1, default+1, default+1),
            Point3D(default+1, default+1, default+1),
            Point3D(default+1, default-1, default+1),
            Point3D(default-1, default-1, default+1)
        ]


class Sphere:
    def __init__(self, color=(255, 255, 255), sphere_size=256, xpos=0, ypos=0, zpos=0, radius=2, default=0):
        self.center = Point3D(default, default, default)
        self.radius = radius
        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        self.size = 2
        self.color = color
        self.sphere_size = sphere_size
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
    
    def set_default(self, default):
        self.center = Point3D(default, default, default)


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
        self.axeX = self.font.render("X", 1, (255, 255, 255))
        self.axeY = self.font.render("Y", 1, (255, 255, 255))
        self.axeZ = self.font.render("Z", 1, (255, 255, 255))
    
    def add(self, object):
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
    
    def draw(self, screen, var=0):
        self.draw_axis(screen)
        for object in self.objects:
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
    
    def foo(self):
        i = 0
        for obj in self.objects:
            obj.set_default(i)
            i -= 0.5


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)