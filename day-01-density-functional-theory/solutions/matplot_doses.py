import numpy as np
import matplotlib.pyplot as plt
import glob

# Read Fermi energy from the header line of NaCl_dos.dat:
# "#  E (eV)   dos(E)     Int dos(E) EFermi =    X.XXX eV"
with open('NaCl_dos.dat') as f:
    header = f.readline()
efermi = float(header.split('EFermi =')[1].split()[0])

fig, ax = plt.subplots(figsize=(7, 4))

# Total DOS
dos = np.loadtxt('NaCl_dos.dat')
e = dos[:, 0] - efermi
ax.fill_between(e, dos[:, 1], alpha=0.25, color='k', label='Total')
ax.plot(e, dos[:, 1], color='k', lw=0.8)

# Projected DOS
for pdos_file in sorted(glob.glob('NaCl_pdos.pdos_atm*')):
    atom    = pdos_file.split('(')[1].split(')')[0]   # e.g. 'Na'
    orbital = pdos_file.split('(')[-1].rstrip(')\n')  # e.g. 's' or 'p'
    pdos = np.loadtxt(pdos_file)
    ax.plot(pdos[:, 0] - efermi, pdos[:, 1], lw=0.8, label=f'{atom} {orbital}')

ax.axvline(0, color='k', lw=0.5, ls='--')
ax.set_xlabel('$E - E_F$ (eV)')
ax.set_ylabel('DOS (states / eV / cell)')
ax.set_xlim(-25, 15)
ax.set_ylim(0,10)
ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig('NaCl_dos.png', dpi=150)
plt.show()
