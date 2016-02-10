import math


class Camera(object):
    def __init__(self, x, y, dirx, diry, planex, planey):
        self.x = float(x)
        self.y = float(y)
        self.dirx = float(dirx)
        self.diry = float(diry)
        self.planex = float(planex)
        self.planey = float(planey)


class Point3D:
    def __init__(self, x=0, y=0, z=0):
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
        return (self.x, self.y, self.z)
 
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