"""tkinter user interface and game flow for the Memory Scramble Game.

Responsibility:
- Display configuration inputs.
- Render the board as buttons.
- Handle card selection, matching, win, and loss states.
- Connect the board and timer modules to the visible game.

Requirements covered in this file:
- player can configure rows, columns, and timeout.
- player can select two face-down cells.
- matching cards stay face-up.
- non-matching cards flip back face-down.
- success and game-over messages are shown.
- player can see how many pair attempts they have made.

Suggested teammate owner:
- feature/ui branch for layout and controls.
- feature/game-logic branch for selection and matching behavior.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

try:
    from .board import generate_board, validate_board_size
    from .timer import CountdownTimer
except ImportError:
    from board import generate_board, validate_board_size
    from timer import CountdownTimer


CARD_BACK_TEXT = "?"
FLIP_BACK_DELAY_MS = 700
CARD_HIDDEN_BG = "#e8edf3"
CARD_FACE_UP_BG = "#fff5c4"
CARD_MATCHED_BG = "#c9f2d1"
CARD_DISABLED_BG = "#dddddd"


class MemoryScrambleGame:
    """Main application class for the GUI game."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Memory Scramble Game")
        self.root.geometry("1100x650")
        self.root.minsize(1100, 650)

        self.rows_val = 4
        self.columns_val = 4
        self.timeout_val = 60

        self.board: list[list[str]] = []
        self.buttons: list[list[tk.Button]] = []
        self.flipped_cards: list[tuple[int, int]] = []
        self.matched_cards: set[tuple[int, int]] = set()
        self.moves_count = 0
        self.waiting_to_hide_cards = False
        self.game_active = False
        self.timer: CountdownTimer | None = None
        self._flip_back_job: str | None = None

        self._build_layout()

    def _build_layout(self) -> None:
        config_frame = tk.Frame(self.root, padx=12, pady=10)
        config_frame.grid(row=0, column=0, sticky="ew")

        # Rows: [-] value [+]
        tk.Button(config_frame, text="Rows ▾", relief=tk.FLAT, bd=0,
                  font=("Arial", 11)).grid(row=0, column=0, padx=(0, 2))
        tk.Button(config_frame, text="−", font=("Arial", 14, "bold"), width=2,
                  command=lambda: self._adjust("rows", -1)).grid(row=0, column=1)
        self.rows_btn = tk.Button(config_frame, text="4", font=("Arial", 14, "bold"),
                                   width=3, relief=tk.GROOVE)
        self.rows_btn.grid(row=0, column=2)
        tk.Button(config_frame, text="+", font=("Arial", 14, "bold"), width=2,
                  command=lambda: self._adjust("rows", 1)).grid(row=0, column=3)

        # Columns: [-] value [+]
        tk.Button(config_frame, text="Cols ▾", relief=tk.FLAT, bd=0,
                  font=("Arial", 11)).grid(row=0, column=4, padx=(16, 2))
        tk.Button(config_frame, text="−", font=("Arial", 14, "bold"), width=2,
                  command=lambda: self._adjust("cols", -1)).grid(row=0, column=5)
        self.cols_btn = tk.Button(config_frame, text="4", font=("Arial", 14, "bold"),
                                   width=3, relief=tk.GROOVE)
        self.cols_btn.grid(row=0, column=6)
        tk.Button(config_frame, text="+", font=("Arial", 14, "bold"), width=2,
                  command=lambda: self._adjust("cols", 1)).grid(row=0, column=7)

        # Timeout: [-] value [+]
        tk.Button(config_frame, text="Time ▾", relief=tk.FLAT, bd=0,
                  font=("Arial", 11)).grid(row=0, column=8, padx=(16, 2))
        tk.Button(config_frame, text="−", font=("Arial", 14, "bold"), width=2,
                  command=lambda: self._adjust("time", -10)).grid(row=0, column=9)
        self.time_btn = tk.Button(config_frame, text="60", font=("Arial", 14, "bold"),
                                   width=3, relief=tk.GROOVE)
        self.time_btn.grid(row=0, column=10)
        tk.Button(config_frame, text="+", font=("Arial", 14, "bold"), width=2,
                  command=lambda: self._adjust("time", 10)).grid(row=0, column=11)

        tk.Button(config_frame, text="Start Game", font=("Arial", 14, "bold"),
                  command=self.start_game).grid(row=0, column=12, padx=(20, 0))

        info_frame = tk.Frame(self.root, padx=12)
        info_frame.grid(row=1, column=0, sticky="ew")

        self.timer_btn = tk.Button(info_frame, text="Time: --", relief=tk.FLAT, bd=0, font=("Arial", 12, "bold"))
        self.timer_btn.grid(row=0, column=0, sticky="w")

        self.moves_btn = tk.Button(info_frame, text="Moves: 0", relief=tk.FLAT, bd=0, font=("Arial", 12, "bold"))
        self.moves_btn.grid(row=0, column=1, padx=12)

        self.status_btn = tk.Button(info_frame, text="Press Start Game to begin.", relief=tk.FLAT, bd=0)
        self.status_btn.grid(row=0, column=2, padx=16)

        self.board_frame = tk.Frame(self.root, padx=12, pady=12)
        self.board_frame.grid(row=2, column=0)

    def _adjust(self, field: str, delta: int) -> None:
        if field == "rows":
            self.rows_val = max(1, min(10, self.rows_val + delta))
            self.rows_btn.config(text=str(self.rows_val))
        elif field == "cols":
            self.columns_val = max(1, min(10, self.columns_val + delta))
            self.cols_btn.config(text=str(self.columns_val))
        elif field == "time":
            self.timeout_val = max(10, min(600, self.timeout_val + delta))
            self.time_btn.config(text=str(self.timeout_val))

    def start_game(self) -> None:
        """Create a new board and start the countdown."""
        rows = self.rows_val
        columns = self.columns_val
        timeout = self.timeout_val

        try:
            validate_board_size(rows, columns)
        except ValueError as error:
            messagebox.showerror("Invalid Configuration", str(error))
            return

        # Stop any previous timer and cancel pending after callbacks
        if self.timer is not None:
            self.timer.stop()
            self.timer = None
        if self._flip_back_job is not None:
            self.root.after_cancel(self._flip_back_job)
            self._flip_back_job = None
        self.game_active = False
        self.waiting_to_hide_cards = False


        # Reset game state
        self.board = generate_board(rows, columns)
        self.flipped_cards = []
        self.matched_cards = set()
        self.moves_count = 0
        self._update_moves_label()
        self.game_active = True

        self.timer = CountdownTimer(
            root=self.root,
            seconds=timeout,
            on_tick=self._update_timer_label,
            on_finish=self._handle_timeout,
        )

        self._render_board(rows, columns)
        self.status_btn.config(text="Find all matching pairs.")
        self.timer.start()

    def _render_board(self, rows: int, columns: int) -> None:
        # First: hide ALL existing buttons from the grid
        for button_row in self.buttons:
            for button in button_row:
                button.grid_forget()

        old_rows = len(self.buttons)
        old_cols = len(self.buttons[0]) if old_rows > 0 else 0

        # Grow rows if needed
        while len(self.buttons) < rows:
            self.buttons.append([])

        # For each row, grow columns if needed
        for row in range(rows):
            while len(self.buttons[row]) < columns:
                button = tk.Button(
                    self.board_frame,
                    text=CARD_BACK_TEXT,
                    width=6,
                    height=3,
                    font=("Arial", 16, "bold"),
                    bg=CARD_HIDDEN_BG,
                    activebackground=CARD_HIDDEN_BG,
                    disabledforeground="black",
                    command=lambda r=row, c=column: self.select_card(r, c),
                )
                self.buttons[row].append(button)

        # Now configure and grid only the buttons we need
        for row in range(rows):
            for col in range(columns):
                self.buttons[row][col].config(
                    text=CARD_BACK_TEXT,
                    state=tk.NORMAL,
                    relief=tk.RAISED,
                    command=lambda r=row, c=col: self.select_card(r, c),
                )
                self.buttons[row][col].grid(row=row, column=col, padx=4, pady=4)

        # Store current active size so select_card works correctly
        self._active_rows = rows
        self._active_cols = columns

    def select_card(self, row: int, column: int) -> None:
        """Flip a selected card and check for a pair after two selections."""
        position = (row, column)

        if not self.game_active:
            return
        if self.waiting_to_hide_cards:
            return
        if position in self.matched_cards or position in self.flipped_cards:
            return

        self._show_card(row, column)
        self.flipped_cards.append(position)

        if len(self.flipped_cards) == 2:
            self.moves_count += 1
            self._update_moves_label()
            self._check_selected_pair()

    def _check_selected_pair(self) -> None:
        first_row, first_column = self.flipped_cards[0]
        second_row, second_column = self.flipped_cards[1]

        first_symbol = self.board[first_row][first_column]
        second_symbol = self.board[second_row][second_column]

        if first_symbol == second_symbol:
            self.matched_cards.update(self.flipped_cards)
            self._mark_matched_cards()
            self.flipped_cards = []
            self.status_btn.config(text="Match found.")
            self._check_for_win()
            return

        self.status_btn.config(text="No match. Try again.")
        self.waiting_to_hide_cards = True
        self._flip_back_job = self.root.after(FLIP_BACK_DELAY_MS, self._hide_unmatched_cards)

    def _check_for_win(self) -> None:
        total_cards = len(self.board) * len(self.board[0])
        if len(self.matched_cards) == total_cards:
            self.game_active = False
            if self.timer is not None:
                self.timer.stop()
            self.status_btn.config(text="You matched all pairs.")
            messagebox.showinfo(
                "You Win",
                f"Congratulations! You matched all pairs in {self.moves_count} moves.",
            )

    def _hide_unmatched_cards(self) -> None:
        self._flip_back_job = None
        for row, column in self.flipped_cards:
            self._hide_card(row, column)

        self.flipped_cards = []
        self.waiting_to_hide_cards = False

    def _show_card(self, row: int, column: int) -> None:
        self.buttons[row][column].config(
            text=self.board[row][column],
            state=tk.DISABLED,
            relief=tk.SUNKEN,
            bg=CARD_FACE_UP_BG,
            activebackground=CARD_FACE_UP_BG,
        )

    def _hide_card(self, row: int, column: int) -> None:
        self.buttons[row][column].config(
            text=CARD_BACK_TEXT,
            state=tk.NORMAL,
            relief=tk.RAISED,
            bg=CARD_HIDDEN_BG,
            activebackground=CARD_HIDDEN_BG,
        )

    def _mark_matched_cards(self) -> None:
        for row, column in self.flipped_cards:
            self.buttons[row][column].config(
                state=tk.DISABLED,
                relief=tk.SUNKEN,
                bg=CARD_MATCHED_BG,
                activebackground=CARD_MATCHED_BG,
            )

    def _update_timer_label(self, remaining_seconds: int) -> None:
        self.timer_btn.config(text=f"Time: {remaining_seconds}")

    def _update_moves_label(self) -> None:
        self.moves_btn.config(text=f"Moves: {self.moves_count}")
        self.root.title(f"Memory Scramble Game  |  Moves: {self.moves_count}")

    def _handle_timeout(self) -> None:
        if not self.game_active:
            return

        self.game_active = False
        self.status_btn.config(text="Time is up.")
        self._disable_all_cards()
        messagebox.showinfo("Game Over", "Time is up. Better luck next round.")

    def _disable_all_cards(self) -> None:
        for row in self.buttons:
            for button in row:
                if button["text"] == CARD_BACK_TEXT:
                    button.config(bg=CARD_DISABLED_BG, activebackground=CARD_DISABLED_BG)
                button.config(state=tk.DISABLED)
