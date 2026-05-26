#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Read polarization.dat
#
# Expected format:
#
# dir   gdir   displacement   P   P_over_disp
#
# Example:
# x   1   0.01   0.123   12.3
# ==========================================================

filename = "../polarization.dat"

# 3x3 matrix:
#
# rows    -> displacement direction (x,y,z)
# columns -> gdir (1,2,3)
#
# matrix[i,j] = P/displacement
#

ratio_matrix = np.zeros((3,3))

dir_to_index = {
    "x": 0,
    "y": 1,
    "z": 2
}

# ==========================================================
# Read file
# ==========================================================

with open(filename, "r") as f:

    for line in f:

        # Skip comments
        if line.startswith("#"):
            continue

        data = line.split()

        direction = data[0]
        gdir      = int(data[1])

        displacement = float(data[2])
        polarization = float(data[3])
        ratio        = float(data[4])

        i = dir_to_index[direction]
        j = gdir - 1

        ratio_matrix[i, j] = ratio

# ==========================================================
# Print matrix
# ==========================================================

print("\nZ(Pb) : \n")

print("         x          y          z")

dirs = ["x", "y", "z"]

for i, d in enumerate(dirs):

    print(
        f"{d}   "
        f"{ratio_matrix[i,0]:12.6f} "
        f"{ratio_matrix[i,1]:12.6f} "
        f"{ratio_matrix[i,2]:12.6f}"
    )

