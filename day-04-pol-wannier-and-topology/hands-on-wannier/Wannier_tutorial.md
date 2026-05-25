
<div align="right">

**Joint ICTP MARVEL College: Materials simulations in the age of AI**  
Thursday, 4 June 2026

&nbsp;


</div>

<div align="center">

# Wannier interpolation of band structures: Hands-on session


</div>

**Tutors**: M. Dowlatabadi, A. Marrazzo, N. Baù, R. Dal Molin, R. D'Souza

**Time budget**: 1 hour and 15 minutes

Hands-on based on QE-v7.5 and Wannier90-v3.1.0

In this session you will learn how to build and use maximally-localized Wannier functions (MLWFs) with `Quantum ESPRESSO` and `Wannier90`. You will first interpolate the valence bands of silicon, then include conduction bands using disentanglement, and finally interpolate the band structure and Fermi surface of lead.

## Files provided

- `ex1/` — input files for silicon valence-band Wannierization.
- `ex2/` — files to create from `ex1/` for silicon valence-and-conduction-band Wannierization.
- `ex3/` — input files for lead Fermi-surface and band-structure interpolation.
- `pseudo/` — pseudopotentials required by the calculations.

---

## Problem 1: Silicon valence bands

In this exercise you will learn how to obtain MLWFs for the valence bands of silicon.

### Step 1

Go to the `ex1` folder and inspect the input file `01_scf.in`. The first step is to perform a ground-state calculation for a silicon crystal (FCC) with two atoms per unit cell. Check if you understand all parameters (you can use the web page <https://www.quantum-espresso.org/Doc/INPUT_PW.html> for keywords that you do not know). To visualize the crystal structure, there are two options, choose the one you prefer:

- `Quantum ESPRESSO input generator and structure visualizer`: open the following link in a browser,  
  <https://www.materialscloud.org/work/tools/qeinputgenerator>,  
  click `Choose File` button, select the `01_scf.in` file, and click "Generate the PWscf input file" button. In the new webpage you find a 3D visualization of the structure.

- `xcrysden` : either open the program, select from the menu `File → Open PWscf... → Open PWscf Input File` and then select the input file, or directly from the command line with the command `xcrysden --pwi 01_scf.in`.

### Step 2

The Si pseudopotential that we will use for the calculation has $Z_{val}=4$ (this information can be obtained by reading the first lines of the pseudopotential file, for instance with the command `less pseudo/Si.pbe-n-van.UPF`). Using the information given above, and knowing that FCC Si is a semiconductor, how many occupied valence bands do you expect (and why)?

<details>
<summary><strong> Solution</strong></summary>

Each Si atom contributes 4 valence electrons. 
Since the primitive cell contains 2 Si atoms, the total number of valence electrons is 8.
In a non-spin-polarized calculation, each band can accommodate 2 electrons, therefore, we expect **4 occupied valence bands**.

</details>

### Step 3

Run the ground-state calculation using the `pw.x` code from the `Quantum ESPRESSO`. The syntax for codes in the `Quantum ESPRESSO` is:

`command < inputfile > outputfile`

For example:

```bash
pw.x < 01_scf.in > scf.out
```
You can either:

- run it directly from the terminal without activating any environment, or
- activate the environment first using: `workon qe`

> **Note**
>
> If you activated the environment, you can deactivate it afterward with: `conda deactivate`
> 

### Step 4

After the calculation finishes, inspect the output file `scf.out` to check if there are any errors/warnings. Compare your answer to the previous point (number of electrons and occupied valence bands) with the information provided in the output file.

### Step 5

Now we want to plot the band structure of silicon (we will use this plot also for the next exercise, where we need also the conduction bands: therefore, we plot also a few of the lowest conduction bands). Copy the file `01_scf.in` to the file `02_bands.in`. Do the following modifications to the file `02_bands.in` (use the INPUT_PW documentation from the link above for an explanation of the meaning of the flags, if needed):

- In the `CONTROL` namelist, change the `calculation` keyword from `scf` to `bands` to perform a band structure calculation    starting from the ground state density obtained from the scf run.

- Ask the code to print 12 bands (flag `nbnd=12` in the `SYSTEM` namelist).

- Set `diago_full_acc = .true.` in the `ELECTRONS` namelist.

- Change the k-point list to plot the band structure along the following path (coordinates are given in crystal units), using 50 points per segment:

  - L$(0.5,0.5,0.5)\to\Gamma(0,0,0)$

  - $\Gamma(0,0,0)\to\mathrm{X}(0.5,0,0.5)$

  You can do this simply using the following `K_POINTS` card:

  ```text
  K_POINTS crystal_b
  3
  0.5 0.5 0.5 50 
  0. 0. 0. 50
  0.5 0. 0.5 50
  ```
### Step 6

Run the calculation using the `pw.x` code, as explained before.

### Step 7

When the calculation has finished, run the file `03_bandsx.in` through the `bands.x` executable (make sure to read and understand the input file): 
```bash
bands.x < 03_bandsx.in > bandsx.out
```
This will produce the `bands.dat` file.

### Step 8

Finally, execute the `plotband.x` code (interactively) and answer to its questions. In particular, the input file is the `bands.dat` file created in the previous step; call the xmgrace file `qebands.agr`. When asked, call the ps file `qebands.ps`. You will be asked to provide the value of the Fermi level, which in this case can be put equal to the highest occupied energy level (see the output file `scf.out`). When asked for the deltaE and reference E for the energy axis, type `2` and Fermi level (use space to separate the 2 numbers), you can also tweak these 2 numbers to adjust the visual output of the figure. At the end, open the xmgrace file (or directly the postscript PS file) and inspect the band structure, identifying the valence and conduction bands.

### Step 9

Now we are ready to calculate the wavefunctions on a complete grid of k-points. Copy the `02_bands.in` file that you created before to `04_nscf.in`, and modify the following:

- Change the `calculation` type from `bands` to `nscf`.

- Change the number of bands from 12 back to the number of valence bands, 4, since for this exercise we only need the valence bands.

- Change the k-point list to a full $4\times4\times4$ Monkhorst-Pack mesh, which will be used to calculate the overlap matrices needed to obtain Wannier functions. To obtain the list of k-points, use the `kmesh.pl` with the following command:
  ```bash
  perl ../kmesh.pl 4 4 4
  ```
  (use the command without parameters to get an explanation of its usage).
  
  > **Note**
  > 
  > In general, if you have installed `Wannier90` locally on your system, you can find `kmesh.pl` utility in the `utility` folder of   the `Wannier90` code: `wannier90/utility/`  
  >

### Step 10

Run the NSCF calculation using the `pw.x` code:

```bash  
mpirun -np 2 pw.x < 04_nscf.in > nscf.out
```

### Step 11

Now we have to prepare the input file for Wannier90. Open the file `ex1.win`, which is a template for the Wannier90 input file (note that Wannier90 input file must have the `.win` extension). Change the values marked with `XXX` inserting the correct values. In particular:

- Insert the `num_bands` value (this must be equal to the `nbnd` value set in the nscf calculation).

- Insert the `num_wann` value (this is the number of requested Wannier functions: in this case without disentanglement, this is equal to the `num_bands` value).

- Set the `mp_grid` value to `4 4 4` (since we are using a $4\times4\times4$ k-mesh).

- Insert, between the `begin kpoints` and `end kpoints` lines, the list of the 64 kpoints, one per line. Note that while `pw.x` requires four numbers per line (the three coordinates of each kpoint, and the weight), `Wannier90` needs only three numbers (the three coordinates). To obtain these lines, use again the `kmesh.pl` utility, but this time specifying a fourth parameter to get the list in the Wannier90 format:  
  ```bash
  perl ../kmesh.pl 4 4 4 wan
  ```  
  **Note**: Using the `kmesh.pl` utility, we are sure that we provide enough significant digits, and that the list of k-points given to `pw.x` and to `Wannier90` is the same.

- Inspect the remaining part of the input file, using the Wannier90 user guide (which can be found at <https://github.com/wannier-developers/wannier90/raw/v3.1.0/doc/compiled_docs/user_guide.pdf> page) for the input flags that you do not understand. Try to understand, in particular, the `projections` section. Can you identify where the four s-like orbitals are located with respect to the Si atoms?
  
### Step 12

Finally, we are ready to perform a Wannier90 calculation. This is done in three steps:

> **Note**
>
> For these steps, you can either activate the environment using `workon wannier` or run it directly from the terminal.
> 

1.  We first run a preprocessing step using the command `wannier90.x` : 
    
    ```bash
    wannier90.x -pp ex1
    ```
    which produces the `ex1.wout` and `ex1.nnkp` files, that contain the relevant information from the Wannier90 input file in a format to be used in the next step.

2.  Next, we run the `pw2wannier90.x` code (of the Quantum ESPRESSO distribution).  
    The input file for `pw2wannier90.x` is provided (file `05_pw2wan.in`). We are asking the code to calculate the overlap matrices $M_{mn}$ (that will be written in the `ex1.mmn` file) and the $A_{mn}$ matrices (file `ex1.amn`). Since we want to plot the Wannier functions in real space, we need also the $u_{nk}(r)$ wavefunctions on a real-space grid. We therefore also set the `write_unk` flag in `05_pw2wan.in`, that will produce a set of files with names `UNK00001.1`, `UNK00002.1`, ... Finally, the code will also produce a `ex1.eig` file, with the eigenvalues on the initial $4\times4\times4$ k-grid (**Note**: this is not needed to obtain the MLWFs of an insulator, but is required for the interpolation and band plotting routines). Note that the `pw2wannier90.x` expects to find the `ex1.nnkp` file produced in the previous step. Run the code using
    
    ```bash
    mpirun -np 2 pw2wannier90.x < 05_pw2wan.in > pw2wan.out
    ```

3.  Finally, we can run Wannier90 to obtain MLWFs. Execute
  
    ```bash  
    wannier90.x ex1
    ```
    and, when it finishes, inspect the output file, called `ex1.wout`.

    Check lines containing `<-- DLTA` to check for the convergence of the spread during the iterations.
   
    Check the lines after the string `Final state`: you find the centers and spreads of the maximally-localized Wannier functions.

### Step 13

To check if the obtained MLWFs are correct, one typically does the following checks:

- *Compare the Wannier-interpolated band structure with the ab-initio one*: the provided Wannier90 input file computes the interpolated band plot; you can try to compare the *ab-initio* band plot obtained in the steps before with the interpolated band structure (files `ex1_band.dat`, and `ex1_band.gnu`)

  - To plot it with `gnuplot`: run `gnuplot` in terminal, and in `gnuplot`, type
  
    ```text
    set xtics nomirr
    set x2tics
    set xrange [0:1.3195]
    set x2range [0:2.1721815]
    plot 'bands.dat.gnu' w p pt 7, 'ex1_band.dat' axes x2y1 w l
    ```
    **Note**: you can reuse the script in following exercises when comparing band structures, by replacing the file names `bands.dat.gnu` and `ex1_band.dat`.

  - Or plot it with `xmgrace`: in terminal, type:  
    ```bash
    xmgrace qebands.agr ex1_band.dat
    ```  
    Note that you may need to rescale the x axis.

- *Plot the real-space Wannier functions and check if they are real*: if you ask `Wannier90` to plot the Wannier functions, it will print also the ratio of the imaginary and real part of each of them at the end of the `ex1.wout` file: check that the value is small.

### Step 14

Plot one of the Wannier functions, which are stored in the files `ex1_00001.xsf, ...`. To visualize Wannier functions, we use `xcrysden`, open the `xsf` file, then choose `Tools → Data Grid → OK`, and then choose a reasonable `isovalue`, activate the `Render +/- isovalue` flag, and press `Submit`.

## Problem 2: Silicon valence and conduction bands

While in exercise 1 we obtained a Wannier-interpolated band structure for the occupied bands only, now we will see how to obtain an interpolated band structure for the conduction bands.

### Step 1

Copy the entire `ex1` folder to a new folder named `ex2`. The first step, i.e. the SCF calculation (`01_scf.in`), is identical. Hence, if you copied also the out directory, you don’t need to rerun it.

### Step 2

In the `04_nscf.in` file, change the value of `nbnd` to 12 to calculate the eigenenergies and wavefunctions for 12 bands, and run the NSCF calculation (using `pw.x` as in the previous exercise).

### Step 3

Rename `ex1`.win to `ex2`.win, and modify the following flags:

- Change `num_bands` to 12 to be consistent with the new NSCF run.

- Change the projections to sp$^{3}$ orbitals for each Si atom in the unit cell: to do this, the projections section should read:

```text
begin projections
Si:sp3
end projections
```
- Change the `num_wann` keyword to the correct number of Wannier functions: how many do we want, according to the projections list given above?

  <details>
  <summary><strong> Solution</strong></summary>
  
  Each Si atom has four sp$^{3}$-like orbitals. Since the primitive cell contains 2 Si atoms, the total number of Wannier functions is 8.
  
  </details>

- Set the maximum energy for the frozen window (flag `dis_froz_max`) inside the energy gap (use the band plot obtained in exercise 1 to get a value for this flag).

- Set the maximum energy for the disentanglement (flag `dis_win_max`) to an energy large enough so as to contain enough bands for each k point; 17.0 eV should be a reasonable value (check where this value lies in the band plot).

### Step 4

In the file `05_pw2wan.in`, change the seedname to `ex2` to reflect the new name of the `.win` file.

### Step 5

Run 

```bash
wannier90.x -pp ex2
```

### Step 6

Run `pw2wannier90.x` using `05_pw2wan.in` as the input file.

### Step 7

Run 

```bash
wannier90.x ex2
```

### Step 8

Check the output:

- Before the start of the Wannierization iterations, there is a new section (containing the string `<--DIS`) with the iterations of the disentanglement procedure. It is important that at the end of this section the convergence is achieved (with a string `<<< Disentanglement convergence criteria satisfied >>>`).

- A practical note: Especially when using disentanglement, it is possible that the disentanglement convergence is not achieved, and/or that the obtained Wannier functions are not real, and/or that the interpolated band structure differs significantly from the *ab-initio* one within the frozen window. In that case, you may need to change/tune the number of Wannier functions, the projections you chose and/or the energy values for the frozen and disentanglement windows, until you obtain well-localized and physically meaningful Wannier functions.

### Step 9

Check final WF centers and verify that WFs are real; you may also want to plot the Wannier functions, or compare the interpolated band structure with the *ab-initio* one (obtained in exercise 1).

### Step 10

**Optional (do this only if you have enough time):** Do the symmetry and the centers of the Wannier functions agree with your intuition? (We would like 4 sp$^{3}$-like orbitals centered on each Si atom, with similar spreads). Try to rerun everything with a $6\times6\times6$ kgrid for the `nscf` and `wannier90` step to check if the results improve, and how the spreads change with respect to the grid density?

## Problem 3: Lead Fermi surface and band structure

In this exercise we will interpolate the band structure of lead, focusing in particular on the states around the Fermi energy. The first goal is to obtain the Fermi surface using Wannier interpolation. This will clearly show one of the advantages of Wannier-interpolation techniques compared to direct *ab-initio* calculations on very dense k-point grids. 

To construct a MLWF model for the bands around the Fermi level, we first need to identify the orbital character of the bands we are interested in. The crystal structure of pure lead has one atom per primitive cell, and since we also want to describe some states above the Fermi energy, we include five $d$ orbitals ($d_{xy}, d_{xz}, d_{yz}, d_{z^2}$ and $d_{x^2-y^2}$), and four $sp^3$ orbitals. Hence our guess for the projections is

- 5 $d$ orbitals centered on the Pb atom

- 4 $sp^3$ orbitals centred on the Pb atom

Now we are ready to obtain MLWFs and describe the states of Pb around the Fermi-level.

Go to folder `ex3`


### Step 1

Run `pw.x` to obtain the ground state of Pb

```bash
mpirun -np 2 pw.x < 01_scf.in > scf.out
```

### Step 2

Run `pw.x` to compute the Bloch states on a uniform k-point grid

```bash
mpirun -np 2 pw.x < 04_nscf.in > nscf.out
```
### Step 3

Run `wannier90.x` to generate the list of the required overlaps (written into the `ex3.nnkp` file).

```bash
wannier90.x -pp ex3
```

### Step 4

Run `pw2wannier90.x` to compute the overlap between Bloch states and the projections for the starting guess (written in the `ex3.mmn` and `ex3.amn` files).

```bash
mpirun -np 2 pw2wannier90.x < 05_pw2wan.in > pw2wan.out
```

### Step 5

Run `wannier90.x` to compute the MLWFs.

```bash
wannier90.x ex3
```

Inspect the output file `ex3.wout`.

### Step 6

Use Wannier interpolation to obtain the Fermi surface of lead. Rather than re-running the whole calculation we can use the unitary transformations obtained in the first calculation and restart directly from the plotting routines. Add the following keywords to the `ex3.win` file:

```text
restart = plot  
fermi_energy = [insert your value here]  
fermi_surface_plot = true  
```
and re-run `wannier90`. The value of the Fermi energy can be obtained from the output of the initial first principles calculation. `wannier90` calculates the band energies, through Wannier interpolation, on a dense mesh of k-points in the Brillouin zone. The density of this grid is controlled by the keyword `fermi_surface_num_points`. The default value is 50 (i.e., 50$^3$ points). The Fermi surface file `ex3.bxsf` can be viewed using `XCrySDen`, e.g.,

```bash
xcrysden --bxsf ex3.bxsf
```

### Step 7

Plot the interpolated band structure by rerunning `wannier90.x` after adding the following lines to `ex3.win`: 

```text
bands_plot = true

begin kpoint_path
G 0.00  0.00  0.00    X 0.50  0.50  0.00
X 0.50  0.50  0.00    W 0.50  0.75  0.25
W 0.50  0.75  0.25    L 0.00  0.50  0.00
L 0.00  0.50  0.00    G 0.00  0.00  0.00
G 0.00  0.00  0.00    K 0.00  0.50 -0.50
end kpoint_path
```

### Further ideas (if you have time)

- Compare the Wannier interpolated band structure with the full `pw.x` band structure. 
  
- Obtain MLWFs using a denser k-point grid.

- Investigate the effects of the outer and inner energy windows on the interpolated bands.

- Instead of extracting a subspace of $d+sp^3$ states, we could extract a different nine dimensional space (i.e., with $s$, $p$ and $d$ character). Examine this case and compare the interpolated band structures.

- Remove the low-energy $d$ states from the wannierization (hint: use the `exclude_bands` option in the Wannier90 input file) and compare both the spread and band structure you obtain.

