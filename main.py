import sys
import pygame
import constants as c
import game_systems as gs

def main():
    print("Starting Asteroids!")

    screen, clock, updatable_group, drawable_group, asteroids_group, shots_group = gs.setup()
    player_character, asteroid_field = gs.setup_game_objects(updatable_group, drawable_group, asteroids_group, shots_group)
    dt = 0

    while True:
        gs.handle_events()
        gs.render_screen(screen, drawable_group)
        gs.update_game_state(updatable_group, asteroids_group, shots_group, player_character, dt)
        pygame.display.flip()
        dt = clock.tick(cs.FRAME_RATE) / 1000


if __name__ == "__main__":
    main()