import pygame
import math
import sys

# Constants
MAP_SIZE = 10
TILE_SIZE = 60
WIDTH = MAP_SIZE * TILE_SIZE
HEIGHT = MAP_SIZE * TILE_SIZE
SOURCE_MOVE_SPEED = 0.4
MAX_DEPTH = 800

# Variables
source_x = WIDTH // 2
source_y = HEIGHT // 2

target_x = WIDTH // 2
target_y = HEIGHT // 4
line_enabled = False
mouseCell = (0, 0)

# Map
map = []
for i in range(MAP_SIZE):
    row = []
    for j in range(MAP_SIZE):
        row.append(0)
    map.append(row)


# Init pygame
pygame.init()

# Create window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raycasting")


# Draw map
def drawMap():
    for r in range(MAP_SIZE):
        for c in range(MAP_SIZE):
            tile = map[r][c]
            if tile == 0:
                pygame.draw.rect(
                    surface=window,
                    color=(0, 0, 0),
                    rect=(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE-1, TILE_SIZE-1)
                )
            elif tile == 1:
                pygame.draw.rect(
                    surface=window,
                    color=(0, 0, 255),
                    rect=(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE-1, TILE_SIZE-1)
                )

    if line_enabled:
        pygame.draw.line(
            surface=window,
            color=(255, 255, 255),
            start_pos=(source_x, source_y),
            end_pos=(target_x, target_y),
            width=3
        )

    pygame.draw.circle(
        surface=window,
        color=(255, 0, 0),
        center=(source_x, source_y),
        radius=7
    )
    pygame.draw.circle(
        surface=window,
        color=(0, 255, 0),
        center=(target_x, target_y),
        radius=7
    )

def castRay():
    start_angle = math.atan2(target_y - source_y, target_x - source_x) - math.pi/2
    max_depth = math.sqrt((target_x-source_x)**2 + (source_y - target_y)**2)

    # Cast ray step by step
    for depth in range(int(max_depth)):
        # Get ray end coord
        target_pos_x = source_x - math.sin(start_angle) * depth
        target_pos_y = source_y + math.cos(start_angle) * depth

        # Convert coords to rows and cols
        target_row = int(target_pos_y / TILE_SIZE)
        target_col = int(target_pos_x / TILE_SIZE)

        # Check if the end point of the ray is not outside the map
        if (target_row < MAP_SIZE) & (target_col < MAP_SIZE):
            # Get the target piece
            target_piece = map[target_row][target_col]
            # Check if the piece is a wall (index of 1)
            if target_piece == 1:
                # Draw point
                pygame.draw.circle(
                    surface=window,
                    color=(50, 255, 50),
                    center=(target_pos_x, target_pos_y),
                    radius=7
                )
                # Break the loop so the ray doesnt go through walls
                break


# Mainloop
while True:
    # Background
    window.fill((255, 255, 255))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_buttons = pygame.mouse.get_pressed(num_buttons=3)
            if mouse_buttons[0]:
                line_enabled = not line_enabled

    drawMap()

    # Movement
    keys = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed(num_buttons=3)
    mouse_pos = pygame.mouse.get_pos()
    mouseCell = (int(mouse_pos[0] / TILE_SIZE), int(mouse_pos[1] / TILE_SIZE))

    if keys[pygame.K_w]: source_y -= SOURCE_MOVE_SPEED
    if keys[pygame.K_s]: source_y += SOURCE_MOVE_SPEED

    if keys[pygame.K_a]: source_x -= SOURCE_MOVE_SPEED
    if keys[pygame.K_d]: source_x += SOURCE_MOVE_SPEED
    target_x, target_y = mouse_pos

    if mouse_buttons[2]: map[mouseCell[1]][mouseCell[0]] = 1

    if line_enabled: castRay()

    # Update screen
    pygame.display.flip()