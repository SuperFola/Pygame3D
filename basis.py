import math
from constants import *


class Point3D:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x, self.y, self.z = float(x), float(y), float(z)
    
    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
        raise IndexError
    
    def __next__(self):
        return self.x, self.y, self.z

    def __str__(self):
        return "{}, {}, {}".format(self.x, self.y, self.z)
 
    def rot_x(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = math.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)
 
    def rot_y(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = math.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)
 
    def rot_z(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = math.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)
 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        if viewer_distance + self.z != 0:
            factor = fov / (viewer_distance + self.z)
        else:
            factor = fov / (viewer_distance + 0.1 + self.z)
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


class Object:
    def __init__(self, color_=WHITE, size=256, xpos=0, ypos=0, zpos=0):
        self.color = color_
        self.size = size
        self.xpos, self.ypos, self.zpos = xpos, ypos, zpos
        self.xangle, self.yangle, self.zangle = 0, 0, 0
        self.vertices = []

    def _draw(self, screen, var):
        if var < 0 or var > 2:
            raise NotImplementedError

        t = []
        for v in self.vertices:
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            r = v.rot_x(self.xangle).rot_y(self.yangle).rot_z(self.zangle)
            # Transform the point from 3D to 2D
            p = r.project(screen.get_width(), screen.get_height(), 2, 4 + self.zpos)
            # Append the projection to the 2D vertices list
            t.append(p)
            # Draw points
            if not var:
                screen.fill(self.color, (p.x + self.xpos, p.y + self.ypos, 2, 2))
        return t

    def draw(self, *args):
        self._draw(*args)
        raise NotImplementedError

    def rot_x(self, d=1):
        self.xangle += d

    def rot_y(self, d=1):
        self.yangle += d

    def rot_z(self, d=1):
        self.zangle += d

    def _move(self, x=0, y=0, z=0):
        for p in self.vertices:
            p.x += x
            p.y += y
            p.z += z

    def mov_x(self, d=1):
        self._move(x=d)
        self.xpos += d

    def mov_y(self, d=1):
        self._move(y=d)
        self.ypos += d

    def mov_z(self, d=1):
        self._move(z=d)
        self.zpos += d

    def get_vertices(self):
        return [(i[0] + self.xpos, i[1] + self.ypos, i[2] + self.zpos) for i in self.vertices]

    def get_2D_pos(self, screen):
        return [tuple(v.project(screen.get_width(), screen.get_height(), self.size, 4 + self.zpos)) for v in
                self.vertices]