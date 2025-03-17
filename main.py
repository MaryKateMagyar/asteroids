import sys
import pygame
import constants as c
import player_module as p
import asteroid_module as a

def main():
    pygame.init()

    print("Starting Asteroids!")

    screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group()
    asteroids_group = pygame.sprite.Group()
    shots_group = pygame.sprite.Group()

    p.Player.containers = (updatable_group, drawable_group)
    player_character = p.Player((c.SCREEN_WIDTH / 2), (c.SCREEN_HEIGHT / 2))

    a.Asteroid.containers = (asteroids_group, updatable_group, drawable_group)

    a.AsteroidField.containers = (updatable_group)
    asteroid_field = a.AsteroidField()

    p.Shot.containers = (shots_group, updatable_group, drawable_group)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill((0, 0, 0))
        for sprite in drawable_group:
            sprite.draw(screen)
        updatable_group.update(dt)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            player_character.shoot(shots_group)
        for asteroid in asteroids_group:
            for shot in shots_group:
                if shot.check_collisions(asteroid) == True:
                    shot.kill()
                    asteroid.split()
            if asteroid.check_collisions(player_character) == True:
                print("Game over!")
                sys.exit()
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()