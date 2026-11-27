import threading

import pygame
from pygame import Vector2

# pygame setup
pygame.init()
E = (192, 132)
screen = pygame.display.set_mode(E, flags=pygame.NOFRAME)
clock = pygame.time.Clock()
running = True
dt = 0
msb = 72
BUFFER = 6.7
MSBE = E[0] - 20 - BUFFER
MSBL = 6.7
X = 67 + 16

class RaT:
    def __init__(self, duration):
        super().__init__()
        self.sprites = [pygame.image.load('smth/idleboyo/pixil-frame-0.png'),
                        pygame.image.load('smth/idleboyo/pixil-frame-1.png'),
                        pygame.image.load('smth/idleboyo/pixil-frame-2.png'),
                        pygame.image.load('smth/idleboyo/pixil-frame-3.png'),
                        pygame.image.load('smth/idleboyo/pixil-frame-4.png'),
                        pygame.image.load('smth/idleboyo/pixil-frame-5.png')]
        self.max_index = len(self.sprites) - 1
        self.current_index = 0
        self.frame_duration = duration
        self.anim_timer = 0.0

    def update(self, dt):
        """ Increment index by 1 and reset if index is larger than max index """
        self.anim_timer += dt
        if self.anim_timer >= self.frame_duration:
            if self.current_index < self.max_index:
                self.current_index += 1
            else:
                self.current_index = 0
            self.anim_timer = 0

    def draw(self, screen, x, y):
        screen.blit(self.sprites[self.current_index], (x, y))

rat = (RaT(duration=1))
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    bg = pygame.image.load("bagound.png").convert_alpha()

    # INSIDE OF THE GAME LOOP
    screen.blit(bg, (0, 0))

    rat.update(dt)
    rat.draw(screen=screen, x=msb, y=X)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        msb -= 300 * dt
    if keys[pygame.K_d]:
        msb += 300 * dt
    msb = (min(max(msb, MSBL), MSBE))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()