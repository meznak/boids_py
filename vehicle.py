import pygame as pg


class Vehicle(pg.sprite.Sprite):
    # default image is a li'l white triangle
    image = pg.Surface((10, 10), pg.SRCALPHA)
    pg.draw.polygon(image, pg.Color('white'),
                    [(15, 5), (0, 2), (0, 8)])

    def __init__(self, position, velocity, min_speed, max_speed,
                 max_force, can_wrap):

        super().__init__()

        # set limits
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.max_force = max_force

        # set position
        dimensions = len(position)
        assert (1 < dimensions < 4), "Invalid spawn position dimensions"

        if dimensions == 2:
            self.position = pg.Vector2(position)
            self.acceleration = pg.Vector2(0, 0)
            self.velocity = pg.Vector2(velocity)
        else:
            self.position = pg.Vector3(position)
            self.acceleration = pg.Vector3(0, 0, 0)
            self.velocity = pg.Vector3(velocity)

        self.heading = 0.0

        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt, steering):
        self.acceleration = steering * dt

        # enforce turn limit
        _, old_heading = self.velocity.as_polar()
        new_velocity = self.velocity + self.acceleration * dt
        speed, new_heading = new_velocity.as_polar()

        heading_diff = 180 - (180 - new_heading + old_heading) % 360
        if abs(heading_diff) > self.max_turn:
            if heading_diff > self.max_turn:
                new_heading = old_heading + self.max_turn
            else:
                new_heading = old_heading - self.max_turn

        self.velocity.from_polar((speed, new_heading))

        # enforce speed limit
        speed, self.heading = self.velocity.as_polar()
        if speed < self.min_speed:
            self.velocity.scale_to_length(self.min_speed)

        if speed > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # move
        self.position += self.velocity * dt

        if self.can_wrap:
            self.wrap()

        # draw
        self.image = pg.transform.rotate(Vehicle.image, -self.heading)

        if self.debug:
            center = pg.Vector2((50, 50))

            velocity = pg.Vector2(self.velocity)
            speed = velocity.length()
            velocity += center

            acceleration = pg.Vector2(self.acceleration)
            acceleration += center

            steering = pg.Vector2(steering)
            steering += center

            overlay = pg.Surface((100, 100), pg.SRCALPHA)
            overlay.blit(self.image, center - (10, 10))

            pg.draw.line(overlay, pg.Color('green'), center, velocity, 3)
            pg.draw.line(overlay, pg.Color('red'), center + (5, 0),
                         acceleration + (5, 0), 3)
            pg.draw.line(overlay, pg.Color('blue'), center - (5, 0),
                         steering - (5, 0), 3)

            self.image = overlay
            self.rect = overlay.get_rect(center=self.position)
        else:
            self.rect = self.image.get_rect(center=self.position)

    def avoid_edge(self):
        left = self.edges[0] - self.position.x
        up = self.edges[1] - self.position.y
        right = self.position.x - self.edges[2]
        down = self.position.y - self.edges[3]

        scale = max(left, up, right, down)

        if scale > 0:
            center = (Vehicle.max_x / 2, Vehicle.max_y / 2)
            steering = pg.Vector2(center)
            steering -= self.position
        else:
            steering = pg.Vector2()

        return steering

    def wrap(self):
        if self.position.x < 0:
            self.position.x += Vehicle.max_x
        elif self.position.x > Vehicle.max_x:
            self.position.x -= Vehicle.max_x

        if self.position.y < 0:
            self.position.y += Vehicle.max_y
        elif self.position.y > Vehicle.max_y:
            self.position.y -= Vehicle.max_y

    @staticmethod
    def set_boundary(edge_distance_pct):
        info = pg.display.Info()
        Vehicle.max_x = info.current_w
        Vehicle.max_y = info.current_h
        margin_w = Vehicle.max_x * edge_distance_pct / 100
        margin_h = Vehicle.max_y * edge_distance_pct / 100
        Vehicle.edges = [margin_w, margin_h, Vehicle.max_x - margin_w,
                         Vehicle.max_y - margin_h]

    def clamp_force(self, force):
        if 0 < force.magnitude() > self.max_force:
            force.scale_to_length(self.max_force)

        return force
