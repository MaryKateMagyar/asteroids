# game_systems.py: Core game loop and management systems for Asteroids game
# This module handles game initialization, object creation, event handling, game state updates, collision detection, and rendering.


# Standard Library Imports 
import sys # Used for systen-level operations like exiting the game

# Third-Party Imports - External game libraries
import pygame

# Local Module Imports - Game-specific modules
import constants as c # Game constants and configurations
import player_module as p # Player-related classes and functionality
import asteroid_module as a # Asteroid-related classes and functionality


def setup():
    """
    Initialize pygame and create essential game components.
    
    This function:
    - Initializes the pygame library
    - Creates the game window with dimensions from constants
    - Sets up a clock for managing frame rate
    - Creates sprite groups for organizing game objects
    
    Returns:
        tuple: Contains:
            - screen: pygame display surface for rendering
            - clock: pygame clock for controlling frame rate
            - updatable_group: sprite group for objects needing update logic
            - drawable_group: sprite group for objects that need to be rendered
            - asteroids_group: sprite group specifically for asteroid objects
            - shots_group: sprite group specifically for player shots
    """

    # Initialize pygame library
    pygame.init()

    # Create game window using dimensions from constants
    screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    # Create clock to manage game's frame rate
    clock = pygame.time.Clock()

    # Create sprite groups to organize and manage different types of game objects
    updatable_group = pygame.sprite.Group()  # Objects that need logic updates each frame
    drawable_group = pygame.sprite.Group()   # Objects that need to be drawn each frame
    asteroids_group = pygame.sprite.Group()  # Collection of asteroid objects for collision detection
    shots_group = pygame.sprite.Group()      # Collection of player shots for collision detection

    return screen, clock, updatable_group, drawable_group, asteroids_group, shots_group


def setup_game_objects(updatable_group, drawable_group, asteroids_group, shots_group):
    """
    Create and initialize all game objects and assign them to appropriate sprite groups.
    
    This function:
    - Sets up class containers for automatic sprite group assignment
    - Creates the player character at the center of the screen
    - Configures asteroid class sprite group assignments
    - Creates the asteroid field that will manage asteroid spawning
    - Sets up shot class sprite group assignments
    
    Args:
        updatable_group (pygame.sprite.Group): Group of all objects that need updating each frame
        drawable_group (pygame.sprite.Group): Group of all objects that need to be drawn
        asteroids_group (pygame.sprite.Group): Group of all asteroid objects
        shots_group (pygame.sprite.Group): Group of all player shot objects
    
    Returns:
        tuple: Contains:
            - player_character: The player's ship object
            - asteroid_field: Manager object that handles asteroid spawning
    """
    
    # Configure Player class to automatically add instances to these sprite groups
    p.Player.containers = (updatable_group, drawable_group)
    # Create player at the center of the screen
    player_character = p.Player((c.SCREEN_WIDTH / 2), (c.SCREEN_HEIGHT / 2))

    # Configure Asteroid class to automatically add instances to these sprite groups
    a.Asteroid.containers = (asteroids_group, updatable_group, drawable_group)

    # Configure AsteroidField class to automatically add to updatable_group for spawning logic
    a.AsteroidField.containers = (updatable_group)
    # Create the asteroid field manager
    asteroid_field = a.AsteroidField()

    # Configure Shot call to automatically add instances to these sprite groups
    p.Shot.containers = (shots_group, updatable_group, drawable_group)

    return player_character, asteroid_field


def handle_events():
    """
    Process all pygame events in the event queue.
    
    This function:
    - Retrieves all pending events from pygame's event queue
    - Handles system events like window close (QUIT)
    - Can be expanded to handle additional event types (keyboard, mouse, etc.)
    
    Returns:
        None: This function doesn't return a value, but may terminate the program
              if a QUIT event is detected.
    
    Note: 
        Calling sys.exit() when a QUIT event is detected ensures the game
        terminates cleanly when the user closes the window.
    """

    # Iterate through all pending pygame events
    for event in pygame.event.get():
        # Check if user has clicked the window close button
        if event.type == pygame.QUIT:
            # Exit the program cleanly
            sys.exit()


def update_game_state(updatable_group, asteroids_group, shots_group, player_character, dt):
    """
    Update the game state for the current frame.
    
    This function:
    - Updates all game objects with the elapsed time
    - Handles player shooting input
    - Detects and resolves collisions between:
      - Shots and asteroids
      - Player and asteroids
    
    Args:
        updatable_group (pygame.sprite.Group): Group of all objects that need updating each frame
        asteroids_group (pygame.sprite.Group): Group of all asteroid objects
        shots_group (pygame.sprite.Group): Group of all player shot objects
        player_character (Player): The player's ship object
        dt (float): Delta time - seconds elapsed since last frame
    
    Returns:
        None: This function updates the game state in-place.
              May terminate the program if the player is destroyed.
    """
    
    # Update all game objects with the time elapsed since last frame
    updatable_group.update(dt)

    # --- Shooting Logic ---
    # Check is space key is pressed
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        # Tell the player object to create a new shot
        # Append shot to 'shots_group'
        player_character.shoot(shots_group)

    # --- Collision Handling ---
    for asteroid in asteroids_group:
        # Check for collisions between each asteroid and all shots
        for shot in shots_group:
            if shot.check_collisions(asteroid) == True:
                # Shot hit an asteroid - remove the shot
                shot.kill()
                # Split the asteroid (which may create smaller asteroids)
                asteroid.split()

        # Check for collision between asteroid and player        
        if asteroid.check_collisions(player_character) == True:
            # Player was hit by an asteroid - game over
            print("Game over!")
            sys.exit() # Exit the program


def render_screen(screen, drawable_group):
    """
    Render all game objects to the screen.
    
    This function:
    - Clears the screen with the background color
    - Draws all sprites from the drawable group to the screen
    - Note: Does not call pygame.display.flip() or update() - this should be done elsewhere
    
    Args:
        screen (pygame.Surface): The main display surface to render onto
        drawable_group (pygame.sprite.Group): Group of all sprites that need to be drawn
    
    Returns:
        None: This function updates the screen surface in-place but doesn't return a value.
    """

    # Fill the enite screen with the background color (erasing previous frame)
    screen.fill(c.BACKGROUND_COLOR)

    # Draw each sprite in the drawable group to the screen
    for sprite in drawable_group:
        sprite.draw(screen)
    
    # Note: This function doesn't update the display - pygame.display.flip() 
    # or pygame.display.update() should be called after this function