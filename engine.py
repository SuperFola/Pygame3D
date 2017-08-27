import pygame
import os
from pygame.locals import *
from operator import itemgetter
from basis import *


texWidth = 64
texHeight = 64


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


class Square(Object):
    def __init__(self, color_=WHITE, size=256, xpos=0, ypos=0, zpos=0):
        super().__init__(color_, size, xpos, ypos, zpos)
        self.vertices = [
            Point3D(0, 0, 0),
            Point3D(1, 0, 0),
            Point3D(1, 1, 0),
            Point3D(0, 1, 0)
        ]
        self._move(
            x=self.xpos,
            y=self.ypos,
            z=self.zpos
        )

    def draw(self, screen, var=0):
        t = self._draw(screen, var)
        if var == 1:
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos),
                             (t[1].x + self.xpos, t[1].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[1].x + self.xpos, t[1].y + self.ypos),
                             (t[2].x + self.xpos, t[2].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[2].x + self.xpos, t[2].y + self.ypos),
                             (t[3].x + self.xpos, t[3].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[3].x + self.xpos, t[3].y + self.ypos),
                             (t[0].x + self.xpos, t[0].y + self.ypos))
        elif var == 2:
            vertices = [
                (t[0].x + self.xpos, t[0].y + self.ypos),
                (t[1].x + self.xpos, t[1].y + self.ypos),
                (t[2].x + self.xpos, t[2].y + self.ypos),
                (t[3].x + self.xpos, t[3].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, vertices)


class Line(Object):
    def __init__(self, color_=WHITE, size=64, xpos=0, ypos=0, zpos=0, xdir=1, ydir=1, zdir=1):
        super().__init__(color_, size, xpos, ypos, zpos)
        self.xdir, self.ydir, self.zdir = xdir, ydir, zdir
        self.vertices = [
            Point3D(0, 0, 0),
            Point3D(self.xdir, self.ydir, self.zdir)
        ]
        self._move(
            x=self.xpos,
            y=self.ypos,
            z=self.zpos
        )

    def draw(self, screen, var=0):
        t = self._draw(screen, var)
        if var in (1, 2):
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos),
                             (t[1].x + self.xpos, t[1].y + self.ypos))


class Pyramid(Object):
    def __init__(self, color_=WHITE, size=256, xpos=0, ypos=0, zpos=0):
        super().__init__(color_, size, xpos, ypos, zpos)
        self.vertices = [
            Point3D(0, +1, 0),
            Point3D(-1, -1, 1),
            Point3D(-1, -1, -1),
            Point3D(1, -1, 1),
            Point3D(1, -1, -1)
        ]
        self._move(
            x=self.xpos,
            y=self.ypos,
            z=self.zpos
        )

    def draw(self, screen, var=0):
        t = self._draw(screen, var)
        if var == 1:
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos),
                             (t[1].x + self.xpos, t[1].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos),
                             (t[2].x + self.xpos, t[2].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos),
                             (t[3].x + self.xpos, t[3].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[0].x + self.xpos, t[0].y + self.ypos),
                             (t[4].x + self.xpos, t[4].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[1].x + self.xpos, t[1].y + self.ypos),
                             (t[2].x + self.xpos, t[2].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[2].x + self.xpos, t[2].y + self.ypos),
                             (t[4].x + self.xpos, t[4].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[3].x + self.xpos, t[3].y + self.ypos),
                             (t[4].x + self.xpos, t[4].y + self.ypos))
            pygame.draw.line(screen, self.color, (t[1].x + self.xpos, t[1].y + self.ypos),
                             (t[3].x + self.xpos, t[3].y + self.ypos))
        elif var == 2:
            vertices = [
                (t[0].x + self.xpos, t[0].y + self.ypos), (t[1].x + self.xpos, t[1].y + self.ypos),
                (t[2].x + self.xpos, t[2].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, vertices)
            vertices = [
                (t[0].x + self.xpos, t[0].y + self.ypos), (t[2].x + self.xpos, t[2].y + self.ypos),
                (t[4].x + self.xpos, t[4].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, vertices)
            vertices = [
                (t[0].x + self.xpos, t[0].y + self.ypos), (t[3].x + self.xpos, t[3].y + self.ypos),
                (t[4].x + self.xpos, t[4].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, vertices)
            vertices = [
                (t[0].x + self.xpos, t[0].y + self.ypos), (t[1].x + self.xpos, t[1].y + self.ypos),
                (t[2].x + self.xpos, t[2].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, vertices)
            vertices = [
                (t[1].x + self.xpos, t[1].y + self.ypos), (t[2].x + self.xpos, t[2].y + self.ypos),
                (t[4].x + self.xpos, t[4].y + self.ypos), (t[3].x + self.xpos, t[3].y + self.ypos)
            ]
            pygame.draw.polygon(screen, self.color, vertices)


class Crate(Object):
    def __init__(self, color_=WHITE, size=256, xpos=0, ypos=0, zpos=0):
        super().__init__(color_, size, xpos, ypos, zpos)
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
        self._move(
            x=self.xpos,
            y=self.ypos,
            z=self.zpos
        )
        self.faces = [
            (0, 1, 2, 3),
            (1, 5, 6, 2),
            (5, 4, 7, 6),
            (4, 0, 3, 7),
            (0, 4, 5, 1),
            (3, 2, 6, 7)
        ]

    def draw(self, screen, var=0):
        t = self._draw(screen, var)
        if var == 1:
            for f in self.faces:
                pygame.draw.line(screen, self.color, (t[f[0]].x + self.xpos, t[f[0]].y + self.ypos),
                                 (t[f[1]].x + self.xpos, t[f[1]].y + self.ypos))
                pygame.draw.line(screen, self.color, (t[f[1]].x + self.xpos, t[f[1]].y + self.ypos),
                                 (t[f[2]].x + self.xpos, t[f[2]].y + self.ypos))
                pygame.draw.line(screen, self.color, (t[f[2]].x + self.xpos, t[f[2]].y + self.ypos),
                                 (t[f[3]].x + self.xpos, t[f[3]].y + self.ypos))
                pygame.draw.line(screen, self.color, (t[f[3]].x + self.xpos, t[f[3]].y + self.ypos),
                                 (t[f[0]].x + self.xpos, t[f[0]].y + self.ypos))
        elif var == 2:
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


class Sphere(Object):
    def __init__(self, color_=WHITE, size=256, xpos=0, ypos=0, zpos=0, radius=2):
        super().__init__(color_, size, xpos, ypos, zpos)
        self.radius = radius
        self.vertices = [
            Point3D(0, 0, 0)
        ]
        self._move(
            x=self.xpos,
            y=self.ypos,
            z=self.zpos
        )

    def draw(self, screen, var=0):
        t = self._draw(screen, var)
        radius = abs(-self.radius * (self.size / (4 - self.zpos)))
        pygame.draw.circle(screen, self.color, (int(t[0].x) + self.xpos, int(t[0].y) + self.ypos), int(radius), 1 if var == 1 else 0)


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
        self.xangle = 0
        self.yangle = 0
        self.zangle = 0
        self.font = pygame.font.SysFont("arial", 12)
        self.axeX = self.font.render("X", 1, WHITE)
        self.axeY = self.font.render("Y", 1, WHITE)
        self.axeZ = self.font.render("Z", 1, WHITE)

    def add(self, *objects):
        for o in objects:
            self.objects.append(o)

    def draw_axis(self, screen):
        t = []
        for axe in self.axis:
            r = axe.rot_x(self.xangle).rot_y(self.yangle).rot_z(self.zangle)
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
        for o in self.objects:
            if only_visible:
                p = sorted(o.get_2D_pos(screen))[0]
                if 0 <= p[0] <= screen.get_width() and 0 <= p[1] <= screen.get_height():
                    o.draw(screen, var)
            else:
                o.draw(screen, var)

    def rot_x(self, d=1):
        self.xangle += d
        for o in self.objects:
            o.rot_x(d)

    def rot_y(self, d=1):
        self.yangle += d
        for o in self.objects:
            o.rot_y(d)

    def rot_z(self, d=1):
        self.zangle += d
        for o in self.objects:
            o.rot_z(d)

    def mov_x(self, d=1):
        for o in self.objects:
            o.mov_x(d)

    def mov_y(self, d=1):
        for o in self.objects:
            o.mov_y(d)

    def mov_z(self, d=1):
        for o in self.objects:
            o.mov_z(d)


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
        for o in objects:
            self.static_objects.append(o)

    def rotateX(self, d):
        self.plan.rot_x(d)

    def rotateY(self, d):
        self.plan.rot_y(d)

    def rotateZ(self, d):
        self.plan.rot_z(d)

    def rotate_objects(self):
        self.plan.rot_y(self.p_rotat[0])
        self.plan.rot_x(self.p_rotat[1])
        self.plan.rot_z(self.p_rotat[2])

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