import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# --- Fermi level from SCF output ---
efermi = None
with open('scf.out') as f:        # replace with your SCF output filename
    for line in f:
        if 'highest occupied' in line:
            efermi = float(line.split(':')[1].split()[0])
            break

# --- k-path coordinates from bands.dat.gnu (Part D) ---
k_path = []
with open('NaCl_bands.dat.gnu') as f:
    for line in f:
        line = line.strip()
        if line:
            k_path.append(float(line.split()[0]))
        else:
            break                  # only need the first band
k_path = np.array(k_path)         # shape (nk,)
nk = len(k_path)

# --- Load k-resolved ldos from a pdos_atm file ---
def load_kdos(filename, nk):
    """Return (Egrid, intensity) where intensity[ik, iE] = ldos."""
    d = np.genfromtxt(filename, comments='#')
    nE = int(np.sum(d[:, 0] == 1))
    Egrid = d[d[:, 0] == 1, 1]
    intensity = np.zeros((nk, nE))
    for ik in range(1, nk + 1):
        intensity[ik - 1] = d[d[:, 0] == ik, 2]   # col 2 = ldos (sum over m)
    return Egrid, intensity

# --- Cl 3p ---
Egrid, cl_p = load_kdos('NaCl.pdos_atm#2(Cl)_wfc#2(p)', nk)

# Restrict to a useful energy window
# Focus on the Cl 3p region; adjust limits when overlaying other orbitals
emask = (Egrid - efermi >= -8) & (Egrid - efermi <= 5)
E_plot  = Egrid[emask] - efermi
K, Emesh = np.meshgrid(k_path, E_plot)

# Clip at the 95th percentile of non-zero values so that weaker features
# are not washed out by the sharp band peaks
flat = cl_p[:, emask].ravel()
vmax = np.percentile(flat[flat > 0], 95)

fig, ax = plt.subplots(figsize=(5, 7))
ax.pcolormesh(K, Emesh, cl_p[:, emask].T,
              cmap='Reds', shading='auto', vmin=0, vmax=vmax)

ax.axhline(0, color='k', lw=0.5, ls='--')
ax.set_ylabel('$E - E_F$ (eV)')
ax.set_ylim(-8, 5)
ax.set_xlim(k_path[0], k_path[-1])

# High-symmetry point markers (fill in from bands_pp.out, as in Part D)
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
    ks.append(k); lbls.append(lbl)
ax.set_xticks(ks)
ax.set_xticklabels(lbls)

plt.tight_layout()
plt.savefig('NaCl_fatbands_Cl_p.png', dpi=150)
plt.show()
