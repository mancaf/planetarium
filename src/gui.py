import pygame
from . import guiconfig
from .simulate import System


class Gui:

    def __init__(self, system):
        self.system = system
        self.screen = pygame.display.set_mode(guiconfig.SCREEN.SIZE)
        self.clock = pygame.time.Clock()
        self.colors = {}
        for body in self.system.bodies:
            self.colors[body.name] = guiconfig.COLORS.random()

    def update(self):
        self.system.update()

    def draw(self):
        self.screen.fill(guiconfig.COLORS.BLACK)
        for body in self.system.bodies:
            pygame.draw.circle(
                self.screen,
                self.colors[body.name],
                screen_coords(body),
                screen_radius(body),
            )
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(guiconfig.TIME.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()
            self.draw()

    @staticmethod
    def from_file(planetfilename):
        return Gui(System.from_file(planetfilename))


def screen_coords(body):
    return (guiconfig.SCREEN.WIDTH // 2 + int(200 * body.pos.x),
            guiconfig.SCREEN.HEIGHT // 2 + int(-200 * body.pos.y))


def screen_radius(body):
    return int(10 * body.mass ** .1)