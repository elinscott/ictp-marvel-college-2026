#!/usr/bin/env bash

cd ../
set -e

OUTPUT="polarization.dat"

echo "# dz(alat)   Polarization(C/m^2)" > "$OUTPUT"

for nscfout in nscf_*_berry.out; do

    idx=$(echo "$nscfout" | sed 's/nscf_\([0-9]*\)_berry.out/\1/')

    # displacement
    dz=$(awk -v i="$idx" -v N=19 -v maxdz=0.20 '
        BEGIN{
            print (i/(N))*maxdz
        }')

    # Berry polarization
    pol=$(grep "P =" "$nscfout" | tail -1 | awk '{print $3}')

    echo "$dz  $pol" >> "$OUTPUT"

done

echo
echo "Saved to $OUTPUT"
