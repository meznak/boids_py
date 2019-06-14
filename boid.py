import pygame as pg
from random import uniform


class Boid(pg.sprite.Sprite):
    image = pg.Surface((20, 10), pg.SRCALPHA)
    pg.draw.polygon(image, pg.Color('white'),
                    [(0, 0), (20, 10), (0, 20)])

    max_x = 0
    max_y = 0

    # CONFIG
    min_speed = .8
    max_speed = 2
    max_force = .01
    perception = 50
    crowding = 30
    ###############

    def __init__(self):
        super(Boid, self).__init__()

        if Boid.max_x == 0:
            info = pg.display.Info()
            Boid.max_x = info.current_w
            Boid.max_y= info.current_h

        self.image = Boid.image.copy()
        self.rect = self.image.get_rect()

        self.pos = pg.math.Vector2(
            uniform(0, Boid.max_x),
            uniform(0, Boid.max_y))
        self.rect = self.image.get_rect(center=self.pos)

        while True:
            self.vel = pg.math.Vector2(
                uniform(-1, 1) * Boid.max_speed,
                uniform(-1, 1) * Boid.max_speed)
            if self.vel.magnitude() != 0:
                break

        self.accel = pg.math.Vector2()

    def separation(self, boids):
        steering = pg.Vector2()
        count = 0
        for boid in boids:
            dist = self.pos.distance_to(boid.pos)
            if dist < self.crowding:
                diff = pg.Vector2(self.pos - boid.pos)
                diff /= dist
                steering += diff
                count += 1
        if count:
            steering /= count
        steering = self.clamp_force(steering)
        return steering

    def alignment(self, boids):
        steering = pg.Vector2()
        for boid in boids:
            steering += boid.vel
        steering /= len(boids)
        steering = self.clamp_force(steering)
        return steering

    def cohesion(self, boids):
        steering = pg.Vector2()
        for boid in boids:
            steering += boid.pos
        steering /= len(boids)
        steering -= self.pos
        steering = self.clamp_force(steering)
        return steering

    def update(self, boids):
        # update velocity
        neighbors = self.get_neighbors(boids)
        if neighbors:
            separation = pg.Vector2()
            alignment = pg.Vector2()
            cohesion = pg.Vector2()

            separation = self.separation(neighbors)
            alignment = self.alignment(neighbors)
            cohesion = self.cohesion(neighbors)

            self.accel = separation + alignment + cohesion
        else:
            self.accel = pg.Vector2()

        # move and turn
        self.pos += + self.vel
        self.wrap()
        _, angle = self.vel.as_polar()

        self.vel += self.accel

        # enforce speed limit
        while self.vel.magnitude() < self.min_speed:
            _, angle = self.vel.as_polar()
            self.vel.from_polar((self.min_speed * 1.1, angle))

        if self.vel.magnitude() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        # make boid
        self.image = pg.transform.rotate(Boid.image, -angle)
        self.rect = self.image.get_rect(center=self.pos)

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

    def clamp_force(self, force):
        if force.magnitude() > self.max_speed:
            force = force.normalize() * self.max_speed
        force -= self.vel
        if force.magnitude() > self.max_force:
            force = force.normalize() * self.max_force
        return force