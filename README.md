# Python Arcade

A collection of **simple, full-colour Python 3 games** built with [pygame](https://www.pygame.org/).

Follow updates: **[x.com/ElbowOS](https://x.com/ElbowOS)**

GitHub: [github.com/ApacheAde/python-arcade](https://github.com/ApacheAde/python-arcade)

## Games

| Game | File | What it is |
|------|------|------------|
| Super Pixel Jump | `games/platformer.py` | Side-scrolling platformer (Mario-style jump, coins, goombas, flag) |
| Neon Blackjack | `games/blackjack.py` | Casino blackjack with colourful cards and chip betting |
| Lucky Reels | `games/slots.py` | Three-reel slot machine with animated spin |
| Memory Match | `games/memory_cards.py` | Flip-and-match card game |
| Velvet Roulette | `games/roulette.py` | European roulette table + spinning wheel |
| Prism Snake | `games/snake.py` | Classic snake with a neon palette |

These are original mini-games, **not** console emulators or ROM players. A real Mario Bros emulator would need a full NES CPU/PPU core and copyrighted ROMs — this repo stays original and legal.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 launcher.py
```

Or run one game directly:

```bash
python3 games/platformer.py
```

## Controls

Most games use **arrow keys / WASD**, **Space**, and **mouse clicks** on on-screen buttons. Each window also shows its own hint bar.

## Licence

MIT. Have fun.

— linked from [x.com/ElbowOS](https://x.com/ElbowOS)
