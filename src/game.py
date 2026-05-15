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
        self.root.resizable(False, False)

        self.rows_var = tk.StringVar(value="4")
        self.columns_var = tk.StringVar(value="4")
        self.timeout_var = tk.StringVar(value="60")
        self.status_var = tk.StringVar(value="Configure the game and press Start.")
        self.timer_var = tk.StringVar(value="Time: 60")

        self.board: list[list[str]] = []
        self.buttons: list[list[tk.Button]] = []
        self.flipped_cards: list[tuple[int, int]] = []
        self.matched_cards: set[tuple[int, int]] = set()
        self.waiting_to_hide_cards = False
        self.game_active = False
        self.timer: CountdownTimer | None = None

        self._build_layout()

    def _build_layout(self) -> None:
        config_frame = tk.Frame(self.root, padx=12, pady=10)
        config_frame.grid(row=0, column=0, sticky="ew")

        tk.Label(config_frame, text="Rows").grid(row=0, column=0, padx=4)
        tk.Entry(config_frame, textvariable=self.rows_var, width=5).grid(
            row=0, column=1, padx=4
        )

        tk.Label(config_frame, text="Columns").grid(row=0, column=2, padx=4)
        tk.Entry(config_frame, textvariable=self.columns_var, width=5).grid(
            row=0, column=3, padx=4
        )

        tk.Label(config_frame, text="Timeout").grid(row=0, column=4, padx=4)
        tk.Entry(config_frame, textvariable=self.timeout_var, width=6).grid(
            row=0, column=5, padx=4
        )

        tk.Button(config_frame, text="Start Game", command=self.start_game).grid(
            row=0, column=6, padx=8
        )

        info_frame = tk.Frame(self.root, padx=12)
        info_frame.grid(row=1, column=0, sticky="ew")

        tk.Label(info_frame, textvariable=self.timer_var, font=("Arial", 12, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        tk.Label(info_frame, textvariable=self.status_var).grid(row=0, column=1, padx=16)

        self.board_frame = tk.Frame(self.root, padx=12, pady=12)
        self.board_frame.grid(row=2, column=0)

    def start_game(self) -> None:
        """Read settings, create a new board, and start the countdown."""
        try:
            rows = int(self.rows_var.get())
            columns = int(self.columns_var.get())
            timeout = int(self.timeout_var.get())
            validate_board_size(rows, columns)
            if timeout <= 0:
                raise ValueError("Timeout must be a positive number of seconds.")
        except ValueError as error:
            messagebox.showerror("Invalid Configuration", str(error))
            return

        if self.timer is not None:
            self.timer.stop()

        self.board = generate_board(rows, columns)
        self.flipped_cards = []
        self.matched_cards = set()
        self.waiting_to_hide_cards = False
        self.game_active = True

        self.timer = CountdownTimer(
            root=self.root,
            seconds=timeout,
            on_tick=self._update_timer_label,
            on_finish=self._handle_timeout,
        )

        self._render_board(rows, columns)
        self.status_var.set("Find all matching pairs.")
        self.timer.start()

    def _render_board(self, rows: int, columns: int) -> None:
        for child in self.board_frame.winfo_children():
            child.destroy()

        self.buttons = []
        for row in range(rows):
            button_row: list[tk.Button] = []
            for column in range(columns):
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
                button.grid(row=row, column=column, padx=4, pady=4)
                button_row.append(button)
            self.buttons.append(button_row)

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
            self.status_var.set("Match found.")
            self._check_for_win()
            return

        self.status_var.set("No match. Try again.")
        self.waiting_to_hide_cards = True
        self.root.after(FLIP_BACK_DELAY_MS, self._hide_unmatched_cards)

    def _check_for_win(self) -> None:
        total_cards = len(self.board) * len(self.board[0])
        if len(self.matched_cards) == total_cards:
            self.game_active = False
            if self.timer is not None:
                self.timer.stop()
            self.status_var.set("You matched all pairs.")
            messagebox.showinfo("You Win", "Congratulations! You matched all pairs.")

    def _hide_unmatched_cards(self) -> None:
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
        self.timer_var.set(f"Time: {remaining_seconds}")

    def _handle_timeout(self) -> None:
        if not self.game_active:
            return

        self.game_active = False
        self.status_var.set("Time is up.")
        self._disable_all_cards()
        messagebox.showinfo("Game Over", "Time is up. Better luck next round.")

    def _disable_all_cards(self) -> None:
        for row in self.buttons:
            for button in row:
                if button["text"] == CARD_BACK_TEXT:
                    button.config(bg=CARD_DISABLED_BG, activebackground=CARD_DISABLED_BG)
                button.config(state=tk.DISABLED)
