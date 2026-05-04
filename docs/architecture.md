# Architecture Overview

This project is a single-module Pygame application. The core behavior lives in `main.py`, where the game initializes Pygame, creates a pool of moving squares, then runs a frame loop that updates motion, applies fleeing and jitter, handles lifespan rebirth, and renders the scene.

## Module Dependency Graph

Because the codebase currently centers on one executable module, this graph shows the internal structure inside `main.py` and its external library dependencies.

```mermaid
graph TD
    A["main.py"] --> B["pygame"]
    A --> C["random"]
    A --> D["math"]
    A --> E["dataclasses.dataclass"]

    A --> F["Square"]
    A --> G["SquareSnapshot"]
    A --> H["draw_fps()"]
    A --> I["handle_lifespan_rebirth()"]
    A --> J["main()"]

    F --> G
    F --> H
    F --> I
```

## Runtime Flow

The main loop polls events, snapshots square state, updates every square, replaces dead squares, and then renders the frame.

```mermaid
graph TD
    A["Program start"] --> B["pygame.init()"]
    B --> C["Create window, clock, and font"]
    C --> D["Build initial square pool"]
    D --> E["Enter frame loop"]
    E --> F["clock.tick(FPS)"]
    F --> G["Poll pygame events"]
    G --> H{"QUIT event received?"}
    H -- "Yes" --> I["Set running = False"]
    H -- "No" --> J["Snapshot all squares"]
    I --> U["pygame.quit()"]
    J --> K["Update each square"]
    K --> L["Handle lifespan rebirth"]
    L --> M["Clear screen"]
    M --> N["Draw squares"]
    N --> O["Draw FPS"]
    O --> P["pygame.display.flip()"]
    P --> E
```

## Function Call Graph

The call graph highlights the main control path and the methods that shape each square's behavior.

```mermaid
graph TD
    A["main()"] --> B["pygame.event.get()"]
    A --> C["Square.snapshot()"]
    A --> D["Square.update()"]
    A --> E["handle_lifespan_rebirth()"]
    A --> F["Square.draw()"]
    A --> G["draw_fps()"]
    A --> H["pygame.display.flip()"]
    A --> I["pygame.quit()"]

    D --> D1["Square.update_age()"]
    D --> D2["Square.apply_chaseing()"]
    D --> D3["Square.apply_fleeing()"]
    D --> D4["Square.apply_jitter()"]
    D --> D5["Square.clamp_speed()"]

    D4 --> D4a["Square.should_apply_jitter()"]
    D4 --> D4b["Square.compute_jitter_rotation()"]
    D4 --> D4c["Square.rotate_velocity()"]

    D3 --> D3a["math.hypot()"]
    D2 --> D2a["math.hypot()"]
```

## Sequence Diagram

This sequence shows the primary execution path, including the per-frame loop and the branch that replaces dead squares.

```mermaid
sequenceDiagram
    participant U as "User"
    participant P as "Python runtime"
    participant M as "main.py"
    participant Py as "pygame"
    participant S as "Square objects"

    U->>P: Run the script
    P->>M: Import module and call main()
    M->>Py: init()
    M->>Py: set_mode(), set_caption(), Clock(), SysFont()
    M->>M: Build initial square pool

    loop Each frame
        M->>Py: clock.tick(FPS)
        M->>Py: event.get()
        alt QUIT event seen
            M->>M: running = False
        else Continue running
            M->>M: Capture SquareSnapshot objects
            loop For each square
                M->>S: update(snapshot, delta_time)
                S->>S: update_age()
                S->>S: apply_chaseing()
                S->>S: apply_fleeing()
                S->>S: apply_jitter()
                S->>S: clamp_speed()
                S->>S: Move and bounce within bounds
            end
            M->>M: handle_lifespan_rebirth()
            alt One or more squares died
                M->>M: Remove dead squares and spawn replacements
            else No dead squares
                M->>M: Keep the existing pool
            end
            M->>Py: fill(), draw.rect(), display.flip()
        end
    end

    M->>Py: quit()
```

## Notes

- The project currently has one source file, so the architecture is intentionally compact.
- `SquareSnapshot` exists to keep fleeing and chasing decisions stable within a frame.
- Lifespan rebirth keeps the number of squares constant even when individual squares expire.
