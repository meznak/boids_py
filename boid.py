import pygame as pg
from random import uniform
from vehicle import Vehicle


class Boid(Vehicle):

    # CONFIG
    min_speed = .01
    max_speed = .2
    max_force = .3
    max_turn = 5
    perception = 60
    crowding = 40
    can_wrap = False
    edge_distance_pct = 10
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
        for boid in boids:
            dist = self.position.distance_to(boid.position)
            if dist < self.crowding:
                steering -= boid.position - self.position
        steering = self.clamp_force(steering)
        return steering

    def alignment(self, boids):
        steering = pg.Vector2()
        for boid in boids:
            steering += boid.velocity
        steering /= len(boids)
        steering -= self.velocity
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

            # DEBUG
            # separation.scale_to_length(0)
            # alignment.scale_to_length(0)
            # cohesion.scale_to_length(0)

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
