### Variables and Attributes:
MIN_LIFESPAN 
MAX_LIFESPAN 
self.age 
self.lifespan
---

### Main Idea

Each square:

- Starts with `age = 0`
- Has a randomly assigned `lifespan`
- Ages over time using `delta_time`

---

### Functions

#### 1. is_dead()

- Returns:
  self.age >= self.lifespan
- if True then the square is removed

---

#### 2. update_age(delta_time)

- Adds elapsed time to the square’s age
 

---

#### 3. destroy and respawn logic

- If `square.is_dead()`:

    - Remove the square
    - Create a new square with a random size, position and lifespan.