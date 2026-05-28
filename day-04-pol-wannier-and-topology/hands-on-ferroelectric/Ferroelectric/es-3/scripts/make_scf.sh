#!/bin/bash
cd ../

# displacements
dx=0.01
dy=0.01
dz=0.01


base_input="base_scf.in"
positions=("x" "y" "z")

for dir in "${positions[@]}"; do
    
    outfile="scf_Pb_${dir}.in"
    outdir="./out_${dir}"

    # modificatio on input files
    awk -v d="$dir" -v dx=$dx -v dy=$dy -v dz=$dz -v outdir="$outdir" '
    BEGIN { in_positions=0; in_control=0 }

    /^ *&control/ {
        print;
        in_control=1
        next
    }
    in_control && /outdir/ {
        print "    outdir       = '\''" outdir "'\''"
        next
    }
    in_control && /\/$/ { in_control=0; print; next }

    /^ATOMIC_POSITIONS/ { 
        print; 
        in_positions=1; 
        next 
    }

    # let's change the Pb position 
    in_positions && /^[[:space:]]*Pb[[:space:]]/ {
        x = $2 + 0; y = $3 + 0; z = $4 + 0
        if(d=="x") x += dx
        if(d=="y") y += dy
        if(d=="z") z += dz
        printf "  Pb    %.6f    %.6f    %.6f\n", x, y, z
        next
    }

    in_positions && /^[[:space:]]*(Ti|O)[[:space:]]/ { in_positions=0 }

    # nothing more to change!
    { print }
    ' "$base_input" > "$outfile"

    echo "Creato $outfile"
done
