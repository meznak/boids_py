import math
import pygame as pg
from random import random


class Boid:
    # image = pg.image.load("boid.png")
    image = pg.Surface((20, 10), pg.SRCALPHA)
    pg.draw.polygon(image, pg.Color('white'),
                    [(0, 0), (20, 10), (0, 20)])

    max_x = 0
    max_y = 0

    max_vel = .5

    def __init__(self):
        if Boid.max_x == 0:
            info = pg.display.Info()
            Boid.max_x = info.current_w
            Boid.max_y= info.current_h

        self.pos = pg.math.Vector2(random() * Boid.max_x, random() * Boid.max_y)
        self.rect = self.image.get_rect(center=self.pos)
        self.vel = pg.math.Vector2(random() * Boid.max_vel, random() * Boid.max_vel)

    def update(self, boids):
        self.pos += + self.vel
        self.wrap()
        _, angle = self.vel.as_polar()
        # angle = angle * math.pi / 180
        self.image = pg.transform.rotate(Boid.image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def wrap(self):
        if self.pos.x < 0:
            self.pos.x += Boid.max_x
        elif self.pos.x > Boid.max_x:
            self.pos.x -= Boid.max_x

        if self.pos.y < 0:
            self.pos.y += Boid.max_y
        elif self.pos.y > Boid.max_y:
            self.pos.y -= Boid.max_y
