# main.py: Entry point for the Asteroids game
# This file initalizes the game, handles the game loop, and ensures proper resource cleanup

# Standard Library Imports - Used for systen-level operations
import sys

# Third-Party Imports - External game libraries
import pygame

# Local Module Imports - Game-specific modules
import constants as c
import game_systems as gs


def main():
    # Main function - Initializes and runs the Asteroids game

    print("Starting Asteroids!")

    # --- GAME SETUP ---
    # Initialize the game screen, clock, and sprite groups for game assets
    # 'gs.setup()' is responsible for setting up everything Pygame needs
    screen, clock, updatable_group, drawable_group, asteroids_group, shots_group = gs.setup()

    # Create the player character and initial asteroid field
    # All objects are added to the necessary groups for updates and rendering
    player_character, asteroid_field = gs.setup_game_objects(updatable_group, drawable_group, asteroids_group, shots_group)
    
    # 'dt' (delta time): Measures the time between frames to allow for frame-independent motion
    dt = 0

    try:
        # --- GAME LOOP ---
        # The core loop that runs the game, processing events, rendering, and updating game logic
        # This will run continuously
        while True:
            # 1. Handles events, specifically the player quitting the game
            #    This ensures the player can interact with the game properly
            gs.handle_events()

            # 2. Render all game objects on the screen
            #    Drawable objects from the 'drawable_group' are drawn to the 'screen' surface
            gs.render_screen(screen, drawable_group)

            # 3. Update the game's logic and state
            #    Handles object movement, collisions, and interactions between:
            #    - 'updatable_group' (all objects needing logic updates),
            #    - 'asteroids_group' (asteroids moving and splitting),
            #    - 'shots_group' (player bullets),
            #    - 'player_character'.
            #    The game's delta time ('dt') ensures movements and updates are frame-independent
            gs.update_game_state(updatable_group, asteroids_group, shots_group, player_character, dt)

            # 4. Update the game's display with the most recent rendered frame
            #    Flips the off-screen buffer to the screen, making the most recent rendering visible
            pygame.display.flip()

            # 5. Control the game's frame rate and calculate delta time ('dt')
            #    - 'clock.time(c.FRAME_RATE)': Ensures the game runs at a consistent FPS
            #    - Divide by 100 to convert milliseconds into seconds for use in delta-time calculations
            dt = clock.tick(c.FRAME_RATE) / 1000  # Frame time in seconds

    except Exception as e:
        # Catch and handle unecpected errors that may occur during the game loop
        # Print an error message to indicate what went wrong,
        # along with the exception fetails for debugging
        print("An error occurred during the game loop!")
        print(f"Error details: {e}")

    finally:
        # Ensure proper cleanup of game resources, even if an error occurs
        # - `pygame.quit()` ensures Pygame shuts down cleanly
        # - `sys.exit()` terminates the program safely
        print("Exiting game. Cleaning up resources.")
        pygame.quit()
        sys.exit()
    

if __name__ == "__main__":
    main()