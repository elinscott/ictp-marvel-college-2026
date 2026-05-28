import numpy as np
import matplotlib.pyplot as plt

# --- Read highest occupied level from SCF output ---
# pw.x prints: "highest occupied, lowest unoccupied level (eV):  X.XXXX  X.XXXX"
efermi = None
with open('scf.out') as f:   # replace with your SCF output file name
    for line in f:
        if 'highest occupied' in line:
            efermi = float(line.split(':')[1].split()[0])
            break

# --- Parse the .gnu file ---
bands, segment = [], []
with open('NaCl_bands.dat.gnu') as f:
    for line in f:
        line = line.strip()
        if line:
            k, e = map(float, line.split())
            segment.append((k, e - efermi))
        else:
            if segment:
                bands.append(np.array(segment))
                segment = []
if segment:
    bands.append(np.array(segment))

# --- Plot ---
fig, ax = plt.subplots(figsize=(5, 7))
for band in bands:
    ax.plot(band[:, 0], band[:, 1], 'b-', lw=0.8)

ax.axhline(0, color='k', lw=0.5, ls='--')  # E_F

# High-symmetry points: fill in k-coordinates from bands_pp.out
from collections import deque
k_L = 0.0000
k_G = 0.8660
k_X = 1.8660
k_W = 2.3660
k_K = 2.7196
k_G2 = 3.7802




hs_points = deque([
    (k_L,  'L'),
    (k_G,  r'$\Gamma$'),
    (k_X,  'X'),
    (k_W,  'W'),
    (k_K,  'K'),
    (k_G2, r'$\Gamma$'),
])
ks, lbls = [], []
while hs_points:
    k, lbl = hs_points.popleft()
    ax.axvline(k, color='k', lw=0.5)
    ks.append(k)
    lbls.append(lbl)
ax.set_xticks(ks)
ax.set_xticklabels(lbls)

ax.set_ylabel('$E - E_F$ (eV)')
ax.set_ylim(-20, 15)    # adjust to your output
ax.set_xlim(bands[0][0, 0], bands[0][-1, 0])
plt.tight_layout()
plt.savefig('NaCl_bands.png', dpi=150)
plt.show()
