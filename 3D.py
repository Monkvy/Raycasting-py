import pygame
import sys
import math

# Constants
WIDTH = 960
HEIGHT = 480
MAX_FPS = 60
MAP_SIZE = 8
TILE_SIZE = int((WIDTH / 2) / MAP_SIZE)
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
RAYS_NUM = 30
STEP_ANGLE = FOV / RAYS_NUM
SCALE = int(WIDTH / 2 / RAYS_NUM)
LOOK_SENSITIVITY = 0.1
PLAYER_MOVE_SPEED = 2

# Variables
player_x = WIDTH // 4  # In the middle of the 2D map
player_y = HEIGHT // 2
player_angle = math.pi
player_walkForward = True
fps = 0

# Map
mMap = [
    '11111111',
    '1..1...1',
    '1......1',
    '111..111',
    '111....1',
    '1...1..1',
    '1...1..1',
    '11111111'
]
if (len(mMap) != MAP_SIZE) | (len(mMap[0]) != MAP_SIZE):
    print("Map size does not equal the MAP_SIZE variable.")
    sys.exit()

# Initialize pygame
pygame.init()

# Create game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ray casting")

# Init timer
clock = pygame.time.Clock()


# Draw map
def drawMap():
    # Loop over map rows
    for row in range(MAP_SIZE):
        # Loop over map cols
        for col in range(MAP_SIZE):
            # Draw map in the game window
            pygame.draw.rect(
                surface=window,
                color=(200, 200, 200) if mMap[row][col] == '1' else (100, 100, 100),
                rect=(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1)
            )

    # Draw player
    pygame.draw.circle(
        surface=window,
        color=(255, 50, 50),
        center=(player_x, player_y),
        radius=8
    )


# Ray casting algorithm
def cast_rays():
    # Define  left most angle of FOV
    start_angle = player_angle - HALF_FOV

    # Loop over rays
    for ray in range(RAYS_NUM):
        # Cast ray step by step
        for depth in range(MAX_DEPTH):
            # Get ray end coord
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth

            # Convert coords to rows and cols
            target_row = int(target_y / TILE_SIZE)
            target_col = int(target_x / TILE_SIZE)

            # Check if the end point of the ray is not outside the map
            if (target_row < MAP_SIZE) & (target_col < MAP_SIZE):
                # Get the target piece
                target_piece = mMap[target_row][target_col]
                # Check if the piece is a wall (index of 1)
                if target_piece == '1':
                    # Draw a green rect on top of the target piece
                    pygame.draw.rect(
                        surface=window,
                        color=(50, 255, 50),
                        rect=(target_col * TILE_SIZE, target_row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                    )

                    # Wall shading
                    c = int(255 / (1 + depth * depth * 0.0001))

                    # Disable fish eye effect
                    depth *= math.cos(player_angle - start_angle)

                    # Calculate wall height (add 0.0001 to avoid division by zero error)
                    wall_height = 21000 / (depth + 0.0001)

                    # Set max wall height
                    if wall_height > WIDTH: wall_height = WIDTH

                    # Draw 3D projection
                    half_width = int(WIDTH / 2)
                    half_height = int(HEIGHT / 2)
                    pygame.draw.rect(
                        surface=window,
                        color=(c, c, c),
                        rect=(half_width + int(ray * SCALE), half_height - int(wall_height / 2),
                              SCALE, int(wall_height))
                    )

                    # Break the loop so the ray doesn't go through walls
                    break

            # Draw ray
            pygame.draw.line(
                surface=window,
                color=(50, 255, 50),
                start_pos=(player_x, player_y),
                end_pos=(target_x, target_y),
                width=3
            )

        # Increment angle by a single step
        start_angle += STEP_ANGLE


# Player collision
def isCollidingWalls():
    # Convert player position to col and row
    player_row = int(player_y / TILE_SIZE)
    player_col = int(player_x / TILE_SIZE)

    # Check if the player point of the ray is not outside the map
    if (player_row < MAP_SIZE) & (player_col < MAP_SIZE):
        # Get the target piece
        player_piece = mMap[player_row][player_col]
        # Check if the player is inside wall
        if player_piece == '1':
            return True
        else:
            return False


# Mainloop
while True:
    # Update background color
    window.fill((0, 0, 0))
    pygame.draw.rect(window, (100, 100, 100), (WIDTH // 2, HEIGHT // 2, WIDTH // 2, HEIGHT))
    pygame.draw.rect(window, (200, 200, 200), (WIDTH // 2, -HEIGHT // 2, WIDTH // 2, HEIGHT))

    # Collision detection
    if isCollidingWalls():
        if player_walkForward:
            player_x -= -math.sin(player_angle) * PLAYER_MOVE_SPEED
            player_y -= math.cos(player_angle) * PLAYER_MOVE_SPEED
        else:
            player_x += -math.sin(player_angle) * PLAYER_MOVE_SPEED
            player_y += math.cos(player_angle) * PLAYER_MOVE_SPEED

    # Escape condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Draw 2D Map
    drawMap()

    # Apply ray casting
    cast_rays()

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle -= LOOK_SENSITIVITY
    elif keys[pygame.K_RIGHT]:
        player_angle += LOOK_SENSITIVITY

    if keys[pygame.K_w]:
        player_x += -math.sin(player_angle) * PLAYER_MOVE_SPEED
        player_y += math.cos(player_angle) * PLAYER_MOVE_SPEED
        player_walkForward = True
    elif keys[pygame.K_s]:
        player_x -= -math.sin(player_angle) * PLAYER_MOVE_SPEED
        player_y -= math.cos(player_angle) * PLAYER_MOVE_SPEED
        player_walkForward = False

    # Set FPS
    clock.tick(60)

    # Get FPS & display it as window title
    fps = int(clock.get_fps())
    pygame.display.set_caption(f"Running at {str(fps)} frames per second")

    # Update display
    pygame.display.flip()
