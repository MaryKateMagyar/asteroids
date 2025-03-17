# player_module.py:
# This module handles the player's attributes and behaviors within the game, such as movement, drawing, and interactions.

# Third-Party Imports - External game libraries
import pygame

# Local Module Imports - Game-specific modules
import constants as c # Game constants and configurations, like colors, sizes, and player settings
import circleshape as cs # Base class for circular shapes, which the Player class extends


# Definition of the Player class, which inherits from the CircleShape class
class Player(cs.CircleShape):
    def __init__(self, x, y):
        # Initialize the player as a type of CircleShape at position (x, y) with a radius from constants
        super().__init__(x, y, c.PLAYER_RADIUS)

        # Player's rotation angle (direction), initialized to 0 degrees
        self.rotation = 0

        # Timer to control shooting rate, initialized to a cooldown value from constants
        self.shot_timer = c.PLAYER_SHOOT_COOLDOWN

    def triangle(self):
        """Calculate the three vertices of the player's triangular representation based on its position and rotation."""

        # Forward direction vector, rotated to match the player's current orientation
        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        # Right direction vector, scaled relative to the radius to form the triangle's base
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5

        # Vertex 'a': Tip of the triangle, extending forward from the player's position
        a = self.position + forward * self.radius
        # Vertex 'b': Bottom-left of the triangle, moving backward and offset by 'right' vector
        b = self.position - forward * self.radius - right
        # Vertex 'c': Bottom-right of the triangle, moving backward and offset by the inverse 'right' vector
        c = self.position - forward * self.radius + right

        # Return a list of the triangle's vertices
        return [a, b, c]

    def draw(self, screen):
        """Render the player's shape on the screen."""

        # Use pygame's draw.polygon function to draw the player as a triangle.
        # The triangle's vertices are calculated using the 'self.triangle()' method.
        # 'screen': The display surface on which to draw the player.
        # 'c.ASSET_COLOR': The color of the triangle, retrieved from the constants module.
        # 'self.triangle()': List of vertices defining the triangular shape of the player.
        # '2': The width (thickness) of the triangle outline.
        pygame.draw.polygon(screen, c.ASSET_COLOR, self.triangle(), 2)

    def rotate(self, dt):
        """Update the player's rotation angle over time."""

        # Increment the rotation angle based on the player's turning speed.
        # 'c.PLAYER_TURN_SPEED': The speed of the player's rotation, defined as a constant.
        # 'dt': Time delta (change in time since the last frame), used to make rotation smooth and frame-independent.
        self.rotation += (c.PLAYER_TURN_SPEED * dt)

    def update(self, dt):
        """Update the player's state every frame."""

        # Decrease the shot timer by the elapsed time ('dt'), enabling the cooldown for shooting.
        self.shot_timer -= dt

        # Get the key states to check which keys are currently being pressed.
        keys = pygame.key.get_pressed()

        # Rotate counterclockwise when the 'A' key is pressed
        if keys[pygame.K_a]:
            self.rotate(-dt)  # '-dt' ensures counterclockwise roration
        
        # Rotate clockwise when the 'D' key is pressed
        if keys[pygame.K_d]:
            self.rotate(dt)  # '+dt' ensures clockwise rotation
        
        # Move forward when the 'W' key is pressed
        if keys[pygame.K_w]:
            self.move(dt)  # Positive 'dt' moves the player forward
        
        # Move backward when the 'S' key is pressed
        if keys[pygame.K_s]:
            self.move(-dt)  # Negative 'dt' moves the player backward

    def move(self, dt):
        """Move the player in the direction it is facing."""

        # Calculate the forward direction vector based on the player's current rotation angle.
        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        # Update the player's position by adding the forward vector, scaled by speed and delta time.
        # 'c.PLAYER_SPEED': A constant determining the player's movement speed.
        # 'dt': Delta time for smooth and consistent movement.
        self.position += forward * c.PLAYER_SPEED * dt

    def shoot(self, shots_group):
        """Shoot a projectile if the player's shot timer has expired."""

        # Check if the shot timer is less than or equal to zero, meaning the cooldown period has ended,
        # and the player is allowed to fire a projectile.
        if self.shot_timer <= 0:
            # Create a new 'Shot' object at the player's current position.
            # 'self.position[0]' is the x-coordinate, and 'self.position[1]' is the y-coordinate of the player.
            # 'c.SHOT_RADIUS' is a constant that defines how large the shot (projectile) will be.
            shot = Shot(self.position[0], self.position[1], c.SHOT_RADIUS)

            # Set the velocity of the shot. 
            # The direction of the velocity is calculated based on the player's current rotation ('self.rotation').
            # 'pygame.Vector2(0, 1)' represents a default forward vector.
            # '.rotate(self.rotation)' rotates the vector to match the direction the player is facing.
            # The resulting vector is scaled by 'c.PLAYER_SHOOT_SPEED' (a constant defining the projectile speed).
            shot.velocity = (pygame.Vector2(0, 1).rotate(self.rotation)) * c.PLAYER_SHOOT_SPEED

            # Add the newly created 'Shot' object to the 'shots_group', 
            # which is a collection (group) that manages all active projectiles in the game.
            shots_group.add(shot)

            # Reset the 'shot_timer' by adding the cooldown time ('c.PLAYER_SHOOT_COOLDOWN'),
            # ensuring the player cannot shoot again until the timer runs down to zero.
            self.shot_timer += c.PLAYER_SHOOT_COOLDOWN


# Definition of the Shot class, which inherits from the CircleShape class
class Shot(cs.CircleShape):
    """
    Represents a projectile (shot) fired by the player.
    Inherits from 'cs.CircleShape'.
    """

    def __init__(self, x, y, radius):
        """
        Initialize a Shot object.
        """

        # Initialize the shot as a type of CircleShape at position (x, y) with a radius from constants
        super().__init__(x, y, radius)

    def draw(self, screen):
        """
        Render the shot on the screen.
        """

        # Use 'pygame.draw.circle' to visually represent the shot as a circle.
        # 'screen' is the display surface where the shot will be drawn.
        # 'c.ASSET_COLOR' is the color of the shot, defined as a constant.
        # 'self.position' refers to the (x, y) coordinates of the shot.
        # 'self.radius' is the size of the shot.
        # '2' specifies the width (outline thickness) of the circle.
        pygame.draw.circle(screen, c.ASSET_COLOR, self.position, self.radius, 2)

    def update(self, dt):
        """
        Update the state of the shot each frame.
        """

        # Update the position of the shot based on its velocity and the elapsed time ('dt').
        # 'self.velocity' determines the direction and speed of the shot.
        # Multiplying by 'dt' ensures smooth, frame-independent movement.
        self.position += self.velocity * dt