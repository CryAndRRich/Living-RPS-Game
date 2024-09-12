# Living-RPS-Game
This code is a simulation of a Rock-Paper-Scissors game using the Pygame and NumPy library
There are 2 main `class`:
## Object class()
Represents an individual element (rock, paper, or scissors) in the Rock-Paper-Scissors simulation
* **Initializes an Object instance**:
  - `img`: represents the type of object (rock, paper, or scissors)
  - `position`: the initial position of the object as a NumPy array
  - `velocity`: the initial velocity of the object as a NumPy array
  - `acceleration`: the initial acceleration of the object as a NumPy array
* **Updates the object's position and velocity** based on its acceleration using `update_pos` method:
  - The position, velocity is updated by adding the velocity, acceleration and a small random perturbation to introduce randomness in movement
  - Every 20 ticks (frames), the object looks for a nearest target it can defeat (based on the Rock-Paper-Scissors rules)
  - If no target is found (or if it's already at the target), the object randomly selects a new position within a specific range to move towards
  - The object's position, velocity, and acceleration are constrained within defined limits using the `Trim` function to prevent them from moving too fast or out of bounds
* **Updates the object's type** (rock, paper, or scissors) in a cyclic manner using `update_img` method
  - The `img` attribute is incremented and then wrapped around using modulo 3 to ensure it cycles through 0, 1, and 2 (rock, paper, scissors)
## gamePlay class()
Responsible for managing the overall gameplay of the Rock-Paper-Scissors simulation and handling the creation, updating, drawing, and collision detection of the objects (rock, paper, scissors) in the game
* Firstly, populates the game with 60 objects (20 rocks, 20 papers, 20 scissors) (You can add more if you want) with random positions, velocities, and accelerations
* **Detects and handles collisions** between objects by `check_collide` method
  - Compares each pair of objects to see if they collide (based on the distance between their positions)
  - If two objects collide and are of different types, one object "defeats" the other based on the Rock-Paper-Scissors rules
* **Updates the game state** each frame, controlling when and how objects are updated and drawn (`update` method)
## Potential Enhancements
If you want to create your own Living RPS Game, consider several improvements and optimizations:
* **Collision Handling Improvement**:
  - **Collision Response**: instead of changing the object type upon collision, you could add more sophisticated collision handling, like bouncing off or more dynamic interactions
  - **Prevent Double-Counting Collisions** : if an object collides with another, the code might handle the collision twice (once per object). You can mark pairs that have already collided within the same update to prevent double processing
* **Improved Randomization**: The random movement and acceleration updates could be made more realistic by tweaking the randomness to simulate more natural motion patterns, such as smooth transitions or inertia
* **Frame Rate Independence**: instead of using a fixed FPS, consider making the game update logic independent of the frame rate, allowing the game to run smoothly on different hardware
