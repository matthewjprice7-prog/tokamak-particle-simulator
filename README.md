# Tokamak Particle Simulator

## Overview

This project is a Python-based simulation exploring charged-particle motion and magnetic-field structure in a simplified tokamak model. I built it to investigate plasma physics concepts computationally and make abstract physical phenomena easier to visualize and explore.

## What It Does

- **Magnetic-field modeling:** Represents a simplified tokamak magnetic field with toroidal and poloidal components and a configurable magnetic perturbation.
- **Particle trajectory simulation:** Numerically integrates charged-particle motion under the modeled electromagnetic forces.
- **3D visualization:** Displays the tokamak geometry, magnetic field lines, and particle trajectories.
- **Poincaré sections:** Plots magnetic field-line intersections to help investigate the structure of the field.
- **Diagnostics:** Includes plots for quantities such as particle energy and phase-space behavior.

## How It Works

The simulator uses Python and numerical integration to evolve particle trajectories. It also traces magnetic field lines separately to produce Poincaré sections. These are different calculations: the field-line plots investigate magnetic geometry, while the particle simulation models motion under the implemented forces.

The model is simplified and is intended as an exploratory computational tool, not a validated prediction of behavior in an actual fusion reactor.


## How to Run

### Requirements

- Python 3
- The packages listed in `requirements.txt`

### Installation

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

### Run the Simulation

Run the main script:

```bash
python simulator.py
```

The simulation calculates particle trajectories and magnetic field lines, then displays an interactive 3D visualization and scientific plots. The computation may take some time to complete.

## Motivation

I wanted to move beyond reading about plasma physics and build something that would let me explore its concepts directly. Developing the simulator has involved learning unfamiliar physics, numerical methods, and visualization techniques, as well as revising my approach when the results did not match my expectations.

## Visual Results

### 3D Tokamak Visualization
<img width="1871" height="926" alt="tokamak-3d" src="https://github.com/user-attachments/assets/ee05d5fe-c08d-4361-94b8-b7add73c35bd" />

This visualization brings together the modeled tokamak geometry, magnetic field lines, and simulated particle trajectories. I built it to make the system's three-dimensional structure easier to explore.

### Poincaré Section
<img width="685" height="759" alt="poincare-section" src="https://github.com/user-attachments/assets/5233399a-f4f4-4be6-b1b4-3ca7e6d40ce8" />


This plot shows intersections of traced magnetic field lines with a cross-section of the modeled system. I used it to investigate how the magnetic perturbation influences field-line structure.

### Simulation Diagnostics
<img width="684" height="760" alt="particle-orbit" src="https://github.com/user-attachments/assets/911f0e36-760a-41fd-9d54-28082314a792" />
<img width="779" height="560" alt="KE_vs_Time" src="https://github.com/user-attachments/assets/b5cffc55-1850-43a7-a878-f18ccde176f6" />
<img width="680" height="752" alt="phase-space" src="https://github.com/user-attachments/assets/4f7bff21-3ac4-45d5-86e2-23f0266e4f06" />
<img width="687" height="751" alt="resonance-check" src="https://github.com/user-attachments/assets/dd7c5317-b02d-4ff1-a7a6-1fb94a55ed77" />


These plots help me examine the simulated particle's behavior through quantities such as energy, phase space, and wave phase. They provide different ways to investigate the numerical results.

## Development Process

I developed this project iteratively, learning the physics and programming techniques needed to implement each feature. Building the visualizations and interpreting the results were important parts of the process, not just ways to display a finished simulation.

The project remains a simplified model. Its results require further numerical and physical validation before they can be treated as predictions of real plasma behavior.
