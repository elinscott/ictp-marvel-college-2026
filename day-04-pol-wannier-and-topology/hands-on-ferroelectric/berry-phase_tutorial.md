
<div align="right">

**Joint ICTP MARVEL College: Materials simulations in the age of AI**  
Thursday, 4 June 2026

&nbsp;


</div>

<div align="center">

# Electric Polarization and Berry phases in ferroelectric $\text{PbTiO}_3$

</div>

> [!NOTE]  Hands-on based on QE-v7.4. 
>
>
> ### ***Tutors***:
> - Antimo Marrazzo
> - Riccardo Dal Molin 
> - Nicolas Baù
> - Ransell D'Souza
> - Mitra Dowlatabadi
---

## 1. Berry-phase polarization

In this exercise you will learn how to calculate the electric polarization and Born effective charges through the modern theory of polarization.

$$
P_{\alpha} = \frac{e}{\Omega} \left [ \sum_{I} Z_{I}s_{I,\alpha} - 2\frac{\bar{\gamma}_{\text{tot}}^{\kappa_{\alpha}}}{2 \pi} \right] \mathbf{a}_{\alpha} \quad \text{mod} \; \left(\frac{e \mathbf{a}_{\alpha}}{\Omega}\right) \;,
$$

We will consider $\text{PbTiO}_3$ a ferroelectric material with the highest spontaneous polarization among all the ferroelectric perovskites.


Go to the `es-1` folder, inspect the input file `scf.in` and visualize the crystal structure (e.g., with xcrysden or the Materials Cloud viewer).
How much is displaced the Pb atom from the center of the unit cell (e.g., in units of the lattice parameter)?

```fortran
&control
    calculation  = 'scf'
    restart_mode = 'from_scratch'
    pseudo_dir   = './pseudo/'
    outdir       = './out/'
/
&system
    ibrav=1
    celldm(1)=7.3699,
    nat=5
    ntyp=3
    nbnd=25
    ecutwfc=30.0
    occupations = 'fixed'
/
&electrons
    conv_thr = 1e-12,
    mixing_beta=0.3,
/
ATOMIC_SPECIES
  Pb   207.2      Pb.pz-d-van.UPF
  Ti    47.867    Ti.pz-sp-van_ak.UPF
  O     15.9994   O.pz-van_ak.UPF

ATOMIC_POSITIONS alat
  Pb    0.000    0.000    0.010
  Ti    0.500    0.500    0.500
  O     0.000    0.500    0.500
  O     0.500    0.500    0.000
  O     0.500    0.000    0.500

K_POINTS {automatic}
  4 4 4 1 1 1
```


 -  Run the SCF calculation with the command:

    ```bash
    pw.x < scf.in > scf.out
    ```
    Inspect the output file `scf.out` and check the convergence of the SCF calculation.

 - Inspect the input file `BP.in` :
    ```fortran
    &control
        calculation   = 'nscf'
        pseudo_dir    = './pseudo/'
        outdir        = './out/'
        lberry        = .true.
        gdir          = 3
        nppstr        = 7
    /
    &system
        ibrav         = 1
        celldm(1)     = 7.3699
        nat           = 5
        ntyp          = 3
        nbnd          = 22
        ecutwfc       = 30.0
        occupations   = 'fixed'
        degauss       = 0.00
    /
    &electrons
        conv_thr      = 1e-5
        mixing_beta   = 0.3
    /
    ATOMIC_SPECIES
    Pb   207.2      Pb.pz-d-van.UPF
    Ti    47.867    Ti.pz-sp-van_ak.UPF
    O     15.9994   O.pz-van_ak.UPF

    ATOMIC_POSITIONS alat
    Pb    0.000    0.000    0.010
    Ti    0.500    0.500    0.500
    O     0.000    0.500    0.500
    O     0.500    0.500    0.000
    O     0.500    0.000    0.500

    K_POINTS {automatic}
    4 4 7 1 1 1
    ```
 
    and run the non-self-consistent calculation with the command:

    ```bash
    pw.x < BP.in > BP.out
    ```

    This calculation will be used to calculate the Berry phase.

    Try to answer the following questions:
    - How many strings are being used in the calculations of the Berry phase?  
    - How many points are being used to sample each string?



 - Inspect the output file `BP.out`:
    - how many points and strings were effectively used to calculate the Berry phase?
    - Look at the ionic, electronic and total contributions to the polarization. What is the total polarization of $\text{PbTiO}_3$?


    - Both the ionic and electronic polarization are expressed modulo $2$, why?

---

## 2. Adiabatic evolution of the polarization

Consider a path connecting the centrosymmetric structure to a ferroelectric one where Pb is off-centered by a $12\%$ of the lattice parameter along the $z$ direction. 
In this exercise we will calculate the ionic, electronic and total contributions to the $P_z$ along this path.  

> [!TIP] 
>Go on the ``es-2/scripts`` folder and run ``make_scf.sh``. Inspect the generated scripts and run the scf calculation with ``run_all_scf.sh``.
>Create the input file for the nscf calulations (for Berry phase calculations) with ``make_scf.sh`` and run ``run_all_nscf.sh``.
>
>You can use  ``grep-P.sh`` to extract the total polarization form the output files. Inspect the ``polarization.dat`` file.

Try to answer the following questions:
  - Do you see any jump in the polarization? Can you explain why?
  - Can you find a way to remove the jump?
  - Check that the energy gap never closes during the adiabatic evolution of the polarization. Why is this important?

---

## 3. Born effective charges
In this esercise we will learn how compute the Born effective charges (BEC) via finite differences. The BEC can be defined as 

$$
Z^{*}_{\alpha \beta}(I) = \frac{\partial P_{\alpha}}{\partial u_{\beta}(I)}\;,
$$
where $u_{\beta}(I)$ is the displacement of the $I$-th atom along the $\beta$ direction and $P_{\alpha}$ is the polarization along the $\alpha$ direction.

Now, using the finite differences approach we can compute the BEC for the Pb atom as 
$$
Z^{*}_{\alpha \beta}(\text{Pb}) = \frac{P_{\alpha}(u(\text{Pb}))}{u_{\beta}(\text{Pb})}\;,
$$
where $P_{\alpha}(u(\text{Pb}))$ is the polarization calculated for a given displacement of the Pb atom along the $\beta$ direction respect the centrosimmetic positions.

Go to ``es-3/scripts`` folder and run the scripts as in the [previous exercise](#2-adiabatic-evolution-of-the-polarization) . Inspect the output files and answer the following questions:
 - Do we need to subtract the spontaneous polarization?
 - Compare the Born charge obtained from your calculations with the values reported in Ref. [^1] (table below). Are they consistent?

    | Material | Z\*(Pb) | Z\*(Ti) | Z\*₁(O) | Z\*₂(O) | Structure |
    |---|---:|---:|---:|---:|---|
    | PbTiO₃ | 3.90 | 7.06 | -5.83 | -2.56 | Cubic |
    | PbTiO₃ | 3.92 | 6.71 | -5.51 | -2.56 | Tetragonal |
 - Any idea on how to improve the accuracy of the BEC calculated with the finite differences approach?

---
## 4. Convergence tests (Optional)

Fix a value for the ferroelectric distortion (e.g., `0.05`) and calculate the polarization with different meshes of $k$-points and different number of strings.

- How does the polarization converge with $k$-point sampling?


<div align="right">
&nbsp;

&nbsp;
---
**Hands-on by Riccardo Dal Molin and Antimo Marrazzo**,

Thursday, 4 June 2026 - Trieste, Italy

</div>


[^1]: W. Zhong, R. D. King-Smith, and David Vanderbilt. Giant lo-to splittings in perovskite ferroelectrics. Phys. Rev. Lett., 72:3618–3621, May 1994. doi: 10.1103/PhysRevLett.72.3618.