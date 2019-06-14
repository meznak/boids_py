from boid import Boid
import pygame as pg


def main():
    pg.init()
    logo = pg.image.load("logo32x32.png")
    pg.display.set_icon(logo)
    pg.display.set_caption("BOIDS!")

    # CONFIG
    width = 800
    height = 600

    num_boids = 10
    ##################

    screen = pg.display.set_mode((width, height))

    running = True

    boids = [Boid() for i in range(num_boids)]

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill((0, 0, 0), rect=None)
        for b in boids:
            b.update(boids)
            screen.blit(b.image, b.pos)
        pg.display.flip()


if __name__ == "__main__":
    main()
