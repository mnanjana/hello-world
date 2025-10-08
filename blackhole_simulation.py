#!/usr/bin/env python3
"""Toy black hole simulation toolkit."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

# Physical constants
G = 6.67430e-11  # m^3 kg^-1 s^-2
C = 299_792_458  # m s^-1
SOLAR_MASS = 1.98847e30  # kg


@dataclass
class SimulationConfig:
    mass_solar_masses: float
    initial_distance_km: float
    particle_mass_kg: float
    initial_velocity_kms: float
    time_step: float
    steps: int

    @classmethod
    def from_dict(cls, data: dict) -> "SimulationConfig":
        return cls(
            mass_solar_masses=float(data["mass_solar_masses"]),
            initial_distance_km=float(data["initial_distance_km"]),
            particle_mass_kg=float(data["particle_mass_kg"]),
            initial_velocity_kms=float(data["initial_velocity_kms"]),
            time_step=float(data["time_step"]),
            steps=int(data["steps"]),
        )

    @property
    def mass_kg(self) -> float:
        return self.mass_solar_masses * SOLAR_MASS

    @property
    def initial_distance_m(self) -> float:
        return self.initial_distance_km * 1_000

    @property
    def initial_velocity_ms(self) -> float:
        return self.initial_velocity_kms * 1_000


@dataclass
class SimulationState:
    time: float
    radius: float
    velocity: float
    tidal_force: float


class ToyBlackHoleSimulation:
    """Simple simulation of radial infall toward a Schwarzschild black hole."""

    def __init__(self, config: SimulationConfig):
        self.config = config
        self.event_horizon_radius = self._schwarzschild_radius(config.mass_kg)

    @staticmethod
    def _schwarzschild_radius(mass_kg: float) -> float:
        return 2 * G * mass_kg / (C ** 2)

    def tidal_force(self, radius: float) -> float:
        """Estimate tidal force per unit mass.

        Uses Newtonian approximation: F ~ 2GM/r^3 * delta r
        with delta r approximated as 1 meter.
        """
        delta_r = 1.0
        return 2 * G * self.config.mass_kg / (radius ** 3) * delta_r

    def simulate(self) -> List[SimulationState]:
        states: List[SimulationState] = []
        radius = self.config.initial_distance_m
        velocity = -abs(self.config.initial_velocity_ms)
        time = 0.0
        dt = self.config.time_step

        for _ in range(self.config.steps):
            if radius <= self.event_horizon_radius:
                radius = self.event_horizon_radius
                states.append(
                    SimulationState(
                        time=time,
                        radius=radius,
                        velocity=velocity,
                        tidal_force=self.tidal_force(radius),
                    )
                )
                break

            acceleration = -G * self.config.mass_kg / (radius ** 2)
            velocity += acceleration * dt
            radius += velocity * dt
            time += dt

            if radius <= self.event_horizon_radius:
                radius = self.event_horizon_radius
                states.append(
                    SimulationState(
                        time=time,
                        radius=radius,
                        velocity=velocity,
                        tidal_force=self.tidal_force(radius),
                    )
                )
                break

            states.append(
                SimulationState(
                    time=time,
                    radius=radius,
                    velocity=velocity,
                    tidal_force=self.tidal_force(radius),
                )
            )
        return states

    def metric_components(self, radius: float) -> tuple[float, float, float, float]:
        r_s = self.event_horizon_radius
        if radius <= r_s:
            raise ValueError("Metric components undefined inside event horizon in Schwarzschild coordinates")
        g_tt = -(1 - r_s / radius)
        g_rr = 1 / (1 - r_s / radius)
        g_thth = radius ** 2
        g_phph = (radius ** 2) * math.sin(math.pi / 2) ** 2
        return g_tt, g_rr, g_thth, g_phph


def load_config(path: Path) -> SimulationConfig:
    data = json.loads(path.read_text())
    return SimulationConfig.from_dict(data)


def format_states(states: Iterable[SimulationState]) -> str:
    header = f"{'time (s)':>10} | {'radius (km)':>12} | {'velocity (km/s)':>16} | {'tidal force (N/kg)':>20}"
    lines = [header, "-" * len(header)]
    for state in states:
        lines.append(
            f"{state.time:10.3f} | {state.radius / 1_000:12.3f} | {state.velocity / 1_000:16.3f} | {state.tidal_force:20.3e}"
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Toy black hole simulation toolkit")
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to the simulation configuration JSON file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    simulation = ToyBlackHoleSimulation(config)
    print("Toy Black Hole Simulation")
    print(f"Black hole mass: {config.mass_solar_masses} solar masses")
    print(f"Event horizon radius: {simulation.event_horizon_radius / 1_000:.3f} km")

    try:
        metric = simulation.metric_components(config.initial_distance_m)
    except ValueError as exc:
        metric = None
        print(f"Metric components unavailable: {exc}")
    else:
        labels = ("g_tt", "g_rr", "g_thth", "g_phph")
        print("Metric components at initial radius:")
        for label, component in zip(labels, metric):
            print(f"  {label}: {component:.6e}")

    states = simulation.simulate()
    print()
    print(format_states(states))


if __name__ == "__main__":
    main()
