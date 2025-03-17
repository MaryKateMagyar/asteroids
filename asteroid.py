import pygame
import random
import circleshape as cs
import constants as c

class Asteroid(cs.CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        random_angle = random.uniform(20, 50)
        split_vector1 = self.velocity.rotate(random_angle)
        split_vector2 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - c.ASTEROID_MIN_RADIUS

        self.kill()
        if self.radius <= c.ASTEROID_MIN_RADIUS:
            return
        new_asteroid1 = Asteroid(self.position[0], self.position[1], new_radius)
        new_asteroid1.velocity = split_vector1 * 1.2

        new_asteroid2 = Asteroid(self.position[0], self.position[1], new_radius) 
        new_asteroid2.velocity = split_vector2 * 1.2     