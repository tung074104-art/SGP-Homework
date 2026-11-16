import pygame
import random
import sys
import math
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Obby Game")
clock = pygame.time.Clock()
FPS = 60
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (231, 76, 60)
GREEN  = (46, 204, 113)
BLUE   = (52, 152, 219)
YELLOW = (241, 196, 15)
PURPLE = (155, 89, 182)
ORANGE = (230, 126, 34)
DARK   = (44, 62, 80)
SKY    = (135, 206, 235)
GRAVITY        = 0.8
JUMP_STRENGTH  = -15
MOVE_SPEED     = 5
MAX_FALL_SPEED = 18

# ========================= CLASSES =========================
class Player:
    def __init__(self, x, y):
        self.start_x, self.start_y = x, y
        self.rect = pygame.Rect(x, y, 35, 45)
        self.prev_rect = self.rect.copy()
        self.vel_x = self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.alive = True
        self.jumps_left = 2
        self.max_jumps = 2
        self.standing_on = None

    def reset(self):
        self.rect.x, self.rect.y = self.start_x, self.start_y
        self.prev_rect = self.rect.copy()
        self.vel_x = self.vel_y = 0
        self.alive = True
        self.on_ground = False
        self.jumps_left = self.max_jumps
        self.standing_on = None

    def jump(self):
        if self.jumps_left > 0 and self.alive:
            self.vel_y = JUMP_STRENGTH
            self.jumps_left -= 1
            self.standing_on = None

    def update(self, platforms, hazards, keys, movers):
        if not self.alive:
            return

        # 1) Carry theo moving platform TRƯỚC
        if self.standing_on is not None:
            m = self.standing_on
            self.rect.x += m.rect.x - m.prev_x
            self.rect.y += m.rect.y - m.prev_y

        # 2) Snapshot vị trí SAU carry, TRƯỚC khi di chuyển
        self.prev_rect = self.rect.copy()

        # 3) Input ngang
        self.vel_x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -MOVE_SPEED
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = MOVE_SPEED
            self.facing_right = True

        # ===== VERTICAL PHASE FIRST =====
        self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL_SPEED)
        self.rect.y += self.vel_y
        self.on_ground = False
        self.standing_on = None

        for p in platforms:
            if self.rect.colliderect(p):
                came_from_above = self.prev_rect.bottom <= p.top + 2
                came_from_below = self.prev_rect.top >= p.bottom - 2

                if came_from_above and self.vel_y >= 0:
                    self.rect.bottom = p.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.jumps_left = self.max_jumps
                    for m in movers:
                        if p is m.rect:
                            self.standing_on = m
                            break
                elif came_from_below:
                    self.rect.top = p.bottom
                    self.vel_y = 0
                else:
                    # Fallback: dùng velocity để quyết định hướng đẩy
                    if self.vel_y < 0:
                        self.rect.top = p.bottom
                    else:
                        self.rect.bottom = p.top
                        self.on_ground = True
                        self.jumps_left = self.max_jumps
                        for m in movers:
                            if p is m.rect:
                                self.standing_on = m
                                break
                    self.vel_y = 0

        # ===== HORIZONTAL PHASE SECOND =====
        self.rect.x += self.vel_x
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vel_x > 0:
                    self.rect.right = p.left
                elif self.vel_x < 0:
                    self.rect.left = p.right

        if self.rect.top > HEIGHT + 200:
            self.alive = False
        for h in hazards:
            if self.rect.colliderect(h):
                self.alive = False

    def draw(self, surf, cam_x):
        r = self.rect.copy(); r.x -= cam_x
        pygame.draw.rect(surf, BLUE, r, border_radius=6)
        pygame.draw.rect(surf, DARK, r, 2, border_radius=6)
        ex = r.right - 12 if self.facing_right else r.x + 6
        pygame.draw.circle(surf, WHITE, (ex, r.y + 14), 6)
        pygame.draw.circle(surf, BLACK, (ex, r.y + 14), 3)


class Block:
    def __init__(self, x, y, w, h, color=GREEN):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
    def draw(self, surf, cam_x):
        r = self.rect.copy(); r.x -= cam_x
        pygame.draw.rect(surf, self.color, r, border_radius=4)
        pygame.draw.rect(surf, (30, 130, 70), r, 3, border_radius=4)


class MovingPlatform:
    def __init__(self, x, y, w, h, dx=0, dy=0, dist=100):
        self.rect = pygame.Rect(x, y, w, h)
        self.start_x, self.start_y = x, y
        self.dx, self.dy, self.dist = dx, dy, dist
        self.t = 0
        self.speed = 0.02
        self.prev_x, self.prev_y = x, y

    def update(self):
        self.prev_x, self.prev_y = self.rect.x, self.rect.y
        self.t += self.speed
        o = math.sin(self.t) * self.dist
        self.rect.x = self.start_x + self.dx * o
        self.rect.y = self.start_y + self.dy * o

    def draw(self, surf, cam_x):
        r = self.rect.copy(); r.x -= cam_x
        pygame.draw.rect(surf, PURPLE, r, border_radius=4)
        pygame.draw.rect(surf, (200, 150, 230), r, 3, border_radius=4)


class Level:
    def __init__(self, platforms, hazards, movers, spawn, goal, width):
        self.platforms = platforms
        self.hazards = hazards
        self.movers = movers
        self.spawn = spawn
        self.goal = goal
        self.width = width
    def all_platforms(self):
        return [p.rect for p in self.platforms] + [m.rect for m in self.movers]

# ========================= LEVELS =========================
def make_level_5():
    platforms = [
            Block(0,    550, 400, 50),
            Block(480,  500, 120, 20),
            Block(660,  450, 120, 20),
            Block(840,  400, 120, 20),
            Block(1620, 420, 200, 20),
            Block(1880, 380, 300, 20),
        ]
    movers = [
                MovingPlatform(1200, 300, 100, 20, dx=1, dy=0, dist=120),
            ]
    hazards = [pygame.Rect(400, 580, 1480, 20)]
    return Level(platforms, hazards, movers, (50, 480), pygame.Rect(2050, 320, 50, 60), 2200)

def make_level_2():
    platforms = [
        Block(0,    550, 350, 50),
        Block(450,  500, 100, 20),
        Block(700,  450, 100, 20),
        Block(2100, 450, 150, 20),
        Block(2350, 400, 300, 20),
    ]
    hazards = [
        pygame.Rect(350, 580, 2000, 20),
        pygame.Rect(1200, 520, 60, 60),
        pygame.Rect(1270, 520, 60, 60),
    ]
    movers = [
        MovingPlatform(1150, 350, 100, 20, dx=1, dy=0, dist=120),
        MovingPlatform(1600, 300, 100, 20, dx=0, dy=1, dist=80),
    ]
    return Level(platforms, hazards, movers, (50, 480), pygame.Rect(2500, 320, 50, 60), 2700)

def make_level_3():
    platforms = [
        Block(0,    550, 300, 50),
        Block(500,  500, 80, 20),
        Block(2500, 400, 100, 20),
        Block(2800, 350, 400, 20),
    ]
    hazards = [
        pygame.Rect(300, 580, 2500, 20),
        pygame.Rect(1400, 520, 80, 60),
        pygame.Rect(1500, 520, 80, 60),
        pygame.Rect(2300, 520, 80, 60),
    ]
    movers = [
        MovingPlatform(950,  300, 90, 20, dx=1, dy=0, dist=120),
        MovingPlatform(1250, 350, 90, 20, dx=0, dy=1, dist=100),
        MovingPlatform(1750, 250, 90, 20, dx=1, dy=0, dist=120),
        MovingPlatform(2050, 300, 90, 20, dx=0, dy=1, dist=80),
    ]
    return Level(platforms, hazards, movers, (50, 480), pygame.Rect(3050, 270, 50, 60), 3250)

def make_level_4():
    platforms = [
        Block(0, 550, 200, 50),
        Block(350, 480, 80, 20),
        Block(550, 380, 80, 20),
        Block(750, 280, 80, 20),
        Block(1000, 250, 60, 20),
        Block(1400, 320, 60, 20),
        Block(1800, 420, 80, 20),
        Block(2800, 350, 400, 20),
    ]
    hazards = [
        pygame.Rect(200, 580, 3000, 20),
        pygame.Rect(900, 200, 40, 380),
        pygame.Rect(1600, 200, 40, 250),
        pygame.Rect(2600, 450, 60, 130),
    ]
    movers = [
        MovingPlatform(1150, 200, 80, 20, dx=0, dy=2, dist=200),
        MovingPlatform(1900, 300, 70, 20, dx=2, dy=0, dist=150),
        MovingPlatform(2500, 380, 80, 20, dx=1, dy=0, dist=100),
    ]
    return Level(platforms, hazards, movers, (50, 480), pygame.Rect(3100, 270, 50, 60), 3250)
def make_level_1():
    platforms = [
        Block(0, 550, 200, 50),
        Block(1000, 250, 60, 20),
        Block(1400, 320, 60, 20),
        Block(2800, 350, 400, 20),
    ]
    hazards = [
        pygame.Rect(200, 580, 3000, 20),
        pygame.Rect(2600, 450, 60, 130),
    ]
    movers = [
        MovingPlatform(850, 450, 80, 20, dx=2, dy=0, dist=190),
        MovingPlatform(1150, 200, 80, 20, dx=0, dy=2, dist=200),
        MovingPlatform(1150, 200, 80, 20, dx=0, dy=2, dist=200),
        MovingPlatform(1800, 420, 80, 20, dx=2, dy=1, dist=90),
        MovingPlatform(2500, 380, 80, 20, dx=1, dy=0, dist=200),
    ]
    return Level(platforms, hazards, movers, (50, 480), pygame.Rect(3100, 270, 50, 60), 3250)
LEVELS = [make_level_1(), make_level_2(), make_level_3(), make_level_4(), make_level_5()]

# ========================= MAIN LOOP =========================
def main():
    idx = 0
    level = LEVELS[idx]
    player = Player(*level.spawn)
    cam_x = 0.0
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_r:
                    player.reset()

        keys = pygame.key.get_pressed()

        # Update movers TRƯỚC (để có prev_x, prev_y cho carry)
        for m in level.movers:
            m.update()

        # Update player
        player.update(level.all_platforms(), level.hazards, keys, level.movers)

        if not player.alive:
            player.reset()

        if player.rect.colliderect(level.goal):
            idx = (idx + 1) % len(LEVELS)
            level = LEVELS[idx]
            player = Player(*level.spawn)

        # Camera
        target = player.rect.centerx - WIDTH // 2
        target = max(0, min(target, level.width - WIDTH))
        cam_x += (target - cam_x) * 0.12

        # ============ DRAW ============
        screen.fill(SKY)
        for p in level.platforms: p.draw(screen, cam_x)
        for m in level.movers:    m.draw(screen, cam_x)
        for h in level.hazards:
            r = h.copy(); r.x -= cam_x
            pygame.draw.rect(screen, RED, r)
            for i in range(0, r.width, 20):
                pygame.draw.polygon(screen, ORANGE, [
                    (r.x + i, r.top),
                    (r.x + i + 10, r.top - 12),
                    (r.x + i + 20, r.top),
                ])
        g = level.goal.copy(); g.x -= cam_x
        pygame.draw.rect(screen, YELLOW, g, border_radius=6)
        pygame.draw.rect(screen, (200, 150, 0), g, 4, border_radius=6)
        player.draw(screen, cam_x)
        pygame.display.update()

if __name__ == "__main__":
    main()
