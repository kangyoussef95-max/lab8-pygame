# Lab 8 - Pygame Random Squares

A Python + Pygame application that displays 10 colored squares moving around the window with dynamic lifespan and rebirth mechanics.

## Features

- **Random Movement**: Squares move at different speeds based on their size (larger = slower).
- **Jitter**: Small random rotations applied to movement direction for visual interest.
- **Fleeing Behavior**: Smaller squares detect and flee from nearby larger squares within a configurable radius.
- **Lifespan & Rebirth**: Each square has a random lifespan (30–180 seconds). When a square reaches the end of its life, it is removed and replaced with a new square to maintain a constant pool of 10 squares.

## Game Mechanics

### Lifespan System
- Each square is assigned a random lifespan between `MIN_LIFESPAN` (30s) and `MAX_LIFESPAN` (180s).
- The square's age increases by `delta_time` each frame (scales with frame rate).
- When `age >= lifespan`, the square is marked as dead.
- Dead squares are removed and replaced with new squares (random size, position, and lifespan).

### Movement & Interaction
- Squares bounce off window edges.
- Larger squares push smaller squares away (fleeing mechanics).
- Jitter adds slight velocity rotations for more natural movement.

## Requirements

- Python 3.13+
- Pygame (listed in requirements.txt)

## Setup

1. Create a local virtual environment:

   ```powershell
   python -m venv .venv
   ```

2. Activate the virtual environment:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

## Run

```powershell
python main.py
```

## Project Files

- **main.py**: Pygame app entry point with all game mechanics (movement, fleeing, lifespan, rebirth).
- **requirements.txt**: Python dependency versions for reproducible installs.
- **MY_NOTES.md**: Design notes for the lifespan rebirth feature.
