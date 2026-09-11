#!/usr/bin/env python3
"""Lucky Reels — colourful three-reel slot machine."""

import random
import pygame

W, H = 780, 560
SYMBOLS = [
    ("7", (255, 60, 60), 20),
    ("★", (255, 210, 40), 12),
    ("♦", (80, 180, 255), 8),
    ("♪", (180, 90, 255), 6),
    ("BAR", (80, 255, 140), 5),
    ("●", (255, 120, 40), 3),
]
PAY = {
    ("7", "7", "7"): 50,
    ("★", "★", "★"): 25,
    ("♦", "♦", "♦"): 15,
    ("♪", "♪", "♪"): 10,
    ("BAR", "BAR", "BAR"): 8,
    ("●", "●", "●"): 4,
}


def pick():
    names = [s[0] for s in SYMBOLS]
    weights = [s[2] for s in SYMBOLS]
    return random.choices(names, weights=weights, k=1)[0]


def colour_of(name):
    for n, c, _w in SYMBOLS:
        if n == name:
            return c
    return (255, 255, 255)


def payout(reels, bet):
    key = tuple(reels)
    if key in PAY:
        return bet * PAY[key]
    if reels[0] == reels[1] or reels[1] == reels[2] or reels[0] == reels[2]:
        return bet * 2
    return 0


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Lucky Reels  ·  x.com/ElbowOS")
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("georgia", 40, bold=True)
    font = pygame.font.SysFont("verdana", 22, bold=True)
    huge = pygame.font.SysFont("segoeui symbol,dejavusans,georgia", 64, bold=True)
    small = pygame.font.SysFont("verdana", 16)

    bank = 200
    bet = 5
    reels = ["7", "★", "♦"]
    spinning = False
    ticks = 0
    stop_at = [0, 0, 0]
    message = "Pull the lever!"
    last_win = 0

    spin_btn = pygame.Rect(280, 460, 220, 56)
    minus = pygame.Rect(80, 470, 70, 40)
    plus = pygame.Rect(630, 470, 70, 40)

    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not spinning:
                if spin_btn.collidepoint(event.pos) and bank >= bet:
                    bank -= bet
                    spinning = True
                    ticks = 0
                    stop_at = [18 + random.randint(0, 8), 28 + random.randint(0, 8), 38 + random.randint(0, 8)]
                    message = "Spinning..."
                    last_win = 0
                elif minus.collidepoint(event.pos):
                    bet = max(1, bet - 1)
                elif plus.collidepoint(event.pos):
                    bet = min(25, bank, bet + 1)

        if spinning:
            ticks += 1
            for i, stop in enumerate(stop_at):
                if ticks < stop:
                    reels[i] = pick()
            if ticks >= max(stop_at):
                spinning = False
                last_win = payout(reels, bet)
                bank += last_win
                message = f"WIN ${last_win}!" if last_win else "No luck — try again"

        screen.fill((18, 8, 28))
        pygame.draw.rect(screen, (90, 20, 50), (0, 0, W, 80))
        t = title.render("LUCKY REELS", True, (255, 210, 70))
        screen.blit(t, t.get_rect(center=(W // 2, 40)))

        pygame.draw.rect(screen, (160, 30, 70), (70, 110, 640, 320), border_radius=18)
        pygame.draw.rect(screen, (40, 10, 20), (100, 140, 580, 250), border_radius=12)

        for i, sym in enumerate(reels):
            box = pygame.Rect(130 + i * 180, 165, 150, 200)
            pygame.draw.rect(screen, (250, 245, 230), box, border_radius=12)
            pygame.draw.rect(screen, (255, 200, 60), box, 4, border_radius=12)
            glyph = huge.render(sym, True, colour_of(sym))
            screen.blit(glyph, glyph.get_rect(center=box.center))

        hover = spin_btn.collidepoint(mouse) and not spinning
        pygame.draw.rect(screen, (220, 40, 70) if hover else (180, 20, 50), spin_btn, border_radius=12)
        screen.blit(font.render("SPIN", True, (255, 255, 255)), font.render("SPIN", True, (255, 255, 255)).get_rect(center=spin_btn.center))
        pygame.draw.rect(screen, (80, 80, 110), minus, border_radius=8)
        pygame.draw.rect(screen, (80, 80, 110), plus, border_radius=8)
        screen.blit(font.render("-", True, (255, 255, 255)), (105, 476))
        screen.blit(font.render("+", True, (255, 255, 255)), (654, 476))

        screen.blit(font.render(f"Bank ${bank}", True, (255, 220, 80)), (80, 430))
        screen.blit(font.render(f"Bet ${bet}", True, (255, 220, 80)), (620, 430))
        screen.blit(small.render(message, True, (255, 240, 200)), (280, 430))
        screen.blit(small.render("3 of a kind pays big  ·  any pair pays 2x  ·  x.com/ElbowOS", True, (200, 180, 220)), (140, 530))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
