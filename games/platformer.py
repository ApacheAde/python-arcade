#!/usr/bin/env python3
"""Super Pixel Jump — original Mario-inspired platformer (not an emulator)."""

import pygame

W, H = 960, 540
GRAVITY = 0.55
JUMP = -12.5
SPEED = 5


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 28, 36)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.facing = 1
        self.alive = True

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -SPEED
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = SPEED
            self.facing = 1
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vy = JUMP
            self.on_ground = False

        self.vy += GRAVITY
        self.rect.x += int(self.vx)
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vx > 0:
                    self.rect.right = p.left
                elif self.vx < 0:
                    self.rect.left = p.right

        self.rect.y += int(self.vy)
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vy > 0:
                    self.rect.bottom = p.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = p.bottom
                    self.vy = 0

    def draw(self, surf, cam):
        r = self.rect.move(-cam, 0)
        body = pygame.Rect(r.x + 4, r.y + 10, 20, 22)
        pygame.draw.rect(surf, (220, 40, 40), body)
        pygame.draw.rect(surf, (40, 80, 200), (r.x + 4, r.y + 24, 20, 12))
        pygame.draw.ellipse(surf, (255, 210, 160), (r.x + 6, r.y, 16, 16))
        cap = pygame.Rect(r.x + 4, r.y - 4, 22, 8)
        pygame.draw.rect(surf, (220, 40, 40), cap)
        eye_x = r.x + (16 if self.facing > 0 else 8)
        pygame.draw.circle(surf, (20, 20, 20), (eye_x, r.y + 7), 2)


class Enemy:
    def __init__(self, x, y, left, right):
        self.rect = pygame.Rect(x, y, 28, 24)
        self.left = left
        self.right = right
        self.dir = 1

    def update(self):
        self.rect.x += self.dir * 2
        if self.rect.x <= self.left or self.rect.x >= self.right:
            self.dir *= -1

    def draw(self, surf, cam):
        r = self.rect.move(-cam, 0)
        pygame.draw.ellipse(surf, (150, 90, 40), r)
        pygame.draw.circle(surf, (20, 20, 20), (r.x + 8, r.y + 10), 3)
        pygame.draw.circle(surf, (20, 20, 20), (r.x + 20, r.y + 10), 3)


def make_world():
    platforms = [
        pygame.Rect(0, 500, 2200, 40),
        pygame.Rect(180, 420, 140, 20),
        pygame.Rect(380, 360, 120, 20),
        pygame.Rect(560, 300, 160, 20),
        pygame.Rect(800, 380, 140, 20),
        pygame.Rect(1000, 320, 180, 20),
        pygame.Rect(1240, 260, 140, 20),
        pygame.Rect(1460, 340, 200, 20),
        pygame.Rect(1720, 280, 160, 20),
        pygame.Rect(1920, 420, 180, 20),
    ]
    coins = [
        pygame.Rect(220, 380, 16, 16),
        pygame.Rect(420, 320, 16, 16),
        pygame.Rect(620, 260, 16, 16),
        pygame.Rect(840, 340, 16, 16),
        pygame.Rect(1080, 280, 16, 16),
        pygame.Rect(1280, 220, 16, 16),
        pygame.Rect(1540, 300, 16, 16),
        pygame.Rect(1780, 240, 16, 16),
    ]
    enemies = [
        Enemy(400, 476, 260, 520),
        Enemy(900, 356, 800, 920),
        Enemy(1500, 316, 1460, 1640),
    ]
    flag = pygame.Rect(2080, 360, 16, 140)
    return platforms, coins, enemies, flag


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Super Pixel Jump  ·  x.com/ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("verdana", 22, bold=True)
    big = pygame.font.SysFont("georgia", 48, bold=True)

    platforms, coins, enemies, flag = make_world()
    player = Player(40, 440)
    score = 0
    won = False
    lost = False
    cam = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                platforms, coins, enemies, flag = make_world()
                player = Player(40, 440)
                score = 0
                won = lost = False

        if player.alive and not won:
            player.update(platforms)
            for e in list(enemies):
                e.update()
                if player.rect.colliderect(e.rect):
                    if player.vy > 0 and player.rect.bottom - e.rect.top < 16:
                        enemies.remove(e)
                        player.vy = JUMP * 0.55
                        score += 50
                    else:
                        player.alive = False
                        lost = True
            for c in coins[:]:
                if player.rect.colliderect(c):
                    coins.remove(c)
                    score += 10
            if player.rect.colliderect(flag):
                won = True
            if player.rect.top > H + 80:
                player.alive = False
                lost = True

        cam = max(0, min(player.rect.centerx - W // 3, 2200 - W))

        screen.fill((92, 178, 255))
        pygame.draw.circle(screen, (255, 240, 120), (120, 80), 40)
        for i, cloud_x in enumerate((200, 480, 760)):
            cx = (cloud_x - cam * 0.3) % (W + 200) - 80
            pygame.draw.ellipse(screen, (255, 255, 255), (cx, 70 + i * 10, 90, 36))
            pygame.draw.ellipse(screen, (255, 255, 255), (cx + 30, 55 + i * 10, 70, 36))

        for hx in range(-50, 2300, 180):
            pygame.draw.ellipse(screen, (60, 170, 70), (hx - cam * 0.5, 430, 220, 140))

        for p in platforms:
            r = p.move(-cam, 0)
            pygame.draw.rect(screen, (70, 160, 50), r)
            pygame.draw.rect(screen, (120, 80, 40), (r.x, r.bottom - 8, r.w, 8))

        for c in coins:
            r = c.move(-cam, 0)
            pygame.draw.circle(screen, (255, 210, 40), r.center, 9)
            pygame.draw.circle(screen, (255, 250, 160), r.center, 4)

        for e in enemies:
            e.draw(screen, cam)

        fr = flag.move(-cam, 0)
        pygame.draw.rect(screen, (240, 240, 240), (fr.x + 6, fr.y, 6, fr.h))
        pygame.draw.polygon(screen, (40, 200, 70), [(fr.x + 12, fr.y), (fr.x + 70, fr.y + 18), (fr.x + 12, fr.y + 36)])

        player.draw(screen, cam)

        pygame.draw.rect(screen, (20, 20, 40), (0, 0, W, 36))
        screen.blit(font.render(f"COINS  {score}", True, (255, 220, 60)), (16, 6))
        screen.blit(font.render("Arrows/WASD  Space jump  R restart", True, (220, 220, 230)), (280, 6))
        screen.blit(font.render("x.com/ElbowOS", True, (180, 160, 255)), (780, 6))

        if won:
            msg = big.render("YOU WIN!", True, (255, 255, 80))
            screen.blit(msg, msg.get_rect(center=(W // 2, H // 2)))
        elif lost:
            msg = big.render("OUCH — press R", True, (255, 80, 80))
            screen.blit(msg, msg.get_rect(center=(W // 2, H // 2)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
