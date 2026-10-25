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


## Current Status

This is an ongoing personal project. The implemented features and visualizations represent my progress so far. The physical model, numerical accuracy, and interpretation of results require further testing and validation.

## Motivation

I wanted to move beyond reading about plasma physics and build something that would let me explore its concepts directly. Developing the simulator has involved learning unfamiliar physics, numerical methods, and visualization techniques, as well as revising my approach when the results did not match my expectations.
