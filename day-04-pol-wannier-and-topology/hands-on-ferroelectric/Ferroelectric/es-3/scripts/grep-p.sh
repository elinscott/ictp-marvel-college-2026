#!/usr/bin/env bash

# ==========================================================
# Extract polarization from files:
#
#   nscf_Pb_x_g1.out
#   nscf_Pb_x_g2.out
#   ...
#
# and save
#
# direction   gdir   displacement(alat)   P(C/m^2)   Z(Pb)
#
# to polarization.dat
# ==========================================================
cd ../
set -e

OUTPUT="polarization.dat"

disp=0.01

echo "# dir   gdir   displacement(alat)   Polarization(C/m^2)   P_over_disp" > "$OUTPUT"

for nscfout in nscf_Pb_*_g*.out; do

    # ==========================================
    # extract direction and gdr
    # ==========================================

    dir=$(echo "$nscfout" | sed 's/nscf_Pb_\([xyz]\)_g[123].out/\1/')

    gdir=$(echo "$nscfout" | sed 's/nscf_Pb_[xyz]_g\([123]\).out/\1/')

    # ==========================================
    # Berry polarization
    # ==========================================

    pol=$(grep "P =" "$nscfout" | tail -1 | awk '{print $3}')

    # Controllo
    if [[ -z "$pol" ]]; then
        echo "Polarization not found in $nscfout"
        continue
    fi

    # ==========================================
    # P/displacement = Z 
    # ==========================================

    ratio=$(awk -v p="$pol" -v d="$disp" '
        BEGIN{
            printf "%.10f", p/d
        }')

    # ==========================================
    # save
    # ==========================================

    printf "%s   %s   %.4f   %s   %s\n" \
        "$dir" "$gdir" "$disp" "$pol" "$ratio" >> "$OUTPUT"

done

echo
echo "Saved to $OUTPUT"
echo

cat "$OUTPUT"
