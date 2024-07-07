import sys
from random import randrange

import pygame
from pygame.locals import *


class Weight(pygame.sprite.Sprite):

    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        # image and rect used when drawing sprite:
        self.image = weight_image
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        """
        Move the weight to a random position at the top of the screen.
        """
        self.rect.top = -self.rect.height
        self.rect.centerx = randrange(screen_size[0])

    def update(self):
        """
        Update the weight for display in the next frame.
        """
        self.rect.top += self.speed

        if self.rect.top > screen_size[1]:
            self.reset()


# Initialize things
pygame.init()
screen_size = 800, 600
pygame.display.set_mode(screen_size)
pygame.mouse.set_visible(False)

# Load the weight image
weight_image = pygame.image.load('weight.png')
weight_image = weight_image.convert_alpha()  # ... to match the display

# You might want a different speed, of course
speed = 5

# Create a sprite group and add a Weight
sprites = pygame.sprite.RenderUpdates()
sprites.add(Weight(speed))

# Get the screen surface and fill it
screen = pygame.display.get_surface()
bg = (255, 255, 255)  # White
screen.fill(bg)
pygame.display.flip()

# To limit frame rate
clock = pygame.time.Clock()


# Used to erase the sprites:
def clear_callback(surf, rect):
    surf.fill(bg, rect)


while True:
    # Check for quit events:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
    # Erase previous positions:
    sprites.clear(screen, clear_callback)
    # Update all sprites:
    sprites.update()
    # Draw all sprites:
    updates = sprites.draw(screen)
    # Update the necessary parts of the display:
    pygame.display.update(updates)
    # Limit frame rate
    clock.tick(60)
