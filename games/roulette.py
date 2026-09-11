#!/usr/bin/env python3
"""Velvet Roulette — European wheel with colourful betting spots."""

import math
import random
import pygame

W, H = 960, 640
WHEEL = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,
         5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
RED = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}


def colour(n):
    if n == 0:
        return (20, 140, 60)
    return (200, 30, 40) if n in RED else (20, 20, 24)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Velvet Roulette  ·  x.com/ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("verdana", 18, bold=True)
    small = pygame.font.SysFont("verdana", 14)
    title = pygame.font.SysFont("georgia", 32, bold=True)

    bank = 300
    bet_amt = 10
    chip_on = None
    angle = 0.0
    spin_vel = 0.0
    spinning = False
    result = None
    message = "Click a bet, then SPIN"

    cells = {}
    x0, y0 = 430, 90
    cells[("num", 0)] = pygame.Rect(x0, y0, 54, 48)
    for n in range(1, 37):
        row = (n - 1) // 3
        col = (n - 1) % 3
        cells[("num", n)] = pygame.Rect(x0 + col * 54, y0 + 52 + row * 36, 52, 34)
    extras = {
        ("red",): pygame.Rect(x0 + 170, y0 + 52, 90, 70),
        ("black",): pygame.Rect(x0 + 170, y0 + 130, 90, 70),
        ("even",): pygame.Rect(x0 + 170, y0 + 210, 90, 70),
        ("odd",): pygame.Rect(x0 + 170, y0 + 290, 90, 70),
    }
    cells.update(extras)
    spin_btn = pygame.Rect(x0 + 170, y0 + 380, 90, 50)
    minus = pygame.Rect(40, 560, 60, 36)
    plus = pygame.Rect(110, 560, 60, 36)

    def settle(n):
        nonlocal bank, message
        if chip_on is None:
            message = f"Landed on {n}"
            return
        kind = chip_on[0]
        win = 0
        if kind == "num" and chip_on[1] == n:
            win = bet_amt * 36
        elif kind == "red" and n in RED:
            win = bet_amt * 2
        elif kind == "black" and n != 0 and n not in RED:
            win = bet_amt * 2
        elif kind == "even" and n != 0 and n % 2 == 0:
            win = bet_amt * 2
        elif kind == "odd" and n % 2 == 1:
            win = bet_amt * 2
        if win:
            bank += win
            message = f"{n} — you win ${win}"
        else:
            bank -= bet_amt
            message = f"{n} — lost ${bet_amt}"

    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if minus.collidepoint(event.pos):
                    bet_amt = max(5, bet_amt - 5)
                elif plus.collidepoint(event.pos):
                    bet_amt = min(50, bet_amt + 5)
                elif spin_btn.collidepoint(event.pos) and not spinning and bank >= bet_amt:
                    spinning = True
                    result = None
                    spin_vel = 18 + random.random() * 10
                    message = "Wheel is spinning..."
                elif not spinning:
                    for key, rect in cells.items():
                        if rect.collidepoint(event.pos):
                            chip_on = key

        if spinning:
            angle = (angle + spin_vel) % 360
            spin_vel *= 0.985
            if spin_vel < 0.15:
                spinning = False
                idx = int(((-angle) % 360) / (360 / 37)) % 37
                result = WHEEL[idx]
                settle(result)

        screen.fill((28, 8, 14))
        pygame.draw.rect(screen, (80, 16, 28), (0, 0, W, 64))
        screen.blit(title.render("VELVET ROULETTE", True, (255, 210, 120)), (20, 14))
        screen.blit(small.render("x.com/ElbowOS", True, (230, 200, 160)), (800, 24))

        cx, cy, rad = 210, 300, 160
        pygame.draw.circle(screen, (180, 150, 60), (cx, cy), rad + 10)
        step = 360 / 37
        for i, n in enumerate(WHEEL):
            a0 = math.radians(-90 + angle + i * step)
            a1 = math.radians(-90 + angle + (i + 1) * step)
            pts = [(cx, cy)]
            for k in range(6):
                t = a0 + (a1 - a0) * k / 5
                pts.append((cx + rad * math.cos(t), cy + rad * math.sin(t)))
            pygame.draw.polygon(screen, colour(n), pts)
        pygame.draw.circle(screen, (40, 20, 10), (cx, cy), 28)
        pygame.draw.polygon(screen, (255, 220, 80), [(cx - 8, cy - rad - 18), (cx + 8, cy - rad - 18), (cx, cy - rad + 4)])

        pygame.draw.rect(screen, (16, 90, 50), (x0 - 12, y0 - 12, 290, 460), border_radius=8)
        for key, rect in cells.items():
            if key[0] == "num":
                pygame.draw.rect(screen, colour(key[1]), rect)
                label = str(key[1])
                colr = (255, 255, 255)
            else:
                names = {"red": ("RED", (180, 30, 40)), "black": ("BLK", (20, 20, 20)),
                         "even": ("EVEN", (40, 80, 40)), "odd": ("ODD", (40, 80, 40))}
                label, fill = names[key[0]]
                pygame.draw.rect(screen, fill, rect)
                colr = (255, 255, 255)
            pygame.draw.rect(screen, (230, 210, 140), rect, 1)
            t = small.render(label, True, colr)
            screen.blit(t, t.get_rect(center=rect.center))
            if chip_on == key:
                pygame.draw.circle(screen, (255, 220, 60), rect.center, 10)
                pygame.draw.circle(screen, (180, 40, 40), rect.center, 7)

        hover = spin_btn.collidepoint(mouse)
        pygame.draw.rect(screen, (200, 50, 50) if hover else (140, 20, 30), spin_btn, border_radius=8)
        screen.blit(font.render("SPIN", True, (255, 255, 255)), font.render("SPIN", True, (255, 255, 255)).get_rect(center=spin_btn.center))

        pygame.draw.rect(screen, (70, 70, 90), minus, border_radius=6)
        pygame.draw.rect(screen, (70, 70, 90), plus, border_radius=6)
        screen.blit(font.render("-", True, (255, 255, 255)), (62, 566))
        screen.blit(font.render("+", True, (255, 255, 255)), (132, 566))
        screen.blit(font.render(f"Bank ${bank}   Bet ${bet_amt}", True, (255, 220, 100)), (190, 566))
        screen.blit(font.render(message, True, (255, 240, 180)), (500, 566))
        if result is not None:
            screen.blit(title.render(str(result), True, colour(result)), (180, 500))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
