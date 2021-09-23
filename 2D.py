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
RAYS_NUM = 10
STEP_ANGLE = FOV / RAYS_NUM
LOOK_SENSITIVITY = 0.1
PLAYER_MOVE_SPEED = 2

# Variables
player_x = WIDTH // 4   # In the middle of the 2D map
player_y = HEIGHT // 2
player_angle = math.pi

# Map
mMap = [
    '11111111',
    '1..1...1',
    '1..1...1',
    '1....111',
    '1......1',
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
pygame.display.set_caption("Raycasting")

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
                rect=(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE-1, TILE_SIZE-1)
            )

    # Draw player
    pygame.draw.circle(
        surface=window,
        color=(255, 50, 50),
        center=(player_x, player_y),
        radius=8
    )

# Raycasting algorithm
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
                        rect=(target_col * TILE_SIZE, target_row * TILE_SIZE, TILE_SIZE-2, TILE_SIZE-2)
                    )
                    # Break the loop so the ray doesnt go through walls
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


# Mainloop
while True:
    # Update background color
    window.fill((0, 0, 0))
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

    # Apply raycasting
    cast_rays()

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player_angle -= LOOK_SENSITIVITY
    elif keys[pygame.K_RIGHT]: player_angle += LOOK_SENSITIVITY

    if keys[pygame.K_w]:
        player_x += -math.sin(player_angle) * PLAYER_MOVE_SPEED
        player_y += math.cos(player_angle) * PLAYER_MOVE_SPEED
    elif keys[pygame.K_s]:
        player_x -= -math.sin(player_angle) * PLAYER_MOVE_SPEED
        player_y -= math.cos(player_angle) * PLAYER_MOVE_SPEED

    # Update display
    pygame.display.flip()

    # Set FPS
    clock.tick(60)
