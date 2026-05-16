# Memory Scramble Game

A Python/tkinter memory card-matching game built for a Software Construction Tools course assignment. The player configures the board size and timeout, then flips cards to find matching pairs before the countdown reaches zero.

## How to Build and Run

### Prerequisites

- **Python 3.9 or newer** (tested on Python 3.9 on macOS and Python 3.10+ on Windows/Linux)
- **tkinter** (included with most Python installations)
- No third-party packages are required

### Steps to Run

1. **Clone the repository:**

   ```bash
   git clone https://github.com/YOUR-USERNAME/Software-Construction-mini-project.git
   cd Software-Construction-mini-project
   ```

2. **Run the game:**

   ```bash
   python3 src/main.py
   ```

   On Windows, use:

   ```bash
   python src/main.py
   ```

3. **If tkinter is missing**, install the Python version from [python.org](https://www.python.org/) or install your OS's tkinter package:
   - **Ubuntu/Debian:** `sudo apt-get install python3-tk`
   - **macOS:** tkinter is included with the system Python and with python.org installers
   - **Windows:** tkinter is included with the standard Python installer

### macOS Note

On macOS you may see: `DEPRECATION WARNING: The system version of Tk is deprecated`. This is a cosmetic warning and does not affect gameplay. To suppress it, run:

```bash
TK_SILENCE_DEPRECATION=1 python3 src/main.py
```

## How to Play

1. **Configure the board** using the `+` and `−` buttons at the top of the window:
   - **Rows**: number of rows (1–10)
   - **Cols**: number of columns (1–10)
   - **Time**: timeout in seconds (10–600, adjusts by 10)
   - The total number of cells (rows × columns) must be **even**

2. **Click "Start Game"** to generate the board and start the countdown timer.

3. **Click on cards** to flip them face-up. Select two cards per turn:
   - If the two cards **match**, they stay face-up
   - If they **don't match**, they flip back face-down after a short delay

4. **Win condition**: match all pairs before the timer runs out.

5. **Game over**: if the countdown reaches zero, a game-over message is displayed.

6. **Move counter and timer** are displayed in the window title bar: `Memory Scramble Game | Moves: X | Time: Y`

7. **Restart anytime** by adjusting the settings and clicking "Start Game" again.

## Team Members

- Student 1: Name / ID
- Student 2: Name / ID
- Student 3: Name / ID

## Project Requirements

| Requirement | Status |
|---|---|
| Player configures board size (nRows × nColumns) | ✅ |
| Board size must be even | ✅ |
| Generates board_size / 2 different symbols | ✅ |
| Each symbol appears exactly twice | ✅ |
| Cards randomly distributed on the board | ✅ |
| Player configures timeout | ✅ |
| Countdown timer visible during play | ✅ |
| Game-over message when timer reaches zero | ✅ |
| Player selects two face-down cards at a time | ✅ |
| Matching cards stay face-up | ✅ |
| Non-matching cards flip back face-down | ✅ |
| Move counter tracks pair attempts | ✅ |
| Game ends successfully when all pairs matched | ✅ |

## Project Structure

```text
Software-Construction-mini-project/
├── src/
│   ├── __init__.py      # Package marker
│   ├── main.py          # Application entry point
│   ├── game.py          # GUI layout and game flow
│   ├── board.py         # Board validation and card generation
│   └── timer.py         # Countdown timer logic
├── README.md            # This file
├── CONTRIBUTING_TASKS.md # Contributor task breakdown
├── PLAN.md              # Team workflow plan
└── requirements.txt     # Python dependencies (none required)
```

## File Responsibilities

### `src/main.py`
Creates the tkinter root window and starts the GUI event loop.

### `src/game.py`
Contains the `MemoryScrambleGame` class — the main GUI and game flow:
- Configuration bar with +/− buttons for rows, columns, and timeout
- Board rendering with reusable card buttons
- Card selection, matching, and flip-back logic
- Move counter and timer display in the window title
- Win and game-over message dialogs

### `src/board.py`
Board validation and random card generation:
- Validates positive row/column values and even total card count
- Generates exactly one pair for each symbol
- Shuffles cards randomly before building the 2D board

### `src/timer.py`
Countdown timer using tkinter's `after()` scheduling:
- Ticks every second and calls back to update the display
- Triggers game-over callback when time reaches zero
- Stops cleanly on win or game restart

## Git Workflow

- `main` — stable final version
- `dev` — integration branch
- `feature/*` — individual feature branches

### Example commands

```bash
# Create a feature branch
git checkout dev
git checkout -b feature/my-feature

# Commit small changes
git add src/game.py
git commit -m "Add card matching behavior"

# Merge into dev
git checkout dev
git merge feature/my-feature
git push origin dev

# Final merge to main
git checkout main
git merge dev
git push origin main
```

## Team Work Split

- **Teammate A** (`feature/game-logic`): Owns `src/board.py` — board validation and pair generation
- **Teammate B** (`feature/timer-config`): Owns `src/timer.py` — countdown and timeout behavior
- **Teammate C** (`feature/ui`): Owns `src/game.py` — tkinter layout and card-click behavior

Detailed contributor tasks are in `CONTRIBUTING_TASKS.md`. Team workflow is in `PLAN.md`.
