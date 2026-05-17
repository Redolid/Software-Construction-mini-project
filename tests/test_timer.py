"""Unit tests for src/timer.py"""

from __future__ import annotations

import tkinter as tk
import unittest

from src.timer import CountdownTimer


def _pump_events(root: tk.Tk, ms: int = 50) -> None:
    """Process pending tkinter events without mainloop()."""
    root.update_idletasks()
    root.update()


class TestCountdownTimerInit(unittest.TestCase):
    """Tests for timer construction."""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_initial_remaining_seconds(self):
        timer = CountdownTimer(self.root, 30, lambda s: None, lambda: None)
        self.assertEqual(timer.remaining_seconds, 30)

    def test_timer_not_running_after_creation(self):
        timer = CountdownTimer(self.root, 10, lambda s: None, lambda: None)
        self.assertFalse(timer._running)

    def test_no_job_scheduled_before_start(self):
        timer = CountdownTimer(self.root, 10, lambda s: None, lambda: None)
        self.assertIsNone(timer._job_id)


class TestCountdownTimerStart(unittest.TestCase):
    """Tests for timer.start() behavior."""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.tick_values: list[int] = []

    def tearDown(self):
        self.root.destroy()

    def test_start_calls_on_tick_immediately(self):
        """start() should call on_tick with the full seconds right away."""
        timer = CountdownTimer(
            self.root, 20, lambda s: self.tick_values.append(s), lambda: None
        )
        timer.start()
        self.assertEqual(self.tick_values, [20])

    def test_start_sets_running_flag(self):
        timer = CountdownTimer(self.root, 10, lambda s: None, lambda: None)
        timer.start()
        self.assertTrue(timer._running)

    def test_start_schedules_a_job(self):
        timer = CountdownTimer(self.root, 10, lambda s: None, lambda: None)
        timer.start()
        self.assertIsNotNone(timer._job_id)


class TestCountdownTimerStop(unittest.TestCase):
    """Tests for timer.stop() behavior."""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_stop_clears_running_flag(self):
        timer = CountdownTimer(self.root, 10, lambda s: None, lambda: None)
        timer.start()
        timer.stop()
        self.assertFalse(timer._running)

    def test_stop_clears_job_id(self):
        timer = CountdownTimer(self.root, 10, lambda s: None, lambda: None)
        timer.start()
        timer.stop()
        self.assertIsNone(timer._job_id)

    def test_stop_before_start_does_not_raise(self):
        """Calling stop() on a timer that was never started should be safe."""
        timer = CountdownTimer(self.root, 10, lambda s: None, lambda: None)
        timer.stop()  # should not raise


class TestCountdownTimerTick(unittest.TestCase):
    """Tests for the internal _tick() method."""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.tick_values: list[int] = []
        self.finished = False

    def tearDown(self):
        self.root.destroy()

    def test_tick_decrements_remaining(self):
        """Calling _tick() once should reduce remaining_seconds by 1."""
        timer = CountdownTimer(
            self.root, 5, lambda s: self.tick_values.append(s), lambda: None
        )
        timer.start()  # remaining = 5, on_tick(5) called
        timer._tick()   # remaining = 4, on_tick(4) called
        self.assertEqual(timer.remaining_seconds, 4)
        self.assertIn(4, self.tick_values)

    def test_tick_to_zero_calls_on_finish(self):
        """When remaining hits 0, on_finish must be called."""
        timer = CountdownTimer(
            self.root,
            1,
            lambda s: self.tick_values.append(s),
            lambda: setattr(self, "finished", True),
        )
        timer.start()  # remaining = 1
        timer._tick()   # remaining = 0 → on_finish()
        self.assertTrue(self.finished)
        self.assertEqual(timer.remaining_seconds, 0)

    def test_tick_to_zero_stops_timer(self):
        """After reaching zero the timer should no longer be running."""
        timer = CountdownTimer(
            self.root, 1, lambda s: None, lambda: None
        )
        timer.start()
        timer._tick()
        self.assertFalse(timer._running)

    def test_tick_does_nothing_when_not_running(self):
        """If the timer was stopped, _tick() should be a no-op."""
        timer = CountdownTimer(
            self.root, 5, lambda s: self.tick_values.append(s), lambda: None
        )
        timer.start()  # on_tick(5)
        timer.stop()
        initial_remaining = timer.remaining_seconds
        timer._tick()   # should be ignored
        self.assertEqual(timer.remaining_seconds, initial_remaining)


class TestCountdownTimerRestart(unittest.TestCase):
    """Tests for restarting a timer."""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.tick_values: list[int] = []

    def tearDown(self):
        self.root.destroy()

    def test_start_after_stop_restarts(self):
        """Calling start() again after stop() should resume ticking."""
        timer = CountdownTimer(
            self.root, 10, lambda s: self.tick_values.append(s), lambda: None
        )
        timer.start()
        timer.stop()
        # Manually lower the remaining to simulate partial play
        timer.remaining_seconds = 5
        timer.start()
        self.assertTrue(timer._running)
        self.assertIn(5, self.tick_values)


if __name__ == "__main__":
    unittest.main()
