"""Unit tests for src/game.py"""

from __future__ import annotations

import tkinter as tk
import unittest
from unittest.mock import patch

from src.game import CARD_BACK_TEXT, MemoryScrambleGame


class TestGameDefaults(unittest.TestCase):
    """Verify initial configuration values."""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.game = MemoryScrambleGame(self.root)

    def tearDown(self):
        if self.game.timer:
            self.game.timer.stop()
        self.root.destroy()

    def test_default_rows(self):
        self.assertEqual(self.game.rows_val, 4)

    def test_default_columns(self):
        self.assertEqual(self.game.columns_val, 4)

    def test_default_timeout(self):
        self.assertEqual(self.game.timeout_val, 60)

    def test_game_not_active_before_start(self):
        self.assertFalse(self.game.game_active)

    def test_moves_count_starts_at_zero(self):
        self.assertEqual(self.game.moves_count, 0)

    def test_no_matched_cards_before_start(self):
        self.assertEqual(len(self.game.matched_cards), 0)


class TestAdjust(unittest.TestCase):
    """Tests for the +/− configuration buttons."""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.game = MemoryScrambleGame(self.root)

    def tearDown(self):
        if self.game.timer:
            self.game.timer.stop()
        self.root.destroy()

    # ── rows ────────────────────────────────────────────────────────

    def test_increase_rows(self):
        self.game._adjust("rows", 1)
        self.assertEqual(self.game.rows_val, 5)

    def test_decrease_rows(self):
        self.game._adjust("rows", -1)
        self.assertEqual(self.game.rows_val, 3)

    def test_rows_lower_bound(self):
        """Rows should not drop below 1."""
        for _ in range(20):
            self.game._adjust("rows", -1)
        self.assertEqual(self.game.rows_val, 1)

    def test_rows_upper_bound(self):
        """Rows should not exceed 10."""
        for _ in range(20):
            self.game._adjust("rows", 1)
        self.assertEqual(self.game.rows_val, 10)

    # ── columns ─────────────────────────────────────────────────────

    def test_increase_columns(self):
        self.game._adjust("cols", 1)
        self.assertEqual(self.game.columns_val, 5)

    def test_decrease_columns(self):
        self.game._adjust("cols", -1)
        self.assertEqual(self.game.columns_val, 3)

    def test_columns_lower_bound(self):
        for _ in range(20):
            self.game._adjust("cols", -1)
        self.assertEqual(self.game.columns_val, 1)

    def test_columns_upper_bound(self):
        for _ in range(20):
            self.game._adjust("cols", 1)
        self.assertEqual(self.game.columns_val, 10)

    # ── timeout ─────────────────────────────────────────────────────

    def test_increase_timeout(self):
        self.game._adjust("time", 10)
        self.assertEqual(self.game.timeout_val, 70)

    def test_decrease_timeout(self):
        self.game._adjust("time", -10)
        self.assertEqual(self.game.timeout_val, 50)

    def test_timeout_lower_bound(self):
        """Timeout should not drop below 10."""
        for _ in range(100):
            self.game._adjust("time", -10)
        self.assertEqual(self.game.timeout_val, 10)

    def test_timeout_upper_bound(self):
        """Timeout should not exceed 600."""
        for _ in range(100):
            self.game._adjust("time", 10)
        self.assertEqual(self.game.timeout_val, 600)


class TestStartGame(unittest.TestCase):
    """Tests for starting a new game."""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.game = MemoryScrambleGame(self.root)

    def tearDown(self):
        if self.game.timer:
            self.game.timer.stop()
        self.root.destroy()

    @patch("tkinter.messagebox.showerror")
    def test_start_with_odd_total_shows_error(self, mock_err):
        """3×3 = 9 should show an error dialog and NOT activate the game."""
        self.game.rows_val = 3
        self.game.columns_val = 3
        self.game.start_game()
        mock_err.assert_called_once()
        self.assertFalse(self.game.game_active)

    def test_start_activates_game(self):
        self.game.start_game()
        self.assertTrue(self.game.game_active)

    def test_start_creates_board(self):
        self.game.start_game()
        self.assertEqual(len(self.game.board), 4)
        self.assertTrue(all(len(row) == 4 for row in self.game.board))

    def test_start_resets_moves(self):
        self.game.moves_count = 99
        self.game.start_game()
        self.assertEqual(self.game.moves_count, 0)

    def test_start_resets_matched_cards(self):
        self.game.matched_cards = {(0, 0), (0, 1)}
        self.game.start_game()
        self.assertEqual(len(self.game.matched_cards), 0)

    def test_start_creates_timer(self):
        self.game.start_game()
        self.assertIsNotNone(self.game.timer)

    def test_restart_stops_previous_timer(self):
        """Starting a second game should stop the first timer cleanly."""
        self.game.start_game()
        first_timer = self.game.timer
        self.game.start_game()
        self.assertFalse(first_timer._running)


class TestCardSelection(unittest.TestCase):
    """Tests for select_card() logic."""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.game = MemoryScrambleGame(self.root)
        # Use a 2×2 board with a known layout for predictable tests
        self.game.rows_val = 2
        self.game.columns_val = 2
        self.game.start_game()
        # Force a known board: A A / B B
        self.game.board = [["A", "A"], ["B", "B"]]

    def tearDown(self):
        if self.game.timer:
            self.game.timer.stop()
        self.root.destroy()

    def test_first_card_flips(self):
        """Selecting the first card should add it to flipped_cards."""
        self.game.select_card(0, 0)
        self.assertIn((0, 0), self.game.flipped_cards)

    def test_selecting_same_card_twice_ignored(self):
        """Clicking the same card again should be ignored."""
        self.game.select_card(0, 0)
        self.game.select_card(0, 0)
        self.assertEqual(len(self.game.flipped_cards), 1)

    def test_selecting_card_when_game_inactive_ignored(self):
        """No card should flip if game_active is False."""
        self.game.game_active = False
        self.game.select_card(0, 0)
        self.assertEqual(len(self.game.flipped_cards), 0)

    def test_selecting_matched_card_ignored(self):
        """Already-matched cards cannot be selected."""
        self.game.matched_cards.add((0, 0))
        self.game.select_card(0, 0)
        self.assertEqual(len(self.game.flipped_cards), 0)

    @patch("tkinter.messagebox.showinfo")
    def test_matching_pair_stays_face_up(self, mock_info):
        """Two identical cards should be added to matched_cards."""
        # board[0][0] == board[0][1] == "A"
        self.game.select_card(0, 0)
        self.game.select_card(0, 1)
        self.assertIn((0, 0), self.game.matched_cards)
        self.assertIn((0, 1), self.game.matched_cards)

    @patch("tkinter.messagebox.showinfo")
    def test_matching_pair_clears_flipped(self, mock_info):
        """After a match, flipped_cards should be cleared."""
        self.game.select_card(0, 0)
        self.game.select_card(0, 1)
        self.assertEqual(len(self.game.flipped_cards), 0)

    def test_non_matching_pair_sets_waiting_flag(self):
        """Mismatched cards should trigger the waiting-to-hide state."""
        # board[0][0] = "A", board[1][0] = "B" → mismatch
        self.game.select_card(0, 0)
        self.game.select_card(1, 0)
        self.assertTrue(self.game.waiting_to_hide_cards)

    def test_selecting_during_wait_ignored(self):
        """While waiting to flip back, further clicks should be ignored."""
        self.game.select_card(0, 0)
        self.game.select_card(1, 0)  # mismatch → waiting
        self.game.select_card(1, 1)  # should be ignored
        # flipped_cards still holds the mismatched pair (not a third card)
        self.assertEqual(len(self.game.flipped_cards), 2)

    @patch("tkinter.messagebox.showinfo")
    def test_moves_increment_on_pair_attempt(self, mock_info):
        """Each pair attempt (2 cards selected) should increase moves by 1."""
        self.game.select_card(0, 0)
        self.game.select_card(0, 1)
        self.assertEqual(self.game.moves_count, 1)


class TestWinCondition(unittest.TestCase):
    """Tests for the win check."""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.game = MemoryScrambleGame(self.root)
        self.game.rows_val = 2
        self.game.columns_val = 2
        self.game.start_game()
        self.game.board = [["A", "A"], ["B", "B"]]

    def tearDown(self):
        if self.game.timer:
            self.game.timer.stop()
        self.root.destroy()

    @patch("tkinter.messagebox.showinfo")
    def test_win_after_all_pairs_matched(self, mock_info):
        """Matching every pair should deactivate the game and show a message."""
        # Match first pair
        self.game.select_card(0, 0)
        self.game.select_card(0, 1)
        # Match second pair
        self.game.select_card(1, 0)
        self.game.select_card(1, 1)

        self.assertFalse(self.game.game_active)
        mock_info.assert_called_once()

    @patch("tkinter.messagebox.showinfo")
    def test_win_stops_timer(self, mock_info):
        """Winning should stop the countdown timer."""
        self.game.select_card(0, 0)
        self.game.select_card(0, 1)
        self.game.select_card(1, 0)
        self.game.select_card(1, 1)

        self.assertFalse(self.game.timer._running)

    @patch("tkinter.messagebox.showinfo")
    def test_moves_counted_correctly_on_win(self, mock_info):
        """A perfect 2×2 game takes exactly 2 moves."""
        self.game.select_card(0, 0)
        self.game.select_card(0, 1)
        self.game.select_card(1, 0)
        self.game.select_card(1, 1)
        self.assertEqual(self.game.moves_count, 2)


class TestGameOver(unittest.TestCase):
    """Tests for the timeout / game-over path."""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.game = MemoryScrambleGame(self.root)
        self.game.start_game()

    def tearDown(self):
        if self.game.timer:
            self.game.timer.stop()
        self.root.destroy()

    @patch("tkinter.messagebox.showinfo")
    def test_timeout_deactivates_game(self, mock_info):
        """When the timer fires _handle_timeout, game_active must be False."""
        self.game._handle_timeout()
        self.assertFalse(self.game.game_active)

    @patch("tkinter.messagebox.showinfo")
    def test_timeout_shows_message(self, mock_info):
        """A game-over dialog should appear on timeout."""
        self.game._handle_timeout()
        mock_info.assert_called_once()

    @patch("tkinter.messagebox.showinfo")
    def test_timeout_disables_all_cards(self, mock_info):
        """After timeout, every button should be disabled."""
        self.game._handle_timeout()
        for row in self.game.buttons:
            for btn in row:
                if btn.winfo_ismapped():
                    self.assertEqual(str(btn["state"]), "disabled")

    @patch("tkinter.messagebox.showinfo")
    def test_no_card_selection_after_timeout(self, mock_info):
        """Card clicks should be ignored after game over."""
        self.game._handle_timeout()
        self.game.select_card(0, 0)
        self.assertEqual(len(self.game.flipped_cards), 0)


class TestHideUnmatchedCards(unittest.TestCase):
    """Tests for _hide_unmatched_cards() flip-back behavior."""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.game = MemoryScrambleGame(self.root)
        self.game.rows_val = 2
        self.game.columns_val = 2
        self.game.start_game()
        self.game.board = [["A", "B"], ["B", "A"]]

    def tearDown(self):
        if self.game.timer:
            self.game.timer.stop()
        self.root.destroy()

    def test_hide_clears_flipped_list(self):
        """After hiding, flipped_cards should be empty."""
        self.game.select_card(0, 0)  # A
        self.game.select_card(0, 1)  # B → mismatch
        self.game._hide_unmatched_cards()
        self.assertEqual(len(self.game.flipped_cards), 0)

    def test_hide_clears_waiting_flag(self):
        self.game.select_card(0, 0)
        self.game.select_card(0, 1)
        self.game._hide_unmatched_cards()
        self.assertFalse(self.game.waiting_to_hide_cards)

    def test_hide_restores_card_text(self):
        """Hidden cards should show the back text again."""
        self.game.select_card(0, 0)
        self.game.select_card(0, 1)
        self.game._hide_unmatched_cards()
        self.assertEqual(self.game.buttons[0][0]["text"], CARD_BACK_TEXT)
        self.assertEqual(self.game.buttons[0][1]["text"], CARD_BACK_TEXT)


if __name__ == "__main__":
    unittest.main()
