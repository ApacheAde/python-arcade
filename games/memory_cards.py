#!/usr/bin/env python3
"""Memory Match — flip colourful cards to find pairs."""

import random
import pygame

W, H = 840, 640
COLS, ROWS = 4, 3
FACES = [
    ("♥", (220, 40, 70)),
    ("★", (240, 190, 30)),
    ("◆", (40, 120, 220)),
    ("●", (40, 180, 90)),
    ("▲", (200, 80, 220)),
    ("☀", (255, 140, 40)),
]


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Memory Match  ·  x.com/ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("verdana", 22, bold=True)
    huge = pygame.font.SysFont("segoeui symbol,dejavusans,georgia", 48, bold=True)
    small = pygame.font.SysFont("verdana", 16)

    deck = FACES + FACES
    random.shuffle(deck)
    margin_x, margin_y = 70, 100
    cw, ch, gap = 160, 140, 18
    cards = []
    for i, (glyph, colour) in enumerate(deck):
        r, c = divmod(i, COLS)
        rect = pygame.Rect(margin_x + c * (cw + gap), margin_y + r * (ch + gap), cw, ch)
        cards.append({"g": glyph, "c": colour, "rect": rect, "up": False, "done": False})

    opened = []
    lock_until = 0
    moves = 0
    won = False

    running = True
    while running:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                random.shuffle(deck)
                for i, card in enumerate(cards):
                    card["g"], card["c"] = deck[i]
                    card["up"] = card["done"] = False
                opened, moves, won = [], 0, False
                lock_until = 0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and now >= lock_until and not won:
                for idx, card in enumerate(cards):
                    if card["rect"].collidepoint(event.pos) and not card["up"] and not card["done"]:
                        card["up"] = True
                        opened.append(idx)
                        if len(opened) == 2:
                            moves += 1
                            a, b = cards[opened[0]], cards[opened[1]]
                            if a["g"] == b["g"]:
                                a["done"] = b["done"] = True
                                opened = []
                                if all(c["done"] for c in cards):
                                    won = True
                            else:
                                lock_until = now + 800
                        break

        if now >= lock_until and len(opened) == 2:
            for i in opened:
                cards[i]["up"] = False
            opened = []

        screen.fill((24, 18, 48))
        pygame.draw.rect(screen, (50, 30, 90), (0, 0, W, 70))
        screen.blit(font.render(f"MEMORY MATCH    moves {moves}", True, (255, 230, 120)), (24, 22))
        screen.blit(small.render("R restart   ·   x.com/ElbowOS", True, (210, 200, 255)), (560, 26))

        for card in cards:
            r = card["rect"]
            if card["up"] or card["done"]:
                pygame.draw.rect(screen, (250, 246, 235), r, border_radius=12)
                pygame.draw.rect(screen, card["c"], r, 5, border_radius=12)
                g = huge.render(card["g"], True, card["c"])
                screen.blit(g, g.get_rect(center=r.center))
            else:
                pygame.draw.rect(screen, (90, 50, 170), r, border_radius=12)
                pygame.draw.rect(screen, (180, 140, 255), r, 3, border_radius=12)
                pygame.draw.circle(screen, (160, 110, 230), r.center, 18)

        if won:
            banner = font.render("All pairs found — press R to shuffle again", True, (255, 255, 160))
            screen.blit(banner, banner.get_rect(center=(W // 2, H - 28)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
