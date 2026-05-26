# Silicon cDFPT Tutorial

This tutorial introduces the use of constrained DFT (cDFT) and constraint Density-Functional Perturbation Theory (cDFPT) for studying the electronic and vibrational properties of silicon under modified electronic occupations.

The workflow is based on calculations performed with the Quantum ESPRESSO suite and is organized as a sequence of ground-state, excited-state, band-structure, and phonon calculations.

---

## Learning goals

By completing this tutorial, participants will learn how to:

- perform structural relaxation calculations for excited silicon;
- compare ground-state and excited-state structural and electronic properties;
- explore the effect of modified electronic occupations on phonon properties;
- organize and analyze workflows for excited-state lattice dynamics.

---

## Software requirements

The tutorial requires:

- Quantum ESPRESSO (`pw.x`, `ph.x`, `bands.x`)
- A plotting tool such as `gnuplot` and `xmgrace`

---

## Tutorial workflow

### 1. Ground-state structural relaxation

The folder `PW_Si_GS/` contains a variable-cell relaxation calculation for bulk silicon.

Run:

```bash
cd PW_Si_GS
bash run_vc-relax_gs
```

Input file:

- `vc-relax.in`

Main output:

- `vc-relax.out`

This calculation determines the equilibrium lattice parameter and relaxed crystal structure.

---

### 2. Excited-state structural relaxation

The folder `PW_Si_Excited/` contains a relaxation calculation using modified electronic occupations.

Run:

```bash
cd PW_Si_Excited
bash run_vc-relax_exc
```

Input file:

- `vc-relax_twochem.in`

Main output:

- `vc-relax_twochem.out`

This setup illustrates how constrained occupations can be used to simulate electronically excited configurations.

---

### 3. Ground-state electronic band structure

The folder `PW_Si_Bands_GS/` contains:

1. a self-consistent field (SCF) calculation;
2. a non-self-consistent field (NSCF) calculation along high-symmetry k-points;
3. a band interpolation/post-processing step.

Run:

```bash
cd PW_Si_Bands_GS
bash run_bands_GS
```

Main input files:

- `scf.in`
- `nscf.in`
- `bands.in`

Outputs include:

- `si_bands.dat`
- `si_bands.dat.gnu`
- `Si_bands_GS.png`

Participants can analyze the electronic structure and identify the indirect band gap of silicon.

---

### 4. Excited-state electronic band structure

The folder `PW_Si_Bands_Excited/` repeats the band-structure workflow using constrained occupations.

Run:

```bash
cd PW_Si_Bands_Excited
bash run_bands_Excited
```

Main input files:

- `scf_twochem.in`
- `nscf_twochem.in`
- `bands.in`

Outputs include:

- `si_bands.dat`
- `si_bands.dat.gnu`
- `Si_bands_twochem.png`

The resulting band structure can be compared with the ground-state calculation to observe changes induced by the modified electronic occupations.

---

### 5. Ground-state phonon calculations

The folder `PH_Si_GS/` contains DFPT phonon calculations.

Run:

```bash
cd PH_Si_GS
bash run_ph_GS
```

Main input files:

- `scf.in`
- `ph.in`

Outputs include:

- `ph.out`
- `dynq1`

These calculations provide the phonon dynamical matrix at the gamma point for silicon in its ground state.

---

### 6. Excited-state phonon calculations

The folder `PH_Si_Excited/` contains DFPT calculations performed with constrained occupations.

Run:

```bash
cd PH_Si_Excited
bash run_ph_Excited
```

Main input files:

- `scf_twochem.in`
- `ph_twochem.in`

Outputs include:

- `ph_twochem.out`
- `dynq1`

This workflow demonstrates how phonon properties can change under electronically excited conditions.

---

## Suggested exercises

1. Compare relaxed lattice parameters between the ground and excited states.
2. Compare the electronic band structures obtained in the two occupation regimes.
3. Inspect the occupation settings in the input files.
4. Analyze changes in phonon frequencies between the ground-state and constrained calculations.
5. Explore the role of electronic screening in lattice dynamics.

---

