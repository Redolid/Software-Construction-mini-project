"""Application entry point for the Memory Scramble Game.

Responsibility:
- Create the tkinter root window.
- Start the GUI event loop.

Requirements covered in this file:
- run the complete game from one beginner-friendly command.

Suggested teammate owner:
- main branch maintainer or integration owner.
"""

from __future__ import annotations

import tkinter as tk

try:
    from .game import MemoryScrambleGame
except ImportError:
    from game import MemoryScrambleGame


def main() -> None:
    """Start the Memory Scramble Game."""
    root = tk.Tk()
    MemoryScrambleGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
