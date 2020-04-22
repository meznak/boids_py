import pygame as pg
from random import uniform
from vehicle import Vehicle


class Boid(Vehicle):

    # CONFIG
    min_speed = .2
    max_speed = 3
    max_force = .05
    perception = 50
    crowding = 30
    can_wrap = False
    edge_distance_pct = 5
    ###############

    def __init__(self):
        Boid.set_boundary(Boid.edge_distance_pct)

        # Randomize starting position and velocity
        start_position = pg.math.Vector2(
            uniform(0, Boid.max_x),
            uniform(0, Boid.max_y))
        start_velocity = pg.math.Vector2(
            uniform(-1, 1) * Boid.max_speed,
            uniform(-1, 1) * Boid.max_speed)

        super().__init__(start_position, start_velocity,
                         Boid.min_speed, Boid.max_speed,
                         Boid.max_force, Boid.can_wrap)

        self.rect = self.image.get_rect(center=self.position)

        self.accel = pg.math.Vector2()

    def separation(self, boids):
        steering = pg.Vector2()
        count = 0
        for boid in boids:
            dist = self.position.distance_to(boid.position)
            if dist < self.crowding:
                diff = pg.Vector2(self.position - boid.position)
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
            steering += boid.velocity
        steering /= len(boids)
        steering = self.clamp_force(steering)
        return steering

    def cohesion(self, boids):
        steering = pg.Vector2()
        for boid in boids:
            steering += boid.position
        steering /= len(boids)
        steering -= self.position
        steering = self.clamp_force(steering)
        return steering

    def update(self, dt, boids):
        neighbors = self.get_neighbors(boids)
        if neighbors:

            separation = self.separation(neighbors)
            alignment = self.alignment(neighbors)
            cohesion = self.cohesion(neighbors)
            if not self.can_wrap:
                avoid_edge = self.avoid_edge()
            else:
                avoid_edge = pg.Vector2()

            steering = separation + alignment + cohesion + avoid_edge
        else:
            steering = pg.Vector2()

        super().update(dt, steering)

    def get_neighbors(self, boids):
        neighbors = []
        for boid in boids:
            if boid != self:
                dist = self.position - boid.position
                if dist.magnitude() < self.perception:
                    neighbors.append(boid)
        return neighbors
