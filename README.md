# Memory Scramble Game

A beginner-friendly Python/tkinter memory game for a Software Construction Tools assignment. The player chooses the number of rows, columns, and a timeout, then flips cards to find matching pairs before the countdown reaches zero.

This repository starts as a playable scaffold. Teammates should still create feature branches, improve their assigned parts, make small commits, and merge through `dev` before the final submission.

## Team Members

- Student 1: Name / ID
- Student 2: Name / ID
- Student 3: Name / ID

## Project Requirements

- The board is configured using `nRows` and `nColumns`.
- `nRows * nColumns` must be even.
- The game creates `board_size / 2` different symbols.
- Each symbol appears exactly twice.
- Cards are randomly distributed on the board.
- The player configures the timeout in seconds.
- A countdown timer is visible during play.
- If the timer reaches zero before all matches are found, the game shows a game-over message.
- The player selects two face-down cards at a time.
- Matching cards stay face-up.
- Non-matching cards flip back face-down.
- Cards use different visual states for hidden, selected, matched, and disabled.
- The game ends successfully when all pairs are matched.

## Technology

- Python 3.10 or newer
- tkinter GUI
- No third-party Python packages are required

## Project Structure

```text
memory-scramble-game/
+-- src/
|   +-- __init__.py
|   +-- main.py
|   +-- game.py
|   +-- board.py
|   +-- timer.py
+-- README.md
+-- requirements.txt
+-- .gitignore
```

## File Responsibilities

### `src/main.py`

Starts the tkinter application.

Owner suggestion: integration owner.

Implementation requirements:
- Create the main window.
- Load `MemoryScrambleGame`.
- Start the tkinter event loop.

### `src/game.py`

Contains the GUI and main game flow.

Owner suggestion: UI teammate or integration teammate.

Implementation requirements:
- Show inputs for rows, columns, and timeout.
- Render the board as clickable buttons.
- Allow selecting two face-down cards.
- Keep matching cards visible.
- Hide non-matching cards after a short delay.
- Show win and game-over messages.

### `src/board.py`

Contains board validation and random card generation.

Owner suggestion: game-logic teammate.

Implementation requirements:
- Validate positive row and column values.
- Validate that total card count is even.
- Generate exactly one pair for each symbol.
- Shuffle the cards before building the board.

### `src/timer.py`

Contains countdown timer logic.

Owner suggestion: timer/config teammate.

Implementation requirements:
- Store remaining seconds.
- Update the GUI every second.
- Trigger game-over when the countdown reaches zero.
- Stop cleanly when the game is won or restarted.

## How to Run

From the project folder:

```bash
python src/main.py
```

On some systems you may need:

```bash
python3 src/main.py
```

If tkinter is missing, install the Python version from [python.org](https://www.python.org/) or install your operating system's tkinter package.

## Suggested Git Workflow

Use `main` as the stable final branch. Use `dev` as the integration branch where completed features are merged before the final release.

Suggested branches:

- `main`: stable final version
- `dev`: integration branch
- `feature/ui`: tkinter layout and board buttons
- `feature/ui-game-flow`: UI states, card matching polish, and game flow review
- `feature/game-logic`: board generation and matching rules
- `feature/timer-config`: timeout input and countdown behavior

## Example Git Commands

Create the repository:

```bash
git init
git add .
git commit -m "Initial project structure"
git branch -M main
```

Create and push the integration branch:

```bash
git checkout -b dev
git push -u origin dev
```

Create a feature branch:

```bash
git checkout dev
git checkout -b feature/game-logic
```

Commit a small change:

```bash
git add src/board.py
git commit -m "Add board validation and generation"
```

Merge a feature branch into `dev`:

```bash
git checkout dev
git merge feature/game-logic
git push origin dev
```

Merge final work into `main`:

```bash
git checkout main
git merge dev
git push origin main
```

Connect to a public GitHub repository:

```bash
git remote add origin https://github.com/YOUR-USERNAME/memory-scramble-game.git
git push -u origin main
```

## Suggested Small Commit Plan

1. `Initial project structure`
   - Add `src/`, `README.md`, `requirements.txt`, and `.gitignore`.

2. `Add board validation and generation`
   - Implement `src/board.py`.
   - Validate rows, columns, even board size, and maximum supported symbols.

3. `Add countdown timer`
   - Implement `src/timer.py`.
   - Add start, stop, tick, and timeout callback behavior.

4. `Build tkinter game layout`
   - Implement configuration inputs.
   - Render card buttons.

5. `Add card matching behavior`
   - Flip selected cards.
   - Keep matches visible.
   - Hide non-matches.

6. `Add win and game-over states`
   - Stop timer when player wins.
   - Disable board when time runs out.

7. `Update README with run and Git workflow`
   - Add setup instructions, branch plan, and teammate responsibilities.

## Edge Cases to Handle

- Rows or columns are empty.
- Rows or columns are not numbers.
- Rows or columns are zero or negative.
- `nRows * nColumns` is odd.
- Board has fewer than two cards.
- Requested board is larger than the available symbol list.
- Timeout is empty, non-numeric, zero, or negative.
- Player clicks the same card twice.
- Player clicks a third card while two non-matching cards are waiting to flip back.
- Player restarts the game while a timer is already running.
- Timer reaches zero at the same time the player finds the final match.

## Team Work Split

Detailed contributor tasks are available in `CONTRIBUTING_TASKS.md`.

The recommended team workflow is available in `PLAN.md`.

- Teammate A: `feature/game-logic`
  - Owns `src/board.py`.
  - Tests board validation and random pair generation.

- Teammate B: `feature/timer-config`
  - Owns `src/timer.py`.
  - Tests countdown, restart, and timeout behavior.

- Teammate C: `feature/ui`
  - Owns `src/game.py`.
  - Builds the tkinter layout and card-click behavior.

Everyone should review changes through pull requests before merging into `dev`.
