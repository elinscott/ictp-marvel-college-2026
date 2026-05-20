# Exercise 2: Ionisation potential and electron affinity of ozone

**Tutors**: Nicola Colonna and Edward Linscott

In this exercise you will use the [`koopmans`](https://koopmans-functionals.org) package to compute the ionisation potential (IP) and electron affinity (EA) of the ozone molecule with the KI functional. The screening parameters will be calculated via the **ΔSCF** method.

## Files provided

- [`ozone.json`](ozone.json) — the input file for the calculation
- [`read.ipynb`](read.ipynb) — a small `jupyter` notebook that extracts the IP and EA from the `koopmans` output
- [`plot_spectrum.ipynb`](plot_spectrum.ipynb) — an incomplete `jupyter` notebook for plotting the orbital binding energies against experiment

## Problem 1: Understanding the input file

Open `ozone.json` and inspect the `workflow` block. You should see the following keys (among others):

```json
{
  "workflow": {
    "functional": "ki",
    "method": "dscf",
    "init_orbitals": "kohn-sham",
    "alpha_numsteps": 1,
    "pseudo_library": "SG15/1.2/PBE/SR"
  }
}
```

### Part A

What does each of `functional`, `method`, and `init_orbitals` control?

<details>
<summary><b>Solution</b></summary>

TODO

</details>

### Part B

Inspect the `atoms` block — what is the geometry of the system, and what does the `"periodic": false` flag mean? Why is the simulation cell so much larger than the molecule itself?

<details>
<summary><b>Solution</b></summary>

TODO

</details>

## Problem 2: Running the calculation

Run the workflow with

```bash
koopmans run ozone.json | tee ozone.md
```

When the calculation finishes, open `ozone.md`. This file is a human-readable outline of the workflow that `koopmans` just executed. (It is markdown, so it renders nicely in `vscode` and on GitHub.)

You should see that the workflow consists of three phases:

1. **Initialization** — preparing the density and variational orbitals.
2. **Calculating the screening parameters** — one $\alpha_i$ per orbital.
3. **The final KI calculation** — applying the corrections.

Identify the three phases in `ozone.md` and the calculation sub-directories they correspond to (all of them live under `01-koopmans-dscf/`).

<details>
<summary><b>Solution</b></summary>

TODO

</details>

## Problem 3: The initialization step

You should see that the initialization phase runs **four** separate PBE calculations, all under `01-koopmans-dscf/01-initialization/`:

```text
01-dft_init_nspin1
02-dft_init_nspin2_dummy
03-convert_files_from_spin1to2
04-dft_init_nspin2
```

Why not just run a single `nspin = 2` PBE calculation? (Hint: ozone is a closed-shell molecule. What could go wrong?)

> **Note**
>
> From this point onward in the workflow the density will not change. This is because the KI functional, by construction, gives back the same density as its base functional (here PBE). This is *not* true for KIPZ — there, the density does change.

<details>
<summary><b>Solution</b></summary>

TODO

</details>

## Problem 4: Calculating the screening parameters

The second phase of the workflow computes one screening parameter $\alpha_i$ per orbital, using the ΔSCF method (see the lecture).

These calculations live under `01-koopmans-dscf/02-calculate-screening-via-dscf/`, organised into one sub-directory per iteration of the screening loop (`01-iteration-1`, `02-iteration-2`, ...). Each iteration begins with a trial KI calculation (`01-ki`), followed by one sub-directory per orbital (`02-orbital-1`, `03-orbital-2`, ..., `11-orbital-10`).

For each *filled* orbital $i$ (orbitals 1–9 of ozone), the code performs a single constrained $N{-}1$-electron PBE calculation in which orbital $i$ is frozen and emptied while the remaining density is allowed to relax. This yields $E_i(N{-}1)$, which combined with $E(N)$, $\lambda_{ii}^\alpha(1)$, and $\lambda_{ii}^0(1)$ (all of which come from the trial KI calculation) is enough to update $\alpha_i$ from its initial guess of $\alpha_i^0 = 0.6$.

### Part A

Select an orbital. Based on the contents of `01-ki` and `??-orbital-?/01-dft_n-1`, calculate by hand the value of the screening parameter.

For the *empty* orbital 10, inside `01-iteration-1/11-orbital-10/` you will see three calculations rather than one:

```text
01-dft_n+1_dummy
02-pz_print
03-dft_n+1
```

The third of these is the constrained $N{+}1$-electron PBE calculation analogous to the $N{-}1$ ones for the filled orbitals. The first two contain preparatory calculations that assemble the files required by the third.

<details>
<summary><b>Solution</b></summary>

TODO

</details>

### Part B

At the end of the screening-parameters phase, `ozone.md` contains two tables. The first lists $\alpha_i$ for each iteration, and the second lists the residual $\Delta E_i - \lambda_{ii}^\alpha$ — the convergence criterion for the screening procedure. Inspect both. Do the residuals indicate that the screening parameters have converged? `koopmans` also prints a warning that the screening parameters are not necessarily self-consistent, and suggests increasing `alpha_numsteps` — which is exactly what you will do in Part C.

<details>
<summary><b>Solution</b></summary>

TODO

</details>

### Part C

In `ozone.json`, increase `alpha_numsteps` from `1` to `2` and re-run the workflow. Now the screening loop runs to self-consistency: each row of the $\alpha$ table is the input to the calculation in the next row. Convince yourself that the $\alpha_i$ values from the first iteration (which is what you got in Part B) are *not* self-consistent, but that the converged values now are.

<details>
<summary><b>Solution</b></summary>

TODO

</details>

## Problem 5: Extracting the IP and the EA

The KI ionisation potential is $-\varepsilon_\text{HOMO}$ from the final KI calculation, and likewise the electron affinity is $-\varepsilon_\text{LUMO}$.

### Part A

Open `01-koopmans-dscf/03-ki_final/ki_final.cpo` and locate the HOMO and LUMO eigenvalues. You should see something like

```text
HOMO Eigenvalue (eV)

  -12.5199

LUMO Eigenvalue (eV)

   -1.8218
```

Report the KI IP and EA of ozone.

<details>
<summary><b>Solution</b></summary>

TODO

</details>

### Part B

For comparison, dig out the corresponding PBE values from the final initialization calculation (`01-koopmans-dscf/01-initialization/04-dft_init_nspin2/04-dft_init_nspin2.cpo`).

<details>
<summary><b>Solution</b></summary>

TODO

</details>

### Part C

Compare your KI and PBE results against the experimental values for ozone:

- IP ≈ 12.5 eV[^NIST-O3]
- EA ≈ 2.1 eV

What do you conclude about the accuracy of semi-local DFT and of the KI functional for predicting charged excitations?

<details>
<summary><b>Solution</b></summary>

TODO

</details>

### Part D

If you prefer to work in `python`, you can use the `read.ipynb` notebook provided. It loads the `ozone.pkl` file generated by `koopmans` and prints the IP and EA. Open it, run all the cells, and check that you get the same numbers as in Part A.

<details>
<summary><b>Solution</b></summary>

TODO

</details>

## Problem 6: Comparing the full spectrum to experiment

So far you have only looked at the HOMO and LUMO. The KI functional in fact predicts a binding energy for *every* occupied orbital, and these can be compared directly against gas-phase photoemission spectroscopy.

The `plot_spectrum.ipynb` notebook contains experimental binding energies (in eV) for the nine occupied orbitals of ozone, taken from [*Chemical Physics Letters* **375**, 76 (2003)](https://doi.org/10.1016/S0009-2614(03)00818-2). There is one value per occupied orbital, ordered from the most tightly bound orbital to the HOMO; orbitals for which no reliable experimental value is available are marked as `np.nan`.

### Part A

Complete the `plot_spectrum.ipynb` notebook. It loads `ozone.pkl`, extracts both the KI and the PBE orbital eigenvalues, converts them into binding energies, and plots them against the experimental values. Open the notebook, fill in the cells marked `TODO`, and run all the cells to produce the comparison plot. The notebook also includes cells for inspecting `wf.calculations[-1].results`, which will help you work out where the eigenvalues are stored.

<details>
<summary><b>Solution</b></summary>

TODO

</details>

### Part B

How well do the KI binding energies agree with experiment across the *whole* spectrum, not just at the HOMO? How do they compare with the PBE binding energies? Are the deeper (more tightly bound) orbitals described as well as the frontier orbitals?

<details>
<summary><b>Solution</b></summary>

TODO

</details>

## Problem 7: Take-aways

A Koopmans calculation requires running many constrained DFT calculations — one per orbital (and even more for empty orbitals). What does this imply about how the cost of a ΔSCF Koopmans calculation scales with system size? What does it imply for *periodic* systems, where the variational orbitals are spread throughout the crystal and the supercell needs to be made large enough to host the constrained $N\pm1$ density?

The second exercise, on bulk ZnO, addresses exactly this issue by using a different — much more efficient — method for computing the screening parameters: density-functional perturbation theory (DFPT).

<details>
<summary><b>Solution</b></summary>

TODO

</details>

## Problem 8: Molecular oxygen [OPTIONAL]

Try modifying the input file from ozone to O₂, and see if you can get an ionization potential and electron affinity that compare well to experiment [^NIST-O2].

When writing your input file, remember...
- O₂ is a linear molecule with a bond length of 1.21 Å
- it is paramagnetic, so you will need to set `spin_polarized = true` in the `workflow` block
- change any other relevant parameters

<details>
<summary><b>Solution</b></summary>

Update...
- `spin_polarized = True`
- `tot_magnetization = 2`
- `nbnd = 8`

as well as the list of atoms and their coordinates.

</details>

[^NIST-O3]: [NIST Chemistry WebBook, SRD 69 — Ozone, ion energetics](https://webbook.nist.gov/cgi/cbook.cgi?ID=C10028156&Mask=20#Ion-Energetics).
[^NIST-O2]: [NIST Chemistry WebBook, SRD 69 — Molecular oxygen, ion energetics](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7782447&Mask=20#Ion-Energetics).
