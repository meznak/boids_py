from boid import Boid
import pygame as pg


def main():
    pg.init()
    logo = pg.image.load("logo32x32.png")
    pg.display.set_icon(logo)
    pg.display.set_caption("BOIDS!")

    # CONFIG
    width = 1400
    height = 1000

    num_boids = 30
    ##################

    screen = pg.display.set_mode((width, height))

    running = True
    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])

    all_sprites = pg.sprite.Group()

    boids = [Boid() for i in range(num_boids)]
    for boid in boids:
        all_sprites.add(boid)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        for b in boids:
            b.update(boids)

        all_sprites.update(boids)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pg.display.flip()


if __name__ == "__main__":
    main()
