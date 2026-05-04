# Refactoring Plan

## 1. Overview

This project is a single-file Pygame app in main.py. It creates a set of moving squares, updates them every frame, applies jitter and chase/flee behavior, replaces dead squares, and draws the result to the screen.

The code already works as a complete lab solution, so the refactoring should stay small and safe. The main improvements are clearer naming, less repeated logic, and comments that explain why each step exists.

## 2. Refactoring Goals

- Make names more consistent and easier to read.
- Reduce repeated logic in the movement methods.
- Replace a few verbose patterns with direct, readable expressions.
- Improve comments and docstrings so they describe the real behavior, not just the earlier stub intent.
- Keep the game behavior the same while making the code easier to study.

## 3. Step-by-Step Refactoring Plan

### Step 1: Normalize the naming style

Rename the chase-related identifiers so they match the rest of the file’s style. For example, change apply_chaseing to apply_chasing and chase_RADIUS to CHASE_RADIUS. Keep the same behavior and update every call site.

Why this helps: consistent names make the code easier to scan and reduce confusion for beginners who are trying to follow the control flow.

Inline comment guidance for the final code: add short comments near the renamed constants or methods explaining that the names now match the purpose of the code and are easier to read.

### Step 2: Simplify small boolean returns

Replace verbose if/return patterns with direct boolean expressions where possible. A good example is is_dead(), which can return the comparison result directly.

Why this helps: beginner code is easier to follow when a function says exactly what it means without extra branching.

Inline comment guidance for the final code: add a brief comment above the direct return that explains the function is checking one condition and does not need an extra branch.

### Step 3: Reduce repeated math in the chase and flee methods

Look for the shared pattern in apply_fleeing() and apply_chasing(): compute the square center, compare against every other square, ignore self, ignore the wrong size group, measure distance, and handle distance == 0 safely.

Refactor that shared pattern into a small private helper or a clearly named local helper section so the two methods focus on their different behavior instead of repeating the same setup code.

Why this helps: duplicated logic is harder to debug and harder to change later. A shared helper also makes the difference between fleeing and chasing easier to study.

Inline comment guidance for the final code: add a short comment where the shared helper is introduced to explain that the helper exists because both methods use the same frame geometry and safety checks.

### Step 4: Tighten the frame-loop comments and structure

Keep main() behavior the same, but rewrite the surrounding comments so the order of operations is obvious: poll events, snapshot squares, update them, handle rebirth, draw the frame, then flip the display.

If one or two tiny helper variables make the loop clearer, add them only when they do not change behavior.

Why this helps: the frame loop is the heart of the program, so the reader should be able to trace it from top to bottom without guessing why each step happens.

Inline comment guidance for the final code: add one concise comment before the snapshot/update block and one before the rebirth/render block so the frame order is easy to understand.

### Step 5: Replace leftover stub-style wording

Several docstrings and comments still say Stub or TODO even though the methods are implemented. Update them so they describe the current behavior directly.

Why this helps: inaccurate comments confuse readers more than no comments at all, especially in a teaching project.

Inline comment guidance for the final code: make each comment explain what the code now does and why that behavior matters.

## 4. Final Output Requirements

When the plan is executed, the output must:

- Contain only the refactored code.
- Include short inline comments that explain what changed.
- Include short inline comments that explain why the change improves readability, maintainability, or correctness.
- Keep the comments beginner-friendly and concise.
- Preserve the same gameplay behavior unless a change is strictly about readability.

## 5. Key Concepts for Students

- Naming consistency: similar ideas should use similar names.
- DRY: do not repeat the same logic in multiple places.
- Boolean expressions: sometimes a direct return is clearer than an if/else block.
- Helper functions: a small helper can make a larger method easier to read.
- Frame order: in game loops, the order of update steps can affect behavior.
- Defensive programming: special cases like distance == 0 prevent crashes.

## 6. Safety Notes

- Test after each small change so behavior stays the same.
- Keep the snapshot/update order unchanged unless you are deliberately changing the game logic.
- Do not remove the zero-distance safeguards in the movement code.
- After renaming methods or constants, update every reference so the file still runs.
- Re-run the game after the refactor to make sure squares still move, bounce, flee, chase, and respawn correctly.
