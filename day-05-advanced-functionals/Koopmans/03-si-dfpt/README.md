# Exercise 3: Band structure of bulk Si with KI and DFPT

**Tutors**: Nicola Colonna and Edward Linscott

In this exercise you will compute the KI band structure of bulk silicon. There are two important differences with the ozone calculation of Exercise 2:

1. **The variational orbitals are now maximally-localised Wannier functions (MLWFs)** instead of Kohn–Sham orbitals.
2. **The screening parameters are computed via DFPT** instead of via constrained ΔSCF calculations in a supercell.

This exercise is adapted from the `koopmans` documentation.

> **Note**
>
> Unlike a ΔSCF calculation, the DFPT screening for silicon is cheap enough to run live during this session: it is performed by linear response in the primitive cell, here on a coarse `dfpt_coarse_grid` of `[2, 2, 2]`. The screening parameters are therefore computed on the fly rather than supplied in advance.

## Files provided

- `si.json` — the input file for the calculation
- `plot_bandstructures.py` — a `python` script to plot the LDA and KI band structures side by side

## Problem 1: Understanding the input file

Open `si.json` and locate the `workflow` block:

```json
{
  "workflow": {
    "task": "singlepoint",
    "functional": "ki",
    "method": "dfpt",
    "init_orbitals": "mlwfs",
    "alpha_guess": 0.077,
    "orbital_groups_spread_tol": 0.01,
    "mp_correction": false,
    "pseudo_library": "PseudoDojo/0.4/LDA/SR/standard/upf",
    "calculate_bands": true,
    "dfpt_coarse_grid": [2, 2, 2]
  }
}
```

### Part A

Compare this block against the one from Exercise 2. Identify and explain each difference:

- `task: singlepoint` (we'll change this in Problems 2 and 3)
- `method: dfpt` instead of `dscf`
- `init_orbitals: mlwfs` instead of `kohn-sham`
- `alpha_guess` (a single starting value, refined by the DFPT screening) instead of `alpha_numsteps`
- `orbital_groups_spread_tol` — a tolerance for grouping orbitals
- `mp_correction`
- the LDA pseudopotential library (so this is KI@LDA) instead of the PBE one
- `dfpt_coarse_grid` and `calculate_bands`

### Part B

`mp_correction` toggles the *Makov–Payne* finite-size correction, which accounts for the spurious electrostatic interaction of a charged simulation cell with its periodic images. Why does the DFPT approach — which computes the screening by linear response in the primitive cell — not need this correction, so that it can be set to `false`?

### Part C

Inspect the `calculator_parameters.w90` block. The projections are split into two sub-lists (so-called "blocks") of `sp3` orbitals. Why are the occupied (bonding) and empty (antibonding) manifolds Wannierized in separate blocks?

## Problem 2: The Wannierization

Before doing any Koopmans physics, we need a good set of Wannier functions. Whether they are "good" depends on whether the band structure they interpolate matches the explicit DFT band structure.

### Part A

Change `"task": "singlepoint"` to `"task": "wannierize"` in `si.json`, then run

```bash
koopmans run si.json | tee si_wannierize.md
```

This task performs an SCF calculation, an NSCF calculation, a Wannierization of each block of bands, and then an explicit DFT band-structure calculation on the same _**k**_-path for comparison. The workflow generates a plot `si_bandstructure.png` that overlays the interpolated and the explicit band structures.

### Part B

Inspect `si_bandstructure.png`. Do the interpolated bands lie on top of the explicit ones? If not, where do the largest discrepancies appear, and in which energy window?

### Part C

The Wannierization of the empty (antibonding) manifold uses two **disentanglement** keywords, which you can find in the `w90` block of `si.json`:

```json
"dis_froz_max": 10.6,
"dis_win_max": 16.9
```

`dis_win_max` is the upper bound of the disentanglement window (within which Bloch states are mixed to construct the Wannier functions); `dis_froz_max` is the upper bound of the frozen window (within which the Bloch states are *exactly* preserved). Try varying these values by ±1 eV and see how the interpolated band structure changes.

> **Tip**
>
> When you run the same workflow more than once, `koopmans` will reuse intermediate results from previous runs by default. If you want to start from scratch, set `"from_scratch": true` in the `engine` block of `si.json`.

## Problem 3: Running the KI calculation

Now change `"task"` back to `"singlepoint"` and re-run

```bash
koopmans run si.json | tee si_ki.md
```

This time the workflow proceeds beyond the Wannierization to actually compute the KI band structure. Open `si_ki.md` and identify the following steps:

- a **Wannierization** block (the same one you just ran),
- a **`wann2kc`** step, which converts the Wannier90 files into a format readable by `kcw.x`,
- a **`screen`** step, in which the screening parameters $\alpha_i$ are computed via DFPT,
- a **`ham`** step, which constructs the Koopmans Hamiltonian,
- an **`unfold and interpolate`** step, which produces the final band structure.

### Part A

Contrast this workflow with the one you saw for ozone. In the DFPT workflow, where does the cost of computing the screening parameters go? Why is this expected to scale much better with system size than ΔSCF?

### Part B

What is the role of `wann2kc`? Why is this conversion step needed when going from a Wannier90 output to a Koopmans calculation?

## Problem 4: Plotting and analysing the band structure

The `singlepoint` task generates `si_bandstructure.png` automatically. For a more comprehensive plot, run

```bash
python plot_bandstructures.py
```

This produces `si_bandstructures.png`, comparing the LDA band structure against the KI@LDA one and labelling the band gap.

### Part A

Inspect `si_bandstructures.png`. What is the KI@LDA band gap? Compare it against

- the LDA band gap (read off the same plot),
- the experimental gap of 1.17 eV[^Madelung2004]. Our calculation is for a static lattice (it neglects electron–phonon coupling), so the fair comparison is against the experimental value with the zero-point renormalisation of 0.06 eV[^Miglio2020] added back — i.e. **1.23 eV**.
- and the KI@LDA result of ‹REFERENCE KI@LDA Si GAP — please provide› eV from Nguyen *et al.* (2018)[^Nguyen2018].

### Part B

The KI calculation does not change the *shape* of the LDA band structure dramatically — it primarily acts as a *scissor* that opens up the gap. Looking at the bands away from the gap, can you identify any features that *are* modified beyond a rigid shift?

### Part C

By construction, the Koopmans correction depends on the screening parameter $\alpha_i$ of each orbital — orbitals with $\alpha_i$ close to 1 are corrected strongly, while orbitals with $\alpha_i$ close to 0 are barely shifted. Inspect the screening parameters that were computed in `si_ki.md`. They are much smaller than the values you saw for ozone — what does this tell you about how strongly the electrons in a covalent semiconductor like silicon screen the Koopmans correction?

## Problem 5: Take-aways

### Part A

Summarise the differences between Exercise 2 (ozone, ΔSCF, KS orbitals) and Exercise 3 (Si, DFPT, Wannier orbitals). For each difference, explain *why* the choice is appropriate to the system.

### Part B

In both exercises we obtained agreement with experiment for a charged-excitation property (IP/EA for ozone; band gap for Si), starting from a semi-local DFT functional that on its own gives the wrong answer by several eV. What is the physical content of the screening parameters $\alpha_i$, and why does enforcing the Koopmans condition fix the eigenvalues so dramatically?

[^Nguyen2018]: N. L. Nguyen, N. Colonna, A. Ferretti, and N. Marzari, *Koopmans-Compliant Spectral Functionals for Extended Systems*, Phys. Rev. X **8**, 021051 (2018). [doi:10.1103/PhysRevX.8.021051](https://doi.org/10.1103/PhysRevX.8.021051).
[^Madelung2004]: O. Madelung, *Semiconductors*, 3rd ed. (Springer-Verlag, Berlin, 2004).
[^Miglio2020]: A. Miglio, V. Brousseau-Couture, E. Godbout, G. Antonius, Y.-H. Chan, S. G. Louie, M. Côté, M. Giantomassi, and X. Gonze, *Predominance of Non-Adiabatic Effects in Zero-Point Renormalization of the Electronic Band Gap*, npj Comput. Mater. **6**, 1–8 (2020). [doi:10.1038/s41524-020-00434-z](https://doi.org/10.1038/s41524-020-00434-z).
