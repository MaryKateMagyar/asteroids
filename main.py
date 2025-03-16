import pygame
import constants as c
import player as p
import asteroid as a

def main():
    pygame.init()

    print("Starting Asteroids!")
    print(f"Screen width: {c.SCREEN_WIDTH}")
    print(f"Screen height: {c.SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group()
    asteroids_group = pygame.sprite.Group()

    p.Player.containers = (updatable_group, drawable_group)
    player_character = p.Player((c.SCREEN_WIDTH / 2), (c.SCREEN_HEIGHT / 2))

    a.Asteroid.containers = (asteroids_group, updatable_group, drawable_group)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill((0, 0, 0))
        for sprite in drawable_group:
            sprite.draw(screen)
        updatable_group.update(dt)
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()