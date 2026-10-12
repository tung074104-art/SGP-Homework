import pygame # import pygame for adding library help you yo make game
import random # random library help you to random number
import sys # sys library help you to control the app system(close game)


# 1-INIT the pygame
pygame.init()
# 2-Config about game window
WIDTH = 1000
HEIGHT = 600
# Create game window
mountain = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First parkour game")
clock = pygame.time.Clock()
FPS = 60
# 3 - Config color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (231, 76, 60)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
YELLOW = (241, 196, 15)
PURPLE = (155, 89, 182)
ORANGE = (230, 126, 34)
GRAY = (149, 165, 166)
SKY = (135, 206, 235)
DARK = (44, 62, 80)

# 4 - Config font text
font_big = pygame.font.SysFont("Arial",60,bold = True)
font_med = pygame.font.SysFont("Arial",30,bold = True)
font_small = pygame.font.SysFont("Arial",20)

# 5 - Classes
class Block():
    def __init__(self,x,y,w,h,color):
        self.rect = pygame.Rect(x,y,w,h)
        self.color = color

    def draw(self,window):
        pygame.draw.rect(window,self.color,self.rect)
block_list = [
    Block(100,540,175,20,GREEN),
    Block(250,500,175,20,GREEN),
    Block(400,460,175,20,GREEN),
    Block(550,420,175,20,GREEN)
]
# 6 - Game loop
game_run = True
while game_run:
    # Handle event when game run
    for event in pygame.event.get():
        # Event 1: Closing
        if event.type == pygame.QUIT:
            game_run = False
    for block in block_list:
        block.draw(mountain)
    pygame.display.update()
