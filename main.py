# Import standard modules.
import argparse
import sys

# Import non-standard modules.
import pygame as pg
from pygame.locals import *

# Import local modules
from boid import Boid

default_boids = 50
default_geometry = "1000x1000"


def update(dt, boids):
    """
    Update game. Called once per frame.
    dt is the amount of time passed since last frame.
    If you want to have constant apparent movement no matter your framerate,
    what you can do is something like

    x += v * dt

    and this will scale your velocity based on time. Extend as necessary."""

    # Go through events that are passed to the script by the window.
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == pg.K_q:
                pg.quit()
                sys.exit(0)
            elif event.key == pg.K_UP:
                add_boids(boids, 10)
            elif event.key == pg.K_DOWN:
                boids.remove(boids.sprites()[:10])
            elif event.key == pg.K_r:
                num_boids = len(boids)
                boids.empty()
                add_boids(boids, num_boids)

    for b in boids:
        b.update(dt, boids)


def draw(screen, background, boids):
    """
    Draw things to the window. Called once per frame.
    """

    # Redraw screen here
    boids.clear(screen, background)
    dirty = boids.draw(screen)

    # Flip the display so that the things we drew actually show up.
    pg.display.update(dirty)


def main(args):
    # Initialise pg.
    pg.init()

    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])

    # Set up the clock to maintain a relatively constant framerate.
    fps = 60.0
    fpsClock = pg.time.Clock()

    # Set up the window.
    logo = pg.image.load("logo32x32.png")
    pg.display.set_icon(logo)
    pg.display.set_caption("BOIDS!")
    window_width, window_height = [int(x) for x in args.geometry.split("x")]
    flags = DOUBLEBUF

    screen = pg.display.set_mode((window_width, window_height), flags)
    screen.set_alpha(None)
    background = pg.Surface(screen.get_size()).convert()
    background.fill(pg.Color('black'))

    boids = pg.sprite.RenderUpdates()

    add_boids(boids, args.num_boids)

    # Main game loop.
    dt = 1/fps  # dt is the time since last frame.

    # Loop forever!
    while True:
        update(dt, boids)
        draw(screen, background, boids)
        dt = fpsClock.tick(fps)


def add_boids(boids, num_boids):
    for _ in range(num_boids):
        boids.add(Boid())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Emergent flocking.')
    parser.add_argument('--geometry', metavar='WxH', type=str,
                        default=default_geometry, help='geometry of window')
    parser.add_argument('--number', dest='num_boids', default=default_boids,
                        help='number of boids to generate')
    args = parser.parse_args()

    main(args)
