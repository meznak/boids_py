import pygame as pg
from random import randrange


class Boid:
    image = pg.Surface((20, 10), pg.SRCALPHA)
    pg.draw.polygon(image, pg.Color('white'),
                    [(0, 0), (20, 10), (0, 20)])

    max_x = 0
    max_y = 0

    max_vel = 1
    max_steer = 1
    perception = 80
    crowding = 50

    def __init__(self):
        if Boid.max_x == 0:
            info = pg.display.Info()
            Boid.max_x = info.current_w
            Boid.max_y= info.current_h

        self.pos = pg.math.Vector2(
            randrange(0, Boid.max_x),
            randrange(0, Boid.max_y))
        self.rect = self.image.get_rect(center=self.pos)
        self.vel = pg.math.Vector2(
            randrange(-1, 1) * Boid.max_vel,
            randrange(-1, 1) * Boid.max_vel)
        self.force = pg.math.Vector2()

    def separation(self, boids):
        diff = pg.Vector2()
        force = pg.Vector2()
        for boid in boids:
            if self.pos.distance_to(boid.pos) < self.crowding:
                diff = pg.Vector2(self.pos - boid.pos)
                diff /= self.pos.distance_squared_to(boid.pos)
                # diff.scale_to_length(1 / self.pos.distance_to(boid.pos))
                self.force += diff

    def alignment(self, boids):
        group_v = pg.Vector2()
        for boid in boids:
            group_v += boid.vel
        group_v /= len(boids)
        self.force += group_v

    def cohesion(self, boids):
        group_pos = pg.Vector2()
        for boid in boids:
            group_pos += boid.pos
        group_pos / len(boids)
        self.force -= self.pos

    def update(self, boids):
        # update velocity
        self.force *= 0
        neighbors = self.get_neighbors(boids)
        if neighbors:
            self.separation(neighbors)
            self.alignment(neighbors)
            self.cohesion(neighbors)

            # enforce force limit
            angle_diff = self.vel.angle_to(self.force)
            steer = clamp(angle_diff, -self.max_steer, self.max_steer)
            self.force.rotate_ip(-angle_diff + steer)

            self.vel += self.force

            # enforce speed limit
            if self.vel.magnitude() > self.max_vel:
                self.vel.scale_to_length(self.max_vel)

        # move and turn
        self.pos += + self.vel
        self.wrap()
        _, angle = self.vel.as_polar()

        # make boid
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

    def get_neighbors(self, boids):
        neighbors = []
        for boid in boids:
            if boid != self:
                dist = self.pos - boid.pos
                if dist.magnitude() < self.perception:
                    neighbors.append(boid)
        return neighbors

def clamp(value, min_val, max_val):
    """Clamp value to a given range"""
    return max(min_val, min(value, max_val))
