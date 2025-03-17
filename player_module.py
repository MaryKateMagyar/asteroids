import pygame
import circleshape as cs
import constants as c


class Player(cs.CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, c.PLAYER_RADIUS)
        self.rotation = 0
        self.shot_timer = c.PLAYER_SHOOT_COOLDOWN

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, c.ASSET_COLOR, self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += (c.PLAYER_TURN_SPEED * dt)

    def update(self, dt):
        self.shot_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt) 
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * c.PLAYER_SPEED * dt

    def shoot(self, shots_group):
        if self.shot_timer <= 0:
            shot = Shot(self.position[0], self.position[1], c.SHOT_RADIUS)
            shot.velocity = (pygame.Vector2(0, 1).rotate(self.rotation)) * c.PLAYER_SHOOT_SPEED
            shots_group.add(shot)
            self.shot_timer += c.PLAYER_SHOOT_COOLDOWN


class Shot(cs.CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, c.ASSET_COLOR, self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt