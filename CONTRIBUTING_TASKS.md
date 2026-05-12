# Contributor Tasks

Use this file to divide the work between 2-3 teammates. Each teammate should work on a separate branch, make small commits, and merge into `dev` before the final merge into `main`.

## Important Git Note

Even if the files already exist locally, you can still create multiple commits before pushing to GitHub. Do not run `git add .` for the first commit. Instead, stage related files one group at a time.

Example:

```bash
git init
git add .gitignore requirements.txt README.md
git commit -m "Add project documentation and setup files"

git add src/__init__.py src/main.py
git commit -m "Add application entry point"

git add src/board.py
git commit -m "Add board validation and generation"

git add src/timer.py
git commit -m "Add countdown timer"

git add src/game.py
git commit -m "Add tkinter memory game interface"
```

After that, connect GitHub and push:

```bash
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/memory-scramble-game.git
git push -u origin main
```

## Branch Setup

Create `dev` from `main`:

```bash
git checkout -b dev
git push -u origin dev
```

Each teammate creates a feature branch from `dev`:

```bash
git checkout dev
git pull origin dev
git checkout -b feature/branch-name
```

## Teammate A: Game Logic

Branch:

```bash
feature/game-logic
```

Main files:

- `src/board.py`
- related parts of `src/game.py` if matching rules need small changes

Tasks:

- Review and improve board validation messages.
- Confirm odd board sizes are rejected.
- Confirm zero or negative rows/columns are rejected.
- Confirm each symbol appears exactly twice.
- Confirm symbols are shuffled each game.
- Optionally add a simple test script or manual testing notes.

Suggested commits:

```bash
git add src/board.py
git commit -m "Improve board validation"

git add src/board.py
git commit -m "Document board generation logic"
```

## Teammate B: Timer and Configuration

Branch:

```bash
feature/timer-config
```

Main files:

- `src/timer.py`
- timeout-related parts of `src/game.py`

Tasks:

- Review timeout validation.
- Confirm non-numeric timeout values are rejected.
- Confirm zero and negative timeout values are rejected.
- Confirm timer stops when the player wins.
- Confirm timer restarts cleanly when a new game starts.
- Confirm game-over message appears when time reaches zero.

Suggested commits:

```bash
git add src/timer.py
git commit -m "Review countdown timer behavior"

git add src/game.py
git commit -m "Improve timeout validation"
```

## Teammate C: User Interface

Branch:

```bash
feature/ui
```

Main files:

- `src/game.py`

Tasks:

- Improve labels, spacing, and button layout.
- Confirm card buttons are easy to click.
- Confirm selected cards flip face-up.
- Confirm matched cards stay visible.
- Confirm unmatched cards flip back after a short delay.
- Confirm the board is disabled after game over.

Suggested commits:

```bash
git add src/game.py
git commit -m "Improve game layout"

git add src/game.py
git commit -m "Polish card button states"
```

## Integration Owner

Branch:

```bash
dev
```

Main files:

- `README.md`
- all files during final review

Tasks:

- Merge completed feature branches into `dev`.
- Resolve merge conflicts.
- Run the game manually.
- Check README instructions.
- Merge `dev` into `main` only when the project is stable.

Suggested commands:

```bash
git checkout dev
git merge feature/game-logic
git merge feature/timer-config
git merge feature/ui
python src/main.py
git push origin dev

git checkout main
git merge dev
git push origin main
```

## Manual Testing Checklist

- Start a `4 x 4` game with `60` seconds.
- Start a `2 x 2` game with `10` seconds.
- Try an odd board size, such as `3 x 3`.
- Try invalid text input, such as `abc`.
- Try timeout `0`.
- Match all pairs before time runs out.
- Let the timer reach zero.
- Restart the game after winning.
- Restart the game after losing.

## Pull Request Checklist

Before merging into `dev`, each teammate should confirm:

- The game still runs with `python src/main.py`.
- The changed file has clear responsibility.
- No unrelated files were changed.
- README instructions are still correct.
- The commit messages are small and understandable.
