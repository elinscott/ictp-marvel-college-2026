"""Plot the LDA and Koopmans band structures of silicon."""

import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np

from koopmans.io import read

# Load the workflow
wf = read('si.pkl')

# Extract the band structures from the workflow
# Note: the API is in the process of being refactored, hence the difference
# in how we access the band structures for the LDA and Koopmans calculations
koopmans_valence_bs = wf.processes[-2].outputs.band_structure
koopmans_conduction_bs = wf.processes[-1].outputs.band_structure
lda_bs = wf.calculations[-2].results['band structure']

reference = lda_bs.energies[:, :, :4].max()

# Fetch the LDA bands, and shift them by the same amount
lda_bs_shifted = lda_bs.subtract_reference(reference)
koopmans_valence_bs = koopmans_valence_bs.subtract_reference(reference)
koopmans_conduction_bs = koopmans_conduction_bs.subtract_reference(reference)

# Plot the two band structures
ax = lda_bs_shifted.plot(label='LDA', spin=0, color='tab:blue', ls='--')
ax = koopmans_valence_bs.plot(ax=ax, label='KI@LDA', color='tab:green')
ax = koopmans_conduction_bs.plot(ax=ax, color='tab:green')

# Find the Koopmans valence band maximum
valence = koopmans_valence_bs.energies
i_vbm = np.unravel_index(np.nanargmax(valence), valence.shape)
x, _, _ = koopmans_valence_bs.get_labels()
x_vbm = x[i_vbm[1]]
y_vbm = valence[i_vbm]

# Find the Koopmans conduction band minimum
conduction = koopmans_conduction_bs.energies
i_cbm = np.unravel_index(np.nanargmin(conduction), conduction.shape)
x, _, _ = koopmans_conduction_bs.get_labels()
x_cbm = x[i_cbm[1]]
y_cbm = conduction[i_cbm]

# Label the band gap
ax.annotate(xy=(x_vbm, y_vbm), xycoords='data',
            xytext=(x_cbm, y_cbm), textcoords='data', text='',
            arrowprops={'arrowstyle': '<->', 'shrinkA': 0, 'shrinkB': 0})
ax.text((x_cbm + x_vbm) / 2 + 0.1, (y_cbm + y_vbm) / 2,
        f'{y_cbm - y_vbm:.2f} eV', ha='left', va='center',
        path_effects=[pe.withStroke(linewidth=4, foreground='white')])
 
# Tweak the figure aesthetics
ax.legend(loc='lower right', ncol=2, bbox_to_anchor=(1, 1))
ax.set_ylim([-10, 5])

# Display or save the figure (uncomment as desired)
plt.savefig('si_bandstructures.png')
# plt.show()
