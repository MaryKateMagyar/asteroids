# asteroid_module.py: 
# This module handles the creation, behavior, and management of asteroids in the game.
# It defines both individual asteroid objects and the asteroid field that spawns them.

# Standard Library Imports 
import random

# Third-Party Imports - External game libraries
import pygame

# Local Module Imports - Game-specific modules
import constants as c # Game constants and configurations
import circleshape as cs # Circle-related class


class Asteroid(cs.CircleShape):
    """
    Represents an asteroid in the game that can move, be drawn, and split when destroyed.
    
    Asteroid objects inherit from CircleShape and have additional functionality
    for drawing themselves and splitting into smaller asteroids when hit.
    
    Attributes:
        Inherits all attributes from CircleShape including:
        - position (pygame.Vector2): Current position of the asteroid
        - velocity (pygame.Vector2): Current velocity vector
        - radius (float): Radius of the asteroid (determines its size)
    """

    def __init__(self, x, y, radius):
        """
        Initialize a new asteroid.
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
            radius (float): Radius of the asteroid
        """

        # Use the __init__ variables from CircleShape class
        super().__init__(x, y, radius) 

    def draw(self, screen):
        """
        Draw the asteroid on the screen as a white circle outline.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        pygame.draw.circle(screen, (c.BACKGROUND_COLOR), self.position, self.radius, 2)

    def update(self, dt):
        """
        Update the asteroid's position based on its velocity and time elapsed.
        
        Args:
            dt (float): Delta time - seconds elapsed since last frame
        """

        self.position += self.velocity * dt

    def split(self):
        """
        Split the asteroid into two smaller asteroids when destroyed.
    
        This method:
        1. Destroys the current asteroid
        2. If the asteroid is large enough (larger than minimum radius), creates two smaller 
           asteroids that move in diverging directions at higher speeds
        3. Small asteroids (at minimum radius) are simply destroyed without creating new ones
    
        The new asteroids:
        - Have a radius equal to (old_radius - ASTEROID_MIN_RADIUS)
        - Are positioned exactly where the original asteroid was
        - Move in directions that are randomly angled from the original trajectory
        - Move 20% faster than the original asteroid
        """
        
        # Generate a random angle between 20 - 50 degress for the split
        random_angle = random.uniform(20, 50)

        # Create two new velocity vectors by rotating the original velocity
        # in opposite directions by the random angle
        split_vector1 = self.velocity.rotate(random_angle)     # Rotate clockwise
        split_vector2 = self.velocity.rotate(-random_angle)    # Rotate counter-clockwise

        # Calculate the size of the new smaller asteroids
        new_radius = self.radius - c.ASTEROID_MIN_RADIUS

        # Destroy the original asteroid
        self.kill()

        # If this was already a minimal-sized asteroid, don't create new ones
        if self.radius <= c.ASTEROID_MIN_RADIUS:
            return

        # Create first new asteroid at the same position as the original
        new_asteroid1 = Asteroid(self.position[0], self.position[1], new_radius)
        # Set velocity: same direction as split_vector but 20$ faster
        new_asteroid1.velocity = split_vector1 * 1.2

        # Create second new asteroid at the same position as the original
        new_asteroid2 = Asteroid(self.position[0], self.position[1], new_radius) 
        # Set veolicty: same direction as split_vector2 but 20% faster
        new_asteroid2.velocity = split_vector2 * 1.2     


class AsteroidField(pygame.sprite.Sprite):
    """
    Manages the creation and spawning of asteroids in the game.
    
    This class handles periodic spawning of new asteroids from the edges
    of the screen, controlling their initial position, size, and velocity.
    It inherits from pygame.sprite.Sprite to integrate with the game's
    sprite management system.
    """

    # Define the four edges of the screen where asteroids can spawn
    # Each edge is defined by:
    # 1. A direction vector pointing inward from that edge
    # 2. A function that generates a position along that edge given a 0-1 parameter
    edges = [
        # Right edge (asteroids move right-to-left)
        [
            pygame.Vector2(1, 0), # Direction: rightward
            lambda y: pygame.Vector2(-c.ASTEROID_MAX_RADIUS, y * c.SCREEN_HEIGHT),
        ],
        # Left edge (asteroids move left-to-right)
        [
            pygame.Vector2(-1, 0), # Direction: leftward
            lambda y: pygame.Vector2(
                c.SCREEN_WIDTH + c.ASTEROID_MAX_RADIUS, y * c.SCREEN_HEIGHT
            ),
        ],
        # Bottom edge (asteroids move bottom-to-top)
        [
            pygame.Vector2(0, 1), # Direction: upward
            lambda x: pygame.Vector2(x * c.SCREEN_WIDTH, -c.ASTEROID_MAX_RADIUS),
        ],
        # Top edge (asteroids move top-to-bottom)
        [
            pygame.Vector2(0, -1), # Direction: downward
            lambda x: pygame.Vector2(
                x * c.SCREEN_WIDTH, c.SCREEN_HEIGHT + c.ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        """
        Initialize the AsteroidField manager.
    
        Initializes the sprite and sets up a timer to track when new
        asteroids should be spawned.
        """

        pygame.sprite.Sprite.__init__(self, self.containers) # Initialize as a sprite in the game containers
        self.spawn_timer = 0.0 # Timer to track when to spawn new asteroids

    def spawn(self, radius, position, velocity):
        """
        Create a new asteroid with the specified properties.
    
        Args:
            radius (float): Radius of the new asteroid
            position (pygame.Vector2): Initial position of the asteroid
            velocity (pygame.Vector2): Initial velocity vector of the asteroid
    
        Returns:
            Asteroid: The newly created asteroid object
    
        Note: The asteroid is automatically added to sprite groups through the 
        Asteroid class constructor.
        """

        asteroid = Asteroid(position.x, position.y, radius) # Create a new asteroid
        asteroid.velocity = velocity # Set its velocity
        # Note: The asteroid is automatically added to the game's asteroid container

    def update(self, dt):
        """
        Update the asteroid field state and potentially spawn new asteroids.
    
        This method is called once per frame to manage the spawning of new asteroids
        based on elapsed time and configured spawn rate.
    
        Args:
            dt (float): Delta time - seconds elapsed since last frame
        """

        # Add elpsed time to the spawn timer
        self.spawn_timer += dt

        # Check if it's time to spawn a new asteroid
        if self.spawn_timer > c.ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0 # Reset the timer

            # Select a random edge (contains direction vector and position function)
            edge = random.choice(self.edges)

            # Generate a random speed between 40 - 100 pixels per second
            speed = random.randint(40, 100)

            # Create a velocity using the edge's direction and random speed
            velocity = edge[0] * speed

            # Add some randomness to the direction by rotating -30 to +30 degrees
            velocity = velocity.rotate(random.randint(-30, 30))

            # Generate a position alone the chosen edge (parameter between 0-1)
            # edge[1] is a function that maps a 0-1 value to a position on that edge
            position = edge[1](random.uniform(0, 1))

            # Determine the asteroid size (small, medium, large)
            # This picks a random integer between 1 and ASTEROID_KINDS (typically 3)
            kind = random.randint(1, c.ASTEROID_KINDS)

            # Spawn the asteroid with calculated properties:
            # - Radius is the minimum radius multiplied by the kind (1, 2, or 3)
            # - Position is the generated point on the edge
            # - Velocity is the calculated direction and speed
            self.spawn(c.ASTEROID_MIN_RADIUS * kind, position, velocity)