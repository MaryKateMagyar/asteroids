# circleshape.py:
# Copied directly from boot.dev as part of the guided Asteroids project
# Used as a base class for the Asteroid, Player, and Shot classes

import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def check_collisions(self, target):
        distance = self.position.distance_to(target.position)
        return distance <= self.radius + target.radius

