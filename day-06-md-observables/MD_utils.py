import numpy as np
import matplotlib.pyplot as plt


def read_lammpstrj(file_name):
    """Read a LAMMPS dump (positions wrapped/unwrapped, or velocities) into (n_frames, n_atoms, 3)."""
    frames = []
    with open(file_name) as f:
        while True:
            if not f.readline():                          # ITEM: TIMESTEP or EOF
                break
            f.readline()                                  # timestep value
            f.readline()                                  # ITEM: NUMBER OF ATOMS
            n = int(f.readline())
            for _ in range(4):                            # box bounds header + 3 lines
                f.readline()
            header = f.readline().split()[2:]             # columns after 'ITEM: ATOMS'

            def pick(*names):
                for nm in names:
                    if nm in header:
                        return header.index(nm)
                raise ValueError(f"none of {names} in {header}")

            ix = pick("xu", "x", "vx")
            iy = pick("yu", "y", "vy")
            iz = pick("zu", "z", "vz")
            id_idx = header.index("id") if "id" in header else None

            raw = np.array([f.readline().split() for _ in range(n)], dtype=float)
            if id_idx is not None:
                raw = raw[raw[:, id_idx].argsort()]

            frames.append(raw[:, [ix, iy, iz]])

    return np.stack(frames)     
   
def plot_equilibration(file_name, Nframes_eq, rho_lj):
    '''
    Plot temperature (left) and total/potential/kinetic energies (right)
    from a LAMMPS thermo file, splitting equilibration from production.
    Faded = equilibration, solid = production.
    '''
    data = np.loadtxt(file_name)
    frame = np.arange(len(data))

    # column indices: 0=TimeStep, 1=temp, 2=etot, 3=pe, 4=ke
    temp = data[:, 1]
    energies = {
        "total": data[:, 2],
        "potential": data[:, 3],
        "kinetic": data[:, 4],
    }

    c_temp = "#0072B2"
    e_colors = {"total": "#009E73", "potential": "#CC79A7", "kinetic": "#E69F00"}

    prod_start = max(Nframes_eq - 1, 0)   # avoids negative slice when Nframes_eq=0

    fig, (ax_T, ax_E) = plt.subplots(1, 2, figsize=(13, 4.5))

    # --- Temperature (faded = equilibration, solid = production) ---
    if Nframes_eq > 0:
        ax_T.plot(frame[:Nframes_eq], temp[:Nframes_eq], color=c_temp, lw=1.2,
                  alpha=0.3)
    ax_T.plot(frame[prod_start:], temp[prod_start:], color=c_temp, lw=1.2,
              label="temperature")
    if Nframes_eq > 0:
        ax_T.axvline(Nframes_eq, color="k", ls="--", lw=0.8,
                     label=f"eq / prod split ({Nframes_eq})")

    T_mean = temp[Nframes_eq:].mean()
    ax_T.axhline(T_mean, color="gray", ls=":", lw=0.8,
                 label=f"⟨T⟩_prod = {T_mean:.3f}")

    ax_T.set_xlabel("frames")
    ax_T.set_ylabel("temperature (LJ units)")
    ax_T.legend(loc="best", fontsize=8)

    # --- Energies (overlaid; faded = equilibration, solid = production) ---
    for label, y in energies.items():
        color = e_colors[label]
        if Nframes_eq > 0:
            ax_E.plot(frame[:Nframes_eq], y[:Nframes_eq], color=color, lw=1.2,
                      alpha=0.3)
        ax_E.plot(frame[prod_start:], y[prod_start:], color=color, lw=1.2,
                  label=label)

    if Nframes_eq > 0:
        ax_E.axvline(Nframes_eq, color="k", ls="--", lw=0.8,
                     label=f"eq / prod split ({Nframes_eq})")

    ax_E.set_xlabel("frames")
    ax_E.set_ylabel("energy (LJ units)")
    ax_E.legend(loc="best", fontsize=8)

    plt.tight_layout()
    plt.show()

    print(f"You are sampling the point (rho_lj, ⟨T⟩_prod) = ({rho_lj:.3f}, {T_mean:.3f})")
