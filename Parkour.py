import pygame # import pygame for adding library help you yo make game
import random # random library help you to random number
import sys # sys library help you to control the app system(close game)
import math

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
# 8 - Physic config
GRAVITY          =  0.8
JUMP_STRENGTH    =  -15
MOVE_SPEED       =  5
MAX_FALL_SPEED   =  18
# 6 - Classes
class Player():
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.rect = pygame.Rect(x,y,35,45)
        self.color = (255,0,0)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.alive = True
        self.jumps_left = 1
        self.max_jumps = 1
    def reset(self):
        self.rect_x = self.start_x
        self.rect_y = self.start_y
        self.vel_x = 0
        self.vel_y = 0
        self.alive = True
        self.jumps_left = self.max_jumps
    def draw(self, window, cam_x = 0):
        r = self.rect.copy()
        pygame.draw.rect(window,self.color,r)
    def jump(self):
        if self.jumps_left > 0 and self.alive:
            self.vel_y = JUMP_STRENGTH
            self.jumps_left -= 1
    def update(self, platforms, keys):
        if not self.alive:
            return
        self.vel_x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -5
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = 5
        self.rect.x += self.vel_x
        for i in platforms:
            if self.rect.colliderect(i):
                if self.vel_x > 0:
                    self.rect.right = i.rect.left
                if self.vel_x < 0:
                    self.rect.left = i.rect.right
        self.vel_y += GRAVITY
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED
        self.rect.y += self.vel_y
        self.on_ground = False
        for i in platforms:
            if self.rect.colliderect(i):
                if self.vel_y > 0:
                    self.rect.bottom = i.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.jumps_left = self.max_jumps
                elif self.vel_y < 0:
                    self.rect.top = i.rect.bottom
                    self.vel_y = 0
# 5 - Classes
class Block():
    def __init__(self,x,y,w,h,color):
        self.rect = pygame.Rect(x,y,w,h)
        self.color = color
    def draw(self,window):
        pygame.draw.rect(window,self.color,self.rect)
class MovingPlatform():
    def __init__(self,x,y,w,h,color, dx = 0, dy = 0, dist = 100): # dx: 1 -> right, -1 -> left, 0: not moving left or right
        # dy: 1 --> up -1 >> down 0 --> not moving up or down
        self.rect = pygame.Rect(x,y,w,h)
        self.color = color
        self.start_x = x
        self.start_y = y
        self.dx = dx
        self.dy = dy
        self.dist = dist
        self.t = 0
        self.speed = 0.02
    def update(self):
        self.t += self.speed
        offset = math.sin(self.t) * self.dist
        self.rect.x = self.start_x + self.dx * offset
        self.rect.y = self.start_y + self.dy * offset
    def draw(self, window, cam_x = 0):
        r = self.rect.copy()
        pygame.draw.rect(window, PURPLE, r, border_radius = 4)
        pygame.draw.rect(window, (200, 150, 230), r, 3, border_radius = 4)
class Level:
    def __init__(self, name, platforms, hazards, movers, spawn, goal, width):
        self.name = name
        self.platforms = platforms
        self.hazards = hazards
        self.movers = movers
        self.spawn = spawn
        self.goal = goal
        self.width = width
    def all_platforms(self):
        return [p.rect for p in self.platforms] + [m.rect for m in self.movers]
        pass
# level 1
def make_level_1():
    """Level 1: Cơ bản"""
    platforms = [
        Block(0, 550, 400, 50, GREEN),
        Block(480, 500, 120, 20, GREEN),
        Block(660, 450, 120, 20, GREEN),
        Block(840, 400, 120, 20, GREEN),
        Block(1020, 350, 120, 20, GREEN),
        Block(1200, 300, 200, 20, GREEN),
        Block(1450, 350, 120, 20, GREEN),
        Block(1620, 420, 200, 20, GREEN),
        Block(1880, 380, 300, 20, GREEN),
    ]
    movers = []
    spawn = (50, 480)
    goal = pygame.Rect(2050, 320, 50, 60)
    return Level("Level 1 - Start", platforms, hazards, movers, spawn, goal, 2200)
block_list = [
    Block(100,400,150,20,GREEN),
    Block(300,300,150,20,GREEN),
    Block(500,200,150,20,GREEN),
    Block(700,100,150,20,GREEN),
]
moving_list = [
    MovingPlatform(100, 500, 200, 20, PURPLE, dx = 1, dy = 0, dist = 200)
]
all_platform = block_list + moving_list
player_1 = Player(100,100)
# 7 - Game loop
game_run = True
while game_run:
    mountain.fill((BLACK))
    clock.tick(FPS)
    # Handle event when game run
    for event in pygame.event.get():
        # Event 1: Closing
        if event.type == pygame.QUIT:
            game_run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_run = False
            if event.key == pygame.K_SPACE:
                player_1.jump()
    keys = pygame.key.get_pressed()
    for block in all_platform:
        block.draw(mountain)
    for moving in moving_list:
        moving.draw(mountain)
        moving.update()
    player_1.draw(mountain)
    player_1.update(all_platform, keys)
    pygame.display.update()
