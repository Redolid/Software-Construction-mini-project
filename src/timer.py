"""Countdown timer logic for the Memory Scramble Game.

Responsibility:
- Track remaining seconds.
- Call a UI update function every second.
- Call a timeout function when time reaches zero.

Requirements covered in this file:
- player configures a timeout.
- countdown timer is shown while playing.
- game-over action happens when timer reaches zero.

Suggested teammate owner:
- feature/timer-config branch.
"""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable


class CountdownTimer:
    """Small wrapper around tkinter's after() scheduling."""

    def __init__(
        self,
        root: tk.Tk,
        seconds: int,
        on_tick: Callable[[int], None],
        on_finish: Callable[[], None],
    ) -> None:
        self.root = root
        self.remaining_seconds = seconds
        self.on_tick = on_tick
        self.on_finish = on_finish
        self._job_id: str | None = None
        self._running = False

    def start(self) -> None:
        """Start or restart the countdown."""
        self.stop()
        self._running = True
        self.on_tick(self.remaining_seconds)
        self._schedule_next_tick()

    def stop(self) -> None:
        """Cancel the timer if it is currently scheduled."""
        self._running = False
        if self._job_id is not None:
            self.root.after_cancel(self._job_id)
            self._job_id = None

    def _schedule_next_tick(self) -> None:
        if self._running:
            self._job_id = self.root.after(1000, self._tick)

    def _tick(self) -> None:
        if not self._running:
            return

        self.remaining_seconds -= 1
        self.on_tick(self.remaining_seconds)

        if self.remaining_seconds <= 0:
            self._running = False
            self._job_id = None
            self.on_finish()
            return

        self._schedule_next_tick()
