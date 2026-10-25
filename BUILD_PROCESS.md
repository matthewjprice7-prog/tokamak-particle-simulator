# Building the Tokamak Particle Simulator
## A Retrospective on the Development Process

*Admittedly, the documentation for this project is very poor. Many old screenshots of results before the final version are lost, and I failed to document progress during the actual building of the simulator. This document reconstructs the project's development process from memory. The exact order of some implementations may be uncertain, but the scientific motivations, major features, and challenges reflect my experience building the simulator.*

## 1. The Original Vision

My original ambition was to model an actual plasma and investigate whether a tokamak with particular parameters could successfully confine it. I wanted to build something that went beyond visualizing physics and could help me investigate meaningful questions about plasma confinement.

As I began working, I encountered a significant gap between that ambition and my programming abilities. Rather than attempting the entire problem at once, I began developing smaller components that would help me work toward the larger goal.

Over time, the project evolved into a simulator focused on magnetic-field structure, charged-particle motion, and the effects of magnetic perturbations and electric fields. Although it has not reached my original goal of modeling an actual plasma, each stage has helped me understand more about the computational tools needed to investigate it.

## 2. From a Simple Model to Three Dimensions

My first version simulated the motion of a charged particle through a simple two-dimensional magnetic field. This was an initial step toward the more ambitious project I envisioned for my MIT maker portfolio.

I eventually realized that I needed to learn how to represent and visualize a complicated three-dimensional structure before I could develop a more complete tokamak model.

This introduced a different kind of challenge. I was no longer just working with equations describing particle motion; I also had to translate a complex physical geometry into code and make it visually interpretable.

## 3. Building the Tokamak Geometry

One of the most difficult parts of the project was coding the toroidal geometry of the tokamak. Programming was one of my weakest skills, and translating a complicated three-dimensional shape into something a computer could represent was a substantial challenge.

Working through this problem helped me develop the programming skills necessary for the rest of the project. It also taught me that building a scientific simulation involves more than understanding the underlying physics: I had to learn how to represent that physics computationally.

Once I had the torus geometry working, I moved on to representing the magnetic field within it.

## 4. Modeling Magnetic Fields

After developing the geometry, I implemented magnetic-field lines to visualize the structure of the modeled magnetic field.

This was an important distinction in the project's development. The geometry established the physical shape of the tokamak, while the field lines allowed me to explore the magnetic structure within that geometry.

Visualizing the field also provided a foundation for later analysis. I wanted to understand not just what the magnetic field looked like in three dimensions, but how its structure changed under different conditions.

## 5. Poincaré Sections and Magnetic Island Formation

I next added a Poincaré section, which allowed me to examine magnetic-field structure through repeated intersections of field lines with a cross-section of the tokamak.

Initially, the plot showed an orderly pattern, providing a baseline for investigating how the magnetic structure could change.

My goal was to study magnetic island formation, so I began experimenting with magnetic perturbations. I immediately saw changes in the resulting patterns, giving me a way to investigate how the perturbations affected the modeled magnetic field.

I could compare these visual results with concepts I had encountered in research papers. Instead of only reading about magnetic island formation, I had built a tool that let me explore the phenomenon computationally.

This was one of the most rewarding moments of the project. Abstract physics had become something I could investigate directly through a system I had developed myself.

## 6. Developing Particle Diagnostics

As the simulator expanded, I added diagnostic plots to help me analyze particle behavior beyond what I could see in the three-dimensional visualization.

Of these diagnostics, I found the kinetic energy plot the most useful. It was cleaner and easier to interpret than the other plots, making it easier to follow how a particle's kinetic energy changed over time.

This taught me something about scientific visualization: generating more plots does not necessarily make a model more informative. A useful diagnostic must communicate the behavior being investigated clearly enough for someone to interpret it.

The kinetic energy plot gave me a particularly accessible way to examine the simulation's results.

## 7. Incorporating an Electrostatic Wave

Later in the project, I contacted plasma physicist Nathaniel Fisch, who recommended incorporating an electrostatic wave propagating in one azimuthal direction, with a phase velocity lower than the speed of a gyrating ion.

I implemented the wave to extend the simulator beyond its existing magnetic-field model. This introduced another physical field into the particle-motion calculations and gave me an opportunity to explore a research idea suggested by a physicist.

I do not remember the specific results I observed immediately after implementing the wave, so I cannot confidently describe a particular outcome. However, incorporating the recommendation expanded the scope of the model and connected my independent development process to an idea from an active area of plasma physics.

## 8. Current Limitations and Future Directions

The biggest limitation of my simulator is that it models individual charged particles rather than an actual plasma. Although I can investigate particle trajectories, magnetic-field structure, and the effects of modeled perturbations and electric fields, the simulator does not capture the collective behavior of a plasma as a whole.

My original goal was to model a plasma and investigate whether a tokamak with particular parameters could successfully confine it. Reaching that goal would require moving beyond individual-particle dynamics toward a model that accounts for collective plasma behavior.

Recognizing this gap has helped me understand both what I have accomplished and what remains to be done. The project has developed from a simple two-dimensional particle simulation into a more sophisticated computational tool for exploring magnetic geometry and charged-particle dynamics.

More importantly, the development process has taught me how to approach a scientific problem that initially exceeds my technical abilities: break it into smaller problems, build tools that make the physics more accessible, investigate unexpected questions, and use the results to decide what to explore next.
