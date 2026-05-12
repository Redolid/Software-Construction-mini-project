"""Board generation for the Memory Scramble Game.

Responsibility:
- Validate board dimensions.
- Create pairs of symbols.
- Shuffle symbols into a two-dimensional board.

Requirements covered in this file:
- nRows * nColumns must be divisible by 2.
- board_size / 2 different icons are generated.
- each icon appears exactly twice.
- cards are randomly distributed.

Suggested teammate owner:
- feature/game-logic branch.
"""

from __future__ import annotations

import random


DEFAULT_SYMBOLS = [
    "★",
    "●",
    "■",
    "▲",
    "◆",
    "♥",
    "☀",
    "☂",
    "☕",
    "♫",
    "⚑",
    "✿",
    "☘",
    "✈",
    "☾",
    "♣",
    "♠",
    "♦",
    "☁",
    "☻",
    "✦",
    "✚",
    "⌂",
    "☞",
    "☯",
    "⚙",
    "⚡",
    "✉",
    "✓",
    "∞",
]


def validate_board_size(rows: int, columns: int) -> None:
    """Raise ValueError if the requested board size is not playable."""
    if rows <= 0 or columns <= 0:
        raise ValueError("Rows and columns must be positive numbers.")

    if rows * columns < 2:
        raise ValueError("Board must contain at least two cards.")

    if (rows * columns) % 2 != 0:
        raise ValueError("Rows multiplied by columns must be an even number.")

    if (rows * columns) // 2 > len(DEFAULT_SYMBOLS):
        raise ValueError(
            f"This version supports up to {len(DEFAULT_SYMBOLS) * 2} cards."
        )


def generate_board(rows: int, columns: int) -> list[list[str]]:
    """Create a shuffled board containing exactly two of each symbol."""
    validate_board_size(rows, columns)

    pairs_needed = (rows * columns) // 2
    selected_symbols = DEFAULT_SYMBOLS[:pairs_needed]
    cards = selected_symbols * 2
    random.shuffle(cards)

    board: list[list[str]] = []
    for row_index in range(rows):
        start = row_index * columns
        end = start + columns
        board.append(cards[start:end])

    return board
