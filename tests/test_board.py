"""Unit tests for src/board.py"""

from __future__ import annotations

import unittest
from collections import Counter

from src.board import DEFAULT_SYMBOLS, generate_board, validate_board_size


class TestValidateBoardSize(unittest.TestCase):
    """Tests for validate_board_size()."""

    # ── valid sizes (should NOT raise) ──────────────────────────────

    def test_valid_2x2(self):
        """2×2 is the smallest playable even board."""
        validate_board_size(2, 2)  # no exception expected

    def test_valid_4x4(self):
        """4×4 is the default board size."""
        validate_board_size(4, 4)

    def test_valid_2x3(self):
        """2×3 = 6 (even) should be accepted."""
        validate_board_size(2, 3)

    def test_valid_1x2(self):
        """1×2 = 2 (minimum even board) should be accepted."""
        validate_board_size(1, 2)

    def test_valid_large_board(self):
        """A board that uses all available symbols is still valid."""
        # 60 cards → 30 pairs, and DEFAULT_SYMBOLS has 30 entries
        validate_board_size(6, 10)

    # ── odd total (should raise ValueError) ─────────────────────────

    def test_odd_total_3x3(self):
        """3×3 = 9 (odd) must be rejected."""
        with self.assertRaises(ValueError):
            validate_board_size(3, 3)

    def test_odd_total_5x5(self):
        """5×5 = 25 (odd) must be rejected."""
        with self.assertRaises(ValueError):
            validate_board_size(5, 5)

    def test_odd_total_1x3(self):
        """1×3 = 3 (odd) must be rejected."""
        with self.assertRaises(ValueError):
            validate_board_size(1, 3)

    # ── zero or negative values ─────────────────────────────────────

    def test_zero_rows(self):
        with self.assertRaises(ValueError):
            validate_board_size(0, 4)

    def test_zero_columns(self):
        with self.assertRaises(ValueError):
            validate_board_size(4, 0)

    def test_negative_rows(self):
        with self.assertRaises(ValueError):
            validate_board_size(-2, 4)

    def test_negative_columns(self):
        with self.assertRaises(ValueError):
            validate_board_size(4, -3)

    def test_both_zero(self):
        with self.assertRaises(ValueError):
            validate_board_size(0, 0)

    # ── board too small ─────────────────────────────────────────────

    def test_single_cell(self):
        """1×1 = 1 card — cannot form a pair."""
        with self.assertRaises(ValueError):
            validate_board_size(1, 1)

    # ── too many pairs exceed available symbols ─────────────────────

    def test_exceeds_symbol_limit(self):
        """Requesting more pairs than DEFAULT_SYMBOLS has entries must fail."""
        # 10×10 = 100 cards → 50 pairs, but only 30 symbols exist
        with self.assertRaises(ValueError):
            validate_board_size(10, 10)


class TestGenerateBoard(unittest.TestCase):
    """Tests for generate_board()."""

    # ── dimensions ──────────────────────────────────────────────────

    def test_board_dimensions_2x2(self):
        board = generate_board(2, 2)
        self.assertEqual(len(board), 2)
        self.assertTrue(all(len(row) == 2 for row in board))

    def test_board_dimensions_4x4(self):
        board = generate_board(4, 4)
        self.assertEqual(len(board), 4)
        self.assertTrue(all(len(row) == 4 for row in board))

    def test_board_dimensions_2x3(self):
        board = generate_board(2, 3)
        self.assertEqual(len(board), 2)
        self.assertTrue(all(len(row) == 3 for row in board))

    # ── symbol pairing ──────────────────────────────────────────────

    def test_each_symbol_appears_exactly_twice(self):
        """Every symbol on the board must appear exactly 2 times."""
        board = generate_board(4, 4)
        flat = [cell for row in board for cell in row]
        counts = Counter(flat)
        for symbol, count in counts.items():
            self.assertEqual(count, 2, f"Symbol {symbol!r} appeared {count} times")

    def test_correct_number_of_unique_symbols(self):
        """board_size / 2 different symbols should be present."""
        board = generate_board(4, 4)
        flat = [cell for row in board for cell in row]
        unique = set(flat)
        self.assertEqual(len(unique), (4 * 4) // 2)

    def test_symbols_come_from_default_list(self):
        """All symbols on the board must exist in DEFAULT_SYMBOLS."""
        board = generate_board(4, 4)
        flat = [cell for row in board for cell in row]
        for symbol in flat:
            self.assertIn(symbol, DEFAULT_SYMBOLS)

    def test_pair_count_for_small_board(self):
        """1×2 board should have exactly 1 unique symbol (1 pair)."""
        board = generate_board(1, 2)
        flat = [cell for row in board for cell in row]
        self.assertEqual(len(set(flat)), 1)
        self.assertEqual(len(flat), 2)

    # ── randomness (statistical) ────────────────────────────────────

    def test_boards_are_shuffled(self):
        """Two boards generated with the same size are very unlikely identical."""
        boards = [generate_board(4, 4) for _ in range(10)]
        # Flatten each board for easy comparison
        flat_boards = [tuple(cell for row in b for cell in row) for b in boards]
        unique_arrangements = set(flat_boards)
        # With 16! / (2^8) possible arrangements, 10 identical boards
        # is astronomically unlikely — we expect at least 2 distinct ones.
        self.assertGreater(len(unique_arrangements), 1)

    # ── invalid inputs propagate ────────────────────────────────────

    def test_generate_board_rejects_odd_total(self):
        """generate_board must also reject odd totals (it calls validate)."""
        with self.assertRaises(ValueError):
            generate_board(3, 3)

    def test_generate_board_rejects_zero(self):
        with self.assertRaises(ValueError):
            generate_board(0, 4)


class TestDefaultSymbols(unittest.TestCase):
    """Sanity checks on the symbol pool itself."""

    def test_symbols_are_unique(self):
        """No duplicate symbols in the default pool."""
        self.assertEqual(len(DEFAULT_SYMBOLS), len(set(DEFAULT_SYMBOLS)))

    def test_at_least_one_symbol(self):
        self.assertGreater(len(DEFAULT_SYMBOLS), 0)

    def test_symbols_are_non_empty_strings(self):
        for sym in DEFAULT_SYMBOLS:
            self.assertIsInstance(sym, str)
            self.assertGreater(len(sym), 0)


if __name__ == "__main__":
    unittest.main()
