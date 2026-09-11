#!/usr/bin/env python3
"""Colourful game launcher for Python Arcade."""

import os
import subprocess
import sys

import pygame

ROOT = os.path.dirname(os.path.abspath(__file__))
GAMES = [
    ("Super Pixel Jump", "games/platformer.py", (70, 160, 255), "Mario-style platformer"),
    ("Neon Blackjack", "games/blackjack.py", (20, 120, 70), "Casino twenty-one"),
    ("Lucky Reels", "games/slots.py", (180, 40, 90), "Three-reel slots"),
    ("Memory Match", "games/memory_cards.py", (90, 60, 180), "Flip matching cards"),
    ("Velvet Roulette", "games/roulette.py", (140, 20, 40), "Spin the wheel"),
    ("Prism Snake", "games/snake.py", (20, 160, 120), "Eat, grow, don't crash"),
]


def main():
    pygame.init()
    screen = pygame.display.set_mode((820, 560))
    pygame.display.set_caption("Python Arcade  ·  x.com/ElbowOS")
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont("georgia", 42, bold=True)
    item_font = pygame.font.SysFont("verdana", 26, bold=True)
    hint_font = pygame.font.SysFont("verdana", 16)
    small = pygame.font.SysFont("verdana", 14)

    buttons = []
    for i, (name, path, colour, blurb) in enumerate(GAMES):
        rect = pygame.Rect(80, 110 + i * 65, 660, 56)
        buttons.append((rect, name, path, colour, blurb))

    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, _name, path, _c, _b in buttons:
                    if rect.collidepoint(event.pos):
                        full = os.path.join(ROOT, path)
                        subprocess.Popen([sys.executable, full], cwd=ROOT)

        screen.fill((18, 16, 28))
        pygame.draw.rect(screen, (40, 30, 70), (0, 0, 820, 90))
        title = title_font.render("PYTHON ARCADE", True, (255, 220, 80))
        screen.blit(title, (40, 22))
        screen.blit(small.render("x.com/ElbowOS", True, (200, 180, 255)), (640, 40))

        for rect, name, _p, colour, blurb in buttons:
            hover = rect.collidepoint(mouse)
            bg = tuple(min(255, c + 30) for c in colour) if hover else colour
            pygame.draw.rect(screen, bg, rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)
            screen.blit(item_font.render(name, True, (255, 255, 255)), (rect.x + 18, rect.y + 6))
            screen.blit(hint_font.render(blurb, True, (230, 230, 230)), (rect.x + 18, rect.y + 32))

        screen.blit(hint_font.render("Click a game to launch  ·  Esc to quit launcher", True, (160, 160, 180)), (80, 520))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
