#!/usr/bin/env bash
# ============================================================
# Script code  for MARVEL-2026 by Riccardo Dal Molin rdalmoli@sissa.it
#
# Generate N QE inputs nscf for berry phase calculations
#
# Assumptions:
#   - input file: scf_*.in
#   - ATOMIC_POSITIONS alat
#   - P computed along z
#   - k point along 3rd gvec = 6 
# Output:
#   nscf_000_berry.in
#   ...
#   nscf_012_berry.in
#
# ============================================================
cd ../
set -e

echo "Generating NSCF Berry-phase inputs..."

for scf in scf_*.in; do

    base=${scf%.in}
    nscf="n${base}_berry.in"

    echo " -> $nscf"

    awk '

    BEGIN{
        in_electrons=0
        done_control=0
    }

    # ----------------------------------------
    # CONTROL SECTION
    # ----------------------------------------

    /calculation[[:space:]]*=/ {
        print "    calculation   = '\''nscf'\'',"
        next
    }

    /outdir[[:space:]]*=/ {
        print
        next
    }

    /^\s*\/\s*$/ && done_control==0 {
        print "    lberry        = .true."
        print "    gdir          = 3"
        print "    nppstr        = 6"
        done_control=1
        print
        next
    }

    # ----------------------------------------
    # remove smearing stuff
    # ----------------------------------------

    /occupations/ {
        print "    occupations   = '\''fixed'\'',"
        next
    }

    /degauss/ {
        next
    }

    /smearing/ {
        next
    }
    # ----------------------------------------
    # K_POINTS
    # ----------------------------------------

    /K_POINTS/ {
        print "K_POINTS {automatic}"
        getline
        print "  2 2 3  1 1 1"
        next
    }

    {
        print
    }

    ' "$scf" > "$nscf"

done

echo
echo "Done."

ls nscf_*_berry.in
