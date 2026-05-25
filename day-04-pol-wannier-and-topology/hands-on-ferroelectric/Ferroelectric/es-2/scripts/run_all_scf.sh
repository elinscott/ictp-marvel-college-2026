#!/usr/bin/env bash
cd ../
set -e

for infile in scf_*.in; do

    base=${infile%.in}
    outfile="${base}.out"

    echo
    echo "===================================="
    echo "Running: $infile"
    echo "Output : $outfile"
    echo "===================================="
    echo

    start=$(date +%s)
    pw.x < "$infile" > "$outfile"

    end=$(date +%s)
    elapsed=$((end - start))
    hours=$((elapsed / 3600))
    minutes=$(((elapsed % 3600) / 60))
    seconds=$((elapsed % 60))

    printf "Execution time: %02d:%02d:%02d\n" $hours $minutes $seconds
    echo "Finished: $infile"
    echo

done

echo "All calculations completed."
