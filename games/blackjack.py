#!/usr/bin/env python3
"""Neon Blackjack — colourful casino twenty-one."""

import random
import pygame

W, H = 900, 620
SUITS = [("♥", (220, 30, 50)), ("♦", (220, 30, 50)), ("♠", (20, 20, 30)), ("♣", (20, 20, 30))]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def new_deck():
    deck = [(r, s, c) for r in RANKS for s, c in SUITS]
    random.shuffle(deck)
    return deck


def value(hand):
    total = 0
    aces = 0
    for r, _s, _c in hand:
        if r == "A":
            aces += 1
            total += 11
        elif r in "JQK":
            total += 10
        else:
            total += int(r)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def draw_card(surf, x, y, card, hidden=False):
    rect = pygame.Rect(x, y, 86, 124)
    pygame.draw.rect(surf, (30, 30, 40), rect.inflate(6, 6), border_radius=8)
    if hidden:
        pygame.draw.rect(surf, (80, 20, 90), rect, border_radius=8)
        pygame.draw.rect(surf, (180, 80, 200), rect.inflate(-16, -16), 3, border_radius=6)
        return
    pygame.draw.rect(surf, (250, 248, 240), rect, border_radius=8)
    rank, suit, colour = card
    font = pygame.font.SysFont("georgia", 22, bold=True)
    big = pygame.font.SysFont("segoeui symbol,dejavusans,georgia", 36, bold=True)
    surf.blit(font.render(rank, True, colour), (x + 8, y + 6))
    surf.blit(big.render(suit, True, colour), (x + 28, y + 44))
    surf.blit(font.render(rank, True, colour), (x + 52, y + 96))


class Button:
    def __init__(self, rect, label, colour):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.colour = colour

    def draw(self, surf, font, hover):
        c = tuple(min(255, v + 25) for v in self.colour) if hover else self.colour
        pygame.draw.rect(surf, c, self.rect, border_radius=10)
        pygame.draw.rect(surf, (255, 255, 255), self.rect, 2, border_radius=10)
        t = font.render(self.label, True, (255, 255, 255))
        surf.blit(t, t.get_rect(center=self.rect.center))

    def hit(self, pos):
        return self.rect.collidepoint(pos)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Blackjack  ·  x.com/ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("verdana", 22, bold=True)
    small = pygame.font.SysFont("verdana", 16)
    big = pygame.font.SysFont("georgia", 40, bold=True)

    bank = 500
    bet = 25
    deck = new_deck()
    player, dealer = [], []
    phase = "bet"
    message = "Place a bet"

    buttons = [
        Button((40, 540, 110, 48), "HIT", (30, 140, 80)),
        Button((160, 540, 110, 48), "STAND", (30, 90, 160)),
        Button((280, 540, 110, 48), "DEAL", (160, 110, 20)),
        Button((400, 540, 70, 48), "-BET", (90, 90, 110)),
        Button((480, 540, 70, 48), "+BET", (90, 90, 110)),
        Button((560, 540, 110, 48), "AGAIN", (120, 50, 140)),
    ]

    def deal():
        nonlocal deck, player, dealer, phase, message, bank, bet
        if bank < bet:
            message = "Not enough chips"
            return
        if len(deck) < 10:
            deck = new_deck()
        bank -= bet
        player = [deck.pop(), deck.pop()]
        dealer = [deck.pop(), deck.pop()]
        phase = "play"
        message = "Hit or Stand"
        if value(player) == 21:
            finish()

    def finish():
        nonlocal phase, message, bank
        phase = "done"
        while value(dealer) < 17:
            dealer.append(deck.pop())
        pv, dv = value(player), value(dealer)
        if pv > 21:
            message = "Bust — dealer wins"
        elif dv > 21 or pv > dv:
            win = bet * 2
            if pv == 21 and len(player) == 2:
                win = int(bet * 2.5)
                message = "Blackjack!"
            else:
                message = "You win!"
            bank += win
        elif pv == dv:
            bank += bet
            message = "Push"
        else:
            message = "Dealer wins"

    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if buttons[0].hit(event.pos) and phase == "play":
                    player.append(deck.pop())
                    if value(player) >= 21:
                        finish()
                elif buttons[1].hit(event.pos) and phase == "play":
                    finish()
                elif buttons[2].hit(event.pos) and phase == "bet":
                    deal()
                elif buttons[3].hit(event.pos) and phase == "bet":
                    bet = max(5, bet - 25)
                elif buttons[4].hit(event.pos) and phase == "bet":
                    bet = min(bank, bet + 25)
                elif buttons[5].hit(event.pos) and phase == "done":
                    player, dealer = [], []
                    phase = "bet"
                    message = "Place a bet"

        screen.fill((8, 70, 42))
        pygame.draw.ellipse(screen, (12, 100, 58), (40, 40, 820, 470))
        pygame.draw.ellipse(screen, (180, 150, 50), (40, 40, 820, 470), 6)

        screen.blit(font.render("DEALER", True, (230, 220, 140)), (70, 60))
        screen.blit(font.render("YOU", True, (230, 220, 140)), (70, 300))

        hide = phase == "play"
        for i, card in enumerate(dealer):
            draw_card(screen, 70 + i * 100, 100, card, hidden=(hide and i == 1))
        for i, card in enumerate(player):
            draw_card(screen, 70 + i * 100, 340, card)

        if player:
            shown_d = value(dealer[:1]) if hide else value(dealer)
            screen.blit(small.render(f"Dealer: {shown_d if not hide else str(shown_d)+'+?'}", True, (255, 255, 255)), (70, 236))
            screen.blit(small.render(f"You: {value(player)}", True, (255, 255, 255)), (70, 476))

        pygame.draw.rect(screen, (20, 30, 20), (0, 520, W, 100))
        for b in buttons:
            b.draw(screen, font, b.rect.collidepoint(mouse))

        screen.blit(font.render(f"Bank ${bank}   Bet ${bet}", True, (255, 220, 80)), (690, 548))
        banner = big.render(message, True, (255, 240, 160))
        screen.blit(banner, (430, 70))
        screen.blit(small.render("x.com/ElbowOS", True, (200, 230, 180)), (760, 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
