# MD Course — Hands-on Sessions

**Tutors:** Edrick Solis Gonzalez, Federica Troni

---

## Session 1 — Basic LAMMPS & NVE simulation of an LJ system

**Goal.** Run NVE molecular dynamics simulations of a Lennard-Jones system with LAMMPS and sample several points on the LJ phase diagram (ρ, T).

### Getting started

To access the correct directory and environment, open a terminal and run:

```bash
cdd 6
```

### Step 1 — Open the input file

Explore the input file `in.nve`. LAMMPS documentation: <https://docs.lammps.org/Manual.html>

### Step 2 — Fill in the placeholders

Three `???` need a value to start:

- `variable rho equal ???` → density.
- `variable T0 equal ???` → initial temperature.
- `variable target_phase string ???` → a tag used as a suffix in every output filename.

### Step 3 — Run

```bash
lmp -in in.nve
```

### Step 4 — Explore the outputs

The `thermo_<phase>.dat` file contains some observables (temperature, total energy, potential and kinetic energy). The `*_<phase>.lammpstrj` files contain positions or velocities for each atom at every dumped time step.

### Step 5 — Sample the phase diagram

Look at the LJ (ρ, T) phase diagram — gas, liquid, gas+liquid, supercritical, solid_fcc, solid_hcp, solid+liquid, gas+solid — and:

1. **Choose** a target phase.
2. **Modify** `in.nve`: update `rho`, `T0`, and the `target_phase` suffix accordingly.
3. **Run** `lmp -in in.nve`.
4. **Separate** the equilibration from the production using the Jupyter notebook (introduced during the session, Exercise 0).
5. **Check:** does ⟨T⟩_prod correspond to your target phase? If not, go back to step 2.

Repeat for a few different phases — we'll compare results across the room.

**Reference:** LJ phase diagram on [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:LJ_PhaseDiagram.png).

---

## Session 2 — MSD, VACF, and g(r) in practice

**Goal.** Analyze the trajectories from Session 1: compute the mean-squared displacement (MSD), velocity autocorrelation function (VACF), and radial distribution function g(r), and connect each curve back to the phase you sampled.

> **Before you start**
> - If you're a beginner in Python, feel free to skip the coding part and think / discuss the points in the Jupyter notebook. At the end of each exercise there are open questions to discuss.
> - The tutors know the answers to the coding exercises and are very happy to help you out.
> - The answers will be given at the end of each exercise, so don't worry and give it a try!

### Setup

Open `MD_Analysis_template.ipynb`. It uses helper functions from `MD_utils.py` (`read_lammpstrj`, `plot_equilibration`). Throughout the notebook, replace every `???` with the appropriate value — most often your `target_phase` suffix in file names like `thermo_???.dat`, `unwrap_pos_???.lammpstrj`, `vels_???.lammpstrj`, `wrap_pos_???.lammpstrj`.

### Exercise 0 — Equilibration (Already done in Session 1)

Set `rho_lj`, plug your suffix into the file names, and pick `Nframes_eq` from the equilibration plot. Confirms ⟨T⟩_prod for the state point you sampled.

### Exercise 1 — MSD

Complete the function `compute_msd(unwrapped)` in the notebook, then plot MSD(t).

**Discuss with your nearest neighbors:**
- What shape of the MSD do you expect for different phases?
- With your current data, could you reduce the noise of the plot? Justify your answer.

### Exercise 2 — VACF

Complete the function `compute_vacf(vels)` in the notebook, then plot the VACF.

**Discuss with your nearest neighbors:**
- What shape would you expect for the VACF of a system in the solid, liquid, or gaseous state?
- What is the meaning of negative values of the VACF?
- What would a system look like if its VACF(τ) = 1?

### Exercise 3 — g(r)

Counting the pair distances is already implemented. You only need to **find the correct normalization** so that `g(r) = pair_distance_counts / normalization`.

**Discuss with your nearest neighbors:**
- Why does `pair_distance_counts` grow as ∝ r² at large r?
- With your current data, how would you count the typical number of atoms in the first coordination shell? And in the second?

### Appendix (optional) — Diffusion coefficient: compare with Rahman (1964)

Estimate the diffusion coefficient D from your data and compare it to Rahman's 1964 value for liquid Argon: **2.43 × 10⁻⁵ cm² s⁻¹** at (ρ\*, ⟨T⟩) = (0.814, 0.787).
