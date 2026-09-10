# Quadtree Particle Simulation

A Python-based particle simulation using **Quadtree** spatial partitioning for efficient collision detection and physics simulation with Pygame visualization.

## Features

- **1000+ Moving Particles** with physics-based motion
- **Random Colors** for visual distinction
- **Wall Collision Detection** with bouncing physics
- **Quadtree Spatial Partitioning** for optimized collision queries
- **Real-time Visualization** at 60 FPS using Pygame

## Project Structure

```
├── main.py                 # Main entry point and game loop
├── Point.py               # Base Point class with rendering
├── PointWithPhysics.py    # Point with velocity and acceleration
├── Quadtree.py            # Quadtree and Rectangle classes
├── Vector2D.py            # 2D vector math utilities
└── README.md              # This file
```

## Classes

### Point
Base class representing a point in 2D space with a position and radius.
- `pos`: Vector2D position
- `r`: radius (int)
- `color`: RGB tuple (randomly generated)
- `show(screen)`: Draws the point on a pygame surface

### PointWithPhysics
Extends Point with velocity and acceleration.
- `vel`: Vector2D velocity
- `acc`: Vector2D acceleration
- `update()`: Updates position based on velocity
- `bounce(area)`: Handles wall collisions
- `collide(other)`: Placeholder for particle-particle collision

### Vector2D
2D vector math utilities.
- `dist(other)`: Distance to another vector
- `magSq()`: Magnitude squared (faster than magnitude)
- Supports addition and in-place addition operations

### Quadtree
Spatial partitioning data structure for efficient collision detection.
- `insert(point)`: Add a point to the tree
- `getQuadTrees(rect)`: Find all quadrants intersecting a rectangle
- `show(screen)`: Visualize the tree boundaries

### Rectangle
Axis-aligned rectangle representation.
- `intersects(other)`: Check intersection with another rectangle
- `isPointInside(point)`: Check if a point is inside

## Installation

1. Clone or download this repository
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install pygame numpy
   ```

## Usage

Run the simulation:
```bash
python main.py
```

Close the window to exit.

## Configuration

Edit these values in `main.py` to customize the simulation:
- `NO_OF_PARTICLE`: Number of particles (default: 1000)
- `capacity`: Max points per quadtree node (default: 10)
- `radius`: Particle radius in pixels (default: 5)
- `max_vel`: Maximum velocity range (default: ±2)
- Screen size: `(1200, 800)` in `pygame.display.set_mode()`

## Dependencies

- **pygame**: Graphics rendering and window management
- **numpy**: (included in requirements, available for future numerical computations)

See `requirements.txt` for exact versions.

## Development

This project uses Git for version control. To contribute:
1. Make changes to the code
2. Test thoroughly with `python main.py`
3. Commit changes: `git commit -m "description"`

## Performance Notes

- The Quadtree implementation provides O(log n) average time complexity for spatial queries
- Rendering 1000+ particles at 60 FPS is CPU-intensive
- Adjust `NO_OF_PARTICLE` if performance is an issue
- Uncomment `qt.show(screen)` in main.py to visualize the quadtree boundaries (may impact performance)
