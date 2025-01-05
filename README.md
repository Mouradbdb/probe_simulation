
# Space Probe Simulation with Multiple Gravities

## Overview

A Pygame-based simulation where you control a space probe navigating through a dynamic gravitational environment with multiple celestial bodies exerting gravitational forces.

## Features

- **Multiple Masses:** Navigate around multiple planets/stars with varying masses and gravitational pulls.
- **Realistic Physics:** Experience gravitational acceleration based on Newton's law of universal gravitation.
- **Thruster Mechanics:** Control the probe's thrust and rotation to maneuver effectively.
- **Visual Feedback:** Gravitational force vectors, trajectory trails, and glowing celestial bodies enhance immersion.
- **Telemetry:** Real-time data display for velocities, angles, distances, and gravitational acceleration.

## Controls

- **Left Arrow (`←`):** Rotate probe clockwise.
- **Right Arrow (`→`):** Rotate probe counter-clockwise.
- **Up Arrow (`↑`):** Activate thrusters to apply thrust in the facing direction.
- **Escape (`ESC`):** Exit the simulation.

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/space_probe_simulation.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd space_probe_simulation
   ```

3. **Install Dependencies:**
   Ensure you have Python installed. Install Pygame using pip:
   ```bash
   pip install pygame
   ```

4. **Run the Simulation:**
   ```bash
   python src/main.py
   ```

## Folder Structure

```plaintext
space_probe_simulation/
│
├── assets/
│   ├── images/
│   └── sounds/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── probe.py
│   ├── mass.py
│   ├── particle.py
│   ├── utils.py
│   └── settings.py
│
└── README.md
```

## Customization

- **Adding More Masses:** Modify the `masses` list in `main.py` to add more celestial bodies with desired properties.

- **Adjusting Gravitational Constant:** Modify the `G` value in `settings.py` to tweak gravitational force intensity.

- **Changing Probe Properties:** Adjust the `Probe` class in `probe.py` to modify thrust, rotation speed, or size.

## Future Enhancements

- **Dynamic Mass Movements:** Allow celestial bodies to move or respond to player actions.
- **Collision Detection:** Implement collisions between the probe and masses.
- **Fuel Mechanics:** Introduce fuel consumption and management.
- **Multiple Levels/Missions:** Design varied missions with different objectives and challenges.

## License

MIT License

## Acknowledgements

Inspired by physics simulations and space exploration concepts.
