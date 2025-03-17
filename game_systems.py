import sys
import pygame
import constants as c
import player_module as p
import asteroid_module as a

# Setup Function
def setup():
    pygame.init()

    screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group()
    asteroids_group = pygame.sprite.Group()
    shots_group = pygame.sprite.Group()

    return screen, clock, updatable_group, drawable_group, asteroids_group, shots_group

# Setup for assets
def setup_game_objects(updatable_group, drawable_group, asteroids_group, shots_group):
    p.Player.containers = (updatable_group, drawable_group)
    player_character = p.Player((c.SCREEN_WIDTH / 2), (c.SCREEN_HEIGHT / 2))

    a.Asteroid.containers = (asteroids_group, updatable_group, drawable_group)

    a.AsteroidField.containers = (updatable_group)
    asteroid_field = a.AsteroidField()

    p.Shot.containers = (shots_group, updatable_group, drawable_group)

    return player_character, asteroid_field

# Event Handling
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

# Game Logic
def update_game_state(updatable_group, asteroids_group, shots_group, player_character, dt):
    updatable_group.update(dt)

    # Shooting Logic
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        player_character.shoot(shots_group)

    # Collision Handling
    for asteroid in asteroids_group:
        for shot in shots_group:
            if shot.check_collisions(asteroid) == True:
                shot.kill()
                asteroid.split()
        if asteroid.check_collisions(player_character) == True:
            print("Game over!")
            sys.exit()

# Rendering Logic
def render_screen(screen, drawable_group):
    screen.fill(c.BACKGROUND_COLOR)
    for sprite in drawable_group:
        sprite.draw(screen)