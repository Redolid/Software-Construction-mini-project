# Team Plan

This project should be pushed first as a starter scaffold. After that, each teammate should pull the repository, create a feature branch, and add their assigned improvements. This gives the project a real Git history and shows teamwork instead of one final single-person upload.

## Current Status

The project currently has:

- A playable tkinter memory game.
- Board size configuration.
- Timeout configuration.
- Countdown timer.
- Card matching behavior.
- README and contribution notes.

This should be treated as the base version, not the final submission.

## Recommended Workflow

1. Project owner creates a public GitHub repository.
2. Project owner pushes this starter version to `main`.
3. Project owner creates and pushes a `dev` branch.
4. Teammates are added as collaborators on GitHub.
5. Each teammate creates a feature branch from `dev`.
6. Each teammate makes small commits for their assigned task.
7. Feature branches are merged into `dev`.
8. After testing, `dev` is merged into `main`.

## Branches

- `main`: stable submitted version.
- `dev`: integration branch for combining teammate work.
- `feature/game-logic`: board validation, symbols, matching rules.
- `feature/timer-config`: timer behavior, timeout validation, restart cases.
- `feature/ui`: tkinter layout, labels, card appearance, user messages.

## First Push Commands

Run these commands from the `memory-scramble-game` folder.

```bash
git init
git add .
git commit -m "Add initial playable scaffold"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/memory-scramble-game.git
git push -u origin main
```

Then create the integration branch:

```bash
git checkout -b dev
git push -u origin dev
```

## Add Teammates on GitHub

In the GitHub repository:

1. Open `Settings`.
2. Open `Collaborators`.
3. Click `Add people`.
4. Add each teammate's GitHub username.
5. Ask them to accept the invitation.

## Teammate 1: Game Logic

Branch:

```bash
feature/game-logic
```

Files:

- `src/board.py`
- matching-related parts of `src/game.py`

Tasks:

- Review board validation.
- Add clearer validation messages if needed.
- Confirm each symbol appears exactly twice.
- Confirm random shuffle happens for every new game.
- Add comments explaining board generation.
- Add manual test notes to `README.md` or this file.

Suggested commits:

```bash
git add src/board.py
git commit -m "Improve board validation messages"

git add src/board.py README.md
git commit -m "Document board generation testing"
```

## Teammate 2: Timer and Configuration

Branch:

```bash
feature/timer-config
```

Files:

- `src/timer.py`
- timeout-related parts of `src/game.py`

Tasks:

- Confirm timeout accepts only positive numbers.
- Confirm timer stops after winning.
- Confirm timer stops before a restarted game begins.
- Confirm game-over disables all cards.
- Improve status messages related to time.
- Add timer test notes to `README.md` or this file.

Suggested commits:

```bash
git add src/timer.py
git commit -m "Improve countdown timer comments"

git add src/game.py README.md
git commit -m "Document timeout edge cases"
```

## Teammate 3: User Interface

Branch:

```bash
feature/ui
```

Files:

- `src/game.py`

Tasks:

- Improve tkinter spacing and layout.
- Improve card button appearance.
- Improve win and game-over messages.
- Confirm clicks are ignored while unmatched cards are waiting to flip back.
- Confirm the board works for `2x2`, `2x4`, and `4x4`.
- Add a screenshot to the README if required by the instructor.

Suggested commits:

```bash
git add src/game.py
git commit -m "Polish game layout"

git add src/game.py README.md
git commit -m "Document UI manual testing"
```

## Commands for Teammates

Clone the project:

```bash
git clone https://github.com/YOUR-USERNAME/memory-scramble-game.git
cd memory-scramble-game
```

Switch to `dev`:

```bash
git checkout dev
git pull origin dev
```

Create a feature branch:

```bash
git checkout -b feature/game-logic
```

Commit and push changes:

```bash
git add FILE-NAME
git commit -m "Short clear message"
git push -u origin feature/game-logic
```

Then open a pull request on GitHub from the feature branch into `dev`.

## Integration Checklist

Before merging a feature branch into `dev`:

- The game runs with `python src/main.py`.
- The teammate changed only files related to their task.
- Commit messages are clear.
- README or plan notes are updated if behavior changed.
- No generated files such as `__pycache__` are committed.

Before merging `dev` into `main`:

- Run the game manually.
- Test a valid board, such as `4x4`.
- Test a small board, such as `2x2`.
- Test invalid board size, such as `3x3`.
- Test invalid timeout, such as `0` or `abc`.
- Test winning before the timer ends.
- Test losing when the timer reaches zero.

## Final Submission Notes

The final repository should show:

- A public GitHub repository.
- Multiple commits.
- Branches for `main`, `dev`, and feature work.
- README with run instructions.
- Teammate names.
- Evidence that each teammate contributed through commits or pull requests.
