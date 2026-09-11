#!/usr/bin/env python3
"""Prism Snake — neon classic."""

import random
import pygame

W, H = 720, 560
CELL = 20
COLS, ROWS = W // CELL, (H - 40) // CELL
PALETTE = [
    (80, 255, 180),
    (80, 200, 255),
    (180, 120, 255),
    (255, 90, 180),
    (255, 210, 70),
]


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Prism Snake  ·  x.com/ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("verdana", 20, bold=True)
    big = pygame.font.SysFont("georgia", 42, bold=True)

    def reset():
        body = [(COLS // 2, ROWS // 2 + i) for i in range(4)]
        return body, (0, -1), spawn(body), 0, False

    def spawn(body):
        while True:
            p = (random.randrange(COLS), random.randrange(ROWS))
            if p not in body:
                return p

    snake, direction, food, score, dead = reset()
    pending = direction
    tick = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                    pending = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                    pending = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                    pending = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    pending = (1, 0)
                elif event.key == pygame.K_r:
                    snake, direction, food, score, dead = reset()
                    pending = direction

        tick += 1
        speed = max(6, 12 - score // 5)
        if not dead and tick % speed == 0:
            direction = pending
            hx, hy = snake[0]
            nx, ny = hx + direction[0], hy + direction[1]
            if nx < 0 or ny < 0 or nx >= COLS or ny >= ROWS or (nx, ny) in snake:
                dead = True
            else:
                snake.insert(0, (nx, ny))
                if (nx, ny) == food:
                    score += 1
                    food = spawn(snake)
                else:
                    snake.pop()

        screen.fill((10, 12, 22))
        pygame.draw.rect(screen, (24, 20, 48), (0, 0, W, 40))
        screen.blit(font.render(f"PRISM SNAKE   score {score}", True, (180, 255, 220)), (12, 10))
        screen.blit(font.render("x.com/ElbowOS", True, (180, 160, 255)), (560, 10))

        for x in range(COLS):
            for y in range(ROWS):
                if (x + y) % 2 == 0:
                    pygame.draw.rect(screen, (16, 18, 30), (x * CELL, 40 + y * CELL, CELL, CELL))

        fx, fy = food
        pygame.draw.rect(screen, (255, 70, 90), (fx * CELL + 3, 40 + fy * CELL + 3, CELL - 6, CELL - 6), border_radius=4)

        for i, (x, y) in enumerate(snake):
            col = PALETTE[i % len(PALETTE)]
            pygame.draw.rect(screen, col, (x * CELL + 1, 40 + y * CELL + 1, CELL - 2, CELL - 2), border_radius=4)

        if dead:
            msg = big.render("CRASH — press R", True, (255, 90, 120))
            screen.blit(msg, msg.get_rect(center=(W // 2, H // 2)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
