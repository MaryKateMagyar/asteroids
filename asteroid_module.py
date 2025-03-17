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


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-c.ASTEROID_MAX_RADIUS, y * c.SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                c.SCREEN_WIDTH + c.ASTEROID_MAX_RADIUS, y * c.SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * c.SCREEN_WIDTH, -c.ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * c.SCREEN_WIDTH, c.SCREEN_HEIGHT + c.ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > c.ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, c.ASTEROID_KINDS)
            self.spawn(c.ASTEROID_MIN_RADIUS * kind, position, velocity)