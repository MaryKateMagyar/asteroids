# --- Screen Settings ---
SCREEN_WIDTH = 1280 # Width of the game window, in pixels
SCREEN_HEIGHT = 720 # Height of the game window, in pixels

# --- Asteroid Settings ---
ASTEROID_MIN_RADIUS = 20 # Minimum radius of an asteroid, in pixels
ASTEROID_KINDS = 3 # Number of distinct asteroid sizes (e.g. small, medium, large)
ASTEROID_SPAWN_RATE = 0.8  # Time between asteroid spawns, in seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS # Maximum asteroid radius, based on size levels

# --- Player Settings ---
PLAYER_RADIUS = 20 # Radius of the player's character, in pixels
PLAYER_TURN_SPEED = 300 # Player's turn peed, in degrees per second
PLAYER_SPEED = 200 # Player's movement speed, in pixels per second

# --- Shot Settings ---
SHOT_RADIUS = 5 # Radius of a player's shot (bullet), in pixels
PLAYER_SHOOT_SPEED = 500 # Speed of a player's shot, in pixels per second
PLAYER_SHOOT_COOLDOWN = 0.3 # Time between player's shots, in seconds

# --- Game Logic ---
FRAME_RATE = 60 # Used for consistent game speed across hardware, in frames per second

# --- Visual Settings ---
BACKGROUND_COLOR = (0, 0, 0) # RGB color for the background (black)
ASSET_COLOR = (255, 255, 255) # RGB color for game assets, e.g. player, asteroids, and bullets (white)