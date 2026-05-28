"""Utility functions for the NaCl Day-01 DFT exercises."""
import numpy as np


_FCC_HS = {
    (0.00, 0.00, 0.00): r'$\Gamma$',
    (0.50, 0.50, 0.50): 'L',
    (0.00, 0.00, 1.00): 'X',
    (0.00, 0.50, 1.00): 'W',
    (0.00, 0.75, 0.75): 'K',
    (0.25, 0.25, 1.00): 'U',
}


def get_high_symm_points(bands_pp_out):
    """Return (ks, lbls): x-coordinates and FCC labels of high-symmetry points in `bands_pp.out`."""
    ks, lbls = [], []
    with open(bands_pp_out) as f:
        for line in f:
            if 'high-symmetry point' in line:
                head, _, tail = line.partition('x coordinate')
                kxyz = [float(t) for t in head.split('point:')[1].split()]
                ks.append(float(tail))
                lbls.append(_FCC_HS[tuple(sorted(round(abs(k), 4) for k in kxyz))])
    return ks, lbls


def read_efermi(scf_out):
    """Return the highest-occupied Kohn-Sham eigenvalue (eV) from a pw.x SCF output."""
    with open(scf_out) as f:
        for line in f:
            if 'highest occupied' in line:
                return float(line.split(':')[1].split()[0])
    raise ValueError(f'No "highest occupied" line found in {scf_out}')


def read_bands_gnu(gnu_file):
    """Return a list of (nk, 2) arrays (k, E in eV) from a bands.x .gnu output file, one per band."""
    bands, segment = [], []
    with open(gnu_file) as f:
        for line in f:
            line = line.strip()
            if line:
                segment.append([float(t) for t in line.split()])
            else:
                if segment:
                    bands.append(np.array(segment))
                    segment = []
    if segment:
        bands.append(np.array(segment))
    return bands


def load_kdos(pdos_file, nk):
    """Return (Egrid, intensity[nk, nE]) from a projwfc.x k-resolved pdos file."""
    d = np.genfromtxt(pdos_file, comments='#')
    Egrid = d[d[:, 0] == 1, 1]
    intensity = np.zeros((nk, len(Egrid)))
    for ik in range(1, nk + 1):
        intensity[ik - 1] = d[d[:, 0] == ik, 2]
    return Egrid, intensity
