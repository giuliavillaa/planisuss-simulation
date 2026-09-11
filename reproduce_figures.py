"""
Reproduce the figures shown in README.md.

Runs the simulation head-less (no Tkinter, no matplotlib window) with a fixed
random seed, then writes two plots to figures/.

Usage:
    python reproduce_figures.py            # seed 1, default parameters
    python reproduce_figures.py --seed 3
    python reproduce_figures.py --seeds 1 2 3 4 5 --summary-only
"""

from __future__ import annotations

import argparse
import os
import random

import matplotlib

matplotlib.use("Agg")  # head-less backend: no window is opened
import matplotlib.pyplot as plt

from game_manager import GameManager

FIGURES_DIR = "figures"
MAX_DAYS = 1000


def run(seed: int, max_days: int = MAX_DAYS) -> dict:
    """Run one simulation to extinction (or max_days) and return its history."""
    random.seed(seed)
    manager = GameManager()
    manager.initialize_world()

    for _ in range(max_days):
        if not manager.simulate_one_day():
            break

    return manager.history


def summarise(seed: int, history: dict) -> str:
    """One-line summary of a run."""
    days = len(history["time"])
    carviz = history["Carviz"]
    first_zero = next((i + 1 for i, v in enumerate(carviz) if v == 0), None)
    return (
        f"seed {seed}: {days} days simulated | "
        f"Carviz peak {max(carviz)}, extinct on day {first_zero} | "
        f"Erbast peak {max(history['Erbast'])}, final {history['Erbast'][-1]}"
    )


def plot_population_dynamics(history: dict, seed: int) -> str:
    """Populations of both species and mean vegetation density over time."""
    days = range(1, len(history["time"]) + 1)

    fig, ax_pop = plt.subplots(figsize=(9, 4.5))
    ax_pop.plot(days, history["Erbast"], color="#2E7D32", lw=1.6,
                label="Erbast (herbivores)")
    ax_pop.plot(days, history["Carviz"], color="#C62828", lw=1.6,
                label="Carviz (predators)")
    ax_pop.set_xlabel("Day")
    ax_pop.set_ylabel("Population")
    ax_pop.set_ylim(top=max(history["Erbast"]) * 1.22)
    ax_pop.grid(alpha=0.25)

    ax_veg = ax_pop.twinx()
    ax_veg.plot(days, history["avg_Vegetob"], color="#F9A825", lw=1.2, ls="--",
                label="Vegetob density (mean)")
    ax_veg.set_ylabel("Mean Vegetob density")

    handles = ax_pop.get_lines() + ax_veg.get_lines()
    ax_pop.legend(handles, [h.get_label() for h in handles],
                  loc="upper right", fontsize=9, framealpha=0.9)
    ax_pop.set_title(
        f"Planisuss \u2014 population dynamics (seed {seed}, default parameters)"
    )

    path = os.path.join(FIGURES_DIR, "population_dynamics.png")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def plot_phase_portrait(history: dict) -> str:
    """Herbivore population against vegetation density, coloured by day."""
    days = range(1, len(history["time"]) + 1)

    fig, ax = plt.subplots(figsize=(5.6, 5))
    points = ax.scatter(history["avg_Vegetob"], history["Erbast"],
                        c=list(days), cmap="viridis", s=7)
    ax.set_xlabel("Mean Vegetob density")
    ax.set_ylabel("Erbast population")
    ax.set_title("Phase portrait: herbivores vs vegetation")
    ax.grid(alpha=0.25)
    plt.colorbar(points, label="Day")

    path = os.path.join(FIGURES_DIR, "phase_portrait.png")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=1,
                        help="seed used for the plotted run (default: 1)")
    parser.add_argument("--seeds", type=int, nargs="+",
                        help="extra seeds to run for the printed summary")
    parser.add_argument("--summary-only", action="store_true",
                        help="print run summaries without writing figures")
    args = parser.parse_args()

    os.makedirs(FIGURES_DIR, exist_ok=True)

    history = run(args.seed)
    print(summarise(args.seed, history))

    if not args.summary_only:
        print("wrote", plot_population_dynamics(history, args.seed))
        print("wrote", plot_phase_portrait(history))

    for seed in args.seeds or []:
        if seed != args.seed:
            print(summarise(seed, run(seed)))


if __name__ == "__main__":
    main()
