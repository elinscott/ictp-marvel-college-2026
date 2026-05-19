# Ozone KI Calculation: Finding the Optimal Screening Parameter alpha

In this exercise, you will perform a Koopmans-compliant KI calculation for ozone.

The goal is to determine the optimal value of the screening parameter alpha and then prepare the final KI input file yourself.

------------------------------------------------------------
GOAL
------------------------------------------------------------

You will:

1. Run a DFT calculation for the neutral N-electron system
2. Restart from the DFT orbitals and run a DFT calculation for the N-1 system
3. Run a KI calculation using a trial value of alpha
4. Use the formula discussed in class, implemented in get_alpha.sh, to compute the optimal alpha
5. Prepare and run the final KI calculation using the optimal value of alpha

------------------------------------------------------------
1. SET UP THE ENVIRONMENT
------------------------------------------------------------

Make sure the Koopmans executable is available in your path:

`export PATH=$PATH:/home/nicola/CODES/koopmans/bin/`

Check that kcp.x is found:

`which kcp.x`

------------------------------------------------------------
2. RUN THE DFT CALCULATION FOR THE NEUTRAL SYSTEM
------------------------------------------------------------

Run the DFT calculation for the N-electron ozone molecule:

`mpirun -np 2 kcp.x -in ozone_dft.in > ozone_dft.out`

Check that the calculation completed successfully before continuing.

------------------------------------------------------------
3. SET THE KS STATES AS VARIATIONAL ORBITALS
------------------------------------------------------------

After the neutral DFT calculation, copy the Kohn-Sham orbitals so that they can be used as the initial variational orbitals:

```
cp TMP/kc_90.save/K00001/evc1.dat TMP/kc_90.save/K00001/evc01.dat
cp TMP/kc_90.save/K00001/evc2.dat TMP/kc_90.save/K00001/evc02.dat
cp TMP/kc_90.save/K00001/evc_empty1.dat TMP/kc_90.save/K00001/evc0_empty1.dat
cp TMP/kc_90.save/K00001/evc_empty2.dat TMP/kc_90.save/K00001/evc0_empty2.dat
``` 

------------------------------------------------------------
4. RUN THE DFT CALCULATION FOR THE N-1 SYSTEM
------------------------------------------------------------

Now run the DFT calculation for the charged system:

`mpirun -np 2 kcp.x -in ozone_dft_n-1.in > ozone_dft_n-1.out`

Again, make sure the calculation finishes correctly.

------------------------------------------------------------
5. RUN A KI CALCULATION WITH A TRIAL VALUE OF ALPHA
------------------------------------------------------------

Choose a trial value for the screening parameter. In this exercise, use:

alpha0=0.7

Prepare the KI input file `ozone_ki.in` using:

```
&NKSIC
   nkscalfact       = 0.7
   which_orbdep     = 'nki'
   do_innerloop     = .false.
   esic_conv_thr    = 1.8000000000000002e-08
   do_innerloop_empty = .false.
/
```

Then run:

`mpirun -np 2 kcp.x -in ozone_ki.in > ozone_ki.out`

------------------------------------------------------------
6. COMPUTE THE OPTIMAL VALUE OF ALPHA
------------------------------------------------------------

Use the fact that the KI eigenvalue is linear in `alpha` to find the optimal value of `alpha` such that `epsilon^{KI}(alpha_opt) = E^{DFT}[N-1]-E^{DFT}[N]` 

Verify you get the correct value by running the script `get_alpha.sh`:

`sh get_alpha.sh`

The scipt automatically applies the formula discussed during the lecture to extract the optimal screening parameter from the DFT and trial-KI calculations.

You can store the value in a shell variable with:

`alpha=$(sh get_alpha.sh | tail -1)`

Print the value with:

`echo "optimal alpha = $alpha"`

------------------------------------------------------------
7. PREPARE THE FINAL KI CALCULATION
------------------------------------------------------------

Create a new input file called:

`ozone_ki_opt.in`

This file should be the same as `ozone_ki.in`, except that:

ndr = 90
ndw = 92

and the value of `nkscalfact` must be replaced by the optimal value of alpha:

```
&NKSIC
   nkscalfact       = <optimal_alpha>
   which_orbdep     = 'nki'
   do_innerloop     = .false.
   esic_conv_thr    = 1.8000000000000002e-08
   do_innerloop_empty = .false.
/
```
Replace `<optimal_alpha>` with the value obtained in Step 6.

------------------------------------------------------------
8. RUN THE FINAL KI CALCULATION
------------------------------------------------------------

Run:

`mpirun -np 2 kcp.x -in ozone_ki_opt.in > ozone_ki_opt.out`

This is the final KI calculation at the optimal value of the screening parameter.


