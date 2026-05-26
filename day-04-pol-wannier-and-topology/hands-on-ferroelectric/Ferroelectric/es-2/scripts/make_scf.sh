#!/usr/bin/env bash

# ============================================================
# Script code  for MARVEL-2026 by Riccardo Dal Molin rdalmoli@sissa.it
#
# Generate N QE inputs with Pb displaced along z
#
# Assumptions:
#   - input file: scf.in
#   - ATOMIC_POSITIONS alat
#   - Pb label exactly "Pb"
#   - displacement along z
#   - total displacement = 0.12 (12% lattice parameter)
#   - total points = 12
# Output:
#   scf_000.in
#   ...
#   scf_012.in
#
# ============================================================
cd ../
set -e

INPUT="base_scf.in"

# number of structures
N=12

# maximum displacement along z
MAXDZ=0.12

echo "Generating $N distorted structures..."

for n in $(seq 0 $((N-1))); do

    lambda=$(awk -v i=$n -v N=$((N-1)) \
        'BEGIN{print i/N}')

    dz=$(awk -v l=$lambda -v d=$MAXDZ \
        'BEGIN{print l*d}')

    outfile=$(printf "scf_%03d.in" "$n")
    outdir=$(printf "./out_%03d/" "$n")

    echo " -> $outfile   dz = $dz"

    awk -v dz="$dz" -v outdir="$outdir" '

    BEGIN{
        inpos=0
    }

    # replace outdir
    /^[[:space:]]*outdir[[:space:]]*=/ {
        printf "   outdir = '\''%s'\'',\n", outdir
        next
    }

    /ATOMIC_POSITIONS/{
        inpos=1
        print
        next
    }

    inpos==1 {

        if ($1 ~ /^(K_POINTS|CELL_PARAMETERS|ATOMIC_SPECIES|OCCUPATIONS|CONSTRAINTS)$/) {
            inpos=0
            print
            next
        }

        if(NF==0){
            inpos=0
            print
            next
        }

        atom=$1
        x=$2
        y=$3
        z=$4

        if(atom=="Pb"){
            z = z + dz
        }

        printf "%-4s %18.10f %18.10f %18.10f", atom,x,y,z

        for(i=5;i<=NF;i++){
            printf " %s",$i
        }

        printf "\n"

        next
    }

    {
        print
    }

    ' "$INPUT" > "$outfile"

done

echo
echo "Done."
echo
ls scf_*.in
