import pygame
import input_util
from player import Player

WIDTH = input_util.get_int("how many tiles wide: ")
HEIGHT = input_util.get_int("how many tiles tall: ")

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

TARGET_FPS = 60

####################
### PYGAME STUFF ###
####################

# initialize pygame
pygame.init()
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
# create a window
screen = pygame.display.set_mode(screen_size)
screen_rect = screen.get_rect()
pygame.display.set_caption("pygame Test")
# clock is used to set a max fps
clock = pygame.time.Clock()

##########################
### CHECKERBOARD STUFF ###
##########################

# determine the largest scale that still fits on the screen
SCALE = min((SCREEN_WIDTH / WIDTH), (SCREEN_HEIGHT / HEIGHT))

# create the surface that will be used for the checkerboard
surface_size = [WIDTH * SCALE, HEIGHT * SCALE]
# background shall be black (by default)
board_surface = pygame.Surface(surface_size)
board_surface_rect = board_surface.get_rect(center=screen_rect.center)

# add white squares to form the checkerboard
for tile in range(WIDTH * HEIGHT):
    x = tile % WIDTH
    y = tile // WIDTH
    # draw every other square (where x + y is even)
    if (x + y) % 2 == 0:
        pygame.draw.rect(board_surface, WHITE, [x * SCALE, y * SCALE, SCALE, SCALE])

####################
### PLAYER STUFF ###
####################
player = Player(WIDTH, HEIGHT)
# create surface the size of a tile, for the player graphics
player_surface = pygame.Surface([SCALE, SCALE])
# black will not get painted (treated like clear)
player_surface.set_colorkey(BLACK)
# the player is a red circle, add it to the player surface
pygame.draw.circle(player_surface, RED, player_surface.get_rect().center, SCALE / 2)


running = True
frame_time = 1000 // TARGET_FPS
while running:
    # handle inputs / events
    for event in pygame.event.get():
        player.handle_input(event)
        # exit the game loop on quit
        if event.type == pygame.QUIT:
            running = False
    
    player.update(frame_time)

    # clear the screen
    screen.fill(BLACK)

    # draw board to the screen
    screen.blit(board_surface, board_surface_rect)

    # add player to the screen, relative to the top left of the board
    screen.blit(player_surface, [board_surface_rect.left + player.x * SCALE, board_surface_rect.top + player.y * SCALE])

    # flip() updates the screen to make our changes visible
    pygame.display.flip()

    # how many updates per second
    frame_time = clock.tick(TARGET_FPS)
pygame.quit()
