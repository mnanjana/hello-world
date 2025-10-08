# Hello World Black Hole Simulation Toolkit

This repository contains a simple, fully self-contained Python toolkit for exploring a toy model of a Schwarzschild black hole. You can adjust parameters such as the black hole mass, starting distance, number of integration steps, and the initial velocity of an infalling test particle to see how they affect the event horizon radius, local tidal forces, and the particle trajectory.

## Repository structure

```
.
├── README.md
├── blackhole_simulation.py
└── configs
    └── default_blackhole_config.json
```

## Requirements

* Python 3.9 or newer.

No third-party dependencies are required beyond the Python standard library.

## Running the simulation

Use the provided configuration file to run the simulation:

```bash
python blackhole_simulation.py --config configs/default_blackhole_config.json
```

The script prints:

1. The black hole mass and the computed Schwarzschild radius (event horizon).
2. The metric coefficients (in Schwarzschild coordinates) at the initial radius.
3. A tabular summary of the simulated particle trajectory including time, radius, velocity, and estimated tidal force.

You can create additional configuration files to explore different scenarios. Each configuration parameter has the following meaning:

* `mass_solar_masses`: Black hole mass in solar masses.
* `initial_distance_km`: Initial radial distance of the test particle from the black hole (kilometres).
* `particle_mass_kg`: Mass of the test particle (kilograms). Only used for reporting tidal forces per unit mass.
* `initial_velocity_kms`: Initial radial velocity toward the black hole (kilometres per second). Positive values are automatically treated as inward velocities.
* `time_step`: Integration time step (seconds).
* `steps`: Number of integration steps to simulate.

## Viewing commits and files

All files described above are committed to this repository. To inspect the commit history locally you can run:

```bash
git log --oneline
```

To list the files included in the latest commit use:

```bash
git ls-tree --full-tree -r HEAD
```

If you are browsing the repository online (e.g., on GitHub), you can view the files directly in the web interface or open the **Commits** tab to see each commit and the files it introduced.
