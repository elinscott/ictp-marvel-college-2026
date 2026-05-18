# How to install Quantum Mobile


QM is a Virtual Machine for Computational Materials Science.
[See the changelog for more details on the latest official release](https://github.com/marvel-nccr/quantum-mobile/blob/main/CHANGELOG.md#quantum-mobile-v2603).

## Installation instructions

Get Quantum Mobile running on your computer in three simple steps:

 1. Check your architecture
    ```bash
    uname -m 
    ```
 
 2. Download virtual machine image for your architecture:
    
    | Architecture | Links | Size |
    |---|---|---|
    | Intel x86/AMD64     | [Google Drive](https://drive.google.com/file/d/12hFWtAFn83wqAwF9H6ClXbb9adOQfpeb/view?usp=sharing) | GB |
    | Apple Silicon/ARM64 | [Google Drive](https://drive.google.com/file/d/1Xqogj1__GRIq2heB92s_2ff3QUF1nAZG/view?usp=sharing) | GB |

 3. Install Virtual Box 7.2.6 or later (see <https://www.virtualbox.org>)
 4. Import virtual machine image into Virtualbox:
    File => Import Appliance

Login credentials: username: `max`, password: `moritz`.  
The default configuration of `2` cores and `2048` MB RAM can be adjusted in the VM settings.

## Contact

For issues encountered during installation, please first consult the [FAQ page](https://github.com/marvel-nccr/quantum-mobile/wiki/Frequently-Asked-Questions#virtualbox-installationstartup-issues).

Please direct inquiries regarding Quantum Mobile to the [Quantum Mobile support channel](https://aiida.discourse.group/c/quantum-mobile/) in the AiiDA Discourse

## Build Process
#TODO: update this part
- OS: MacOS Sequoia 15.5 & Ubuntu 24.04.4 LTS
- Ansible: `13.4`
- Vagrant: `2.4.9`
- Virtualbox: `7.2.6r172322`
- Base VM Image: `bento/ubuntu-24.04`

### Software Summary

#TODO: update this part
**AMD64**

```ini
[Quantum Mobile]
version = 26.03
Operating System = Ubuntu 24.04.3 LTS
Login credentials = max / moritz
[Apt packages]
grace = 1:5.1.25-14
xcrysden = 1.6.2-4
default-jre = 2:1.21-75+exp1
rabbitmq-server = 3.12.1-1ubuntu1.4
postgresql-client = 16+257build1.1
[Conda 'abinit' environment]
abinit = 10.0.3-h2b8cb88_2@conda-forge
libxc = 4.3.4-hd8f1df9_4@conda-forge
mpich = 4.3.2-h79b1c89_101@conda-forge
[Conda 'bigdft' environment]
bigdft-suite = 1.9.5-mpi_mpich_py310h21f0213_0@conda-forge
libxc = 4.3.4-hd8f1df9_4@conda-forge
mpich = 4.3.2-h23078de_105@conda-forge
[Conda 'cp2k' environment]
cp2k = 2024.2-openblas_openmpi_hae4b963_0@conda-forge
libxc = 6.2.2-cpu_h5ef0af7_6@conda-forge
openmpi = 4.1.6-hc5af2df_101@conda-forge
[Conda 'fleur' environment]
fleur = 8.0-h4856401_0@conda-forge
openmpi = 5.0.8-h2fe1745_110@conda-forge
[Conda 'nwchem' environment]
libxc = 7.0.0-cpu_h54041b4_6@conda-forge
nwchem = 7.3.1-py314_mpi_ts_h23c3b41b_1002@conda-forge
openmpi = 5.0.8-h611b0e2_111@conda-forge
[Conda 'qespresso' environment]
openmpi = 5.0.8-h611b0e2_111@conda-forge
qe = 7.5-h19104ac_2@conda-forge
[Conda 'siesta' environment]
libxc = 7.0.0-cpu_h54041b4_6@conda-forge
openmpi = 5.0.8-h611b0e2_111@conda-forge
siesta = 5.4.2-nompi_h3aee6c3_1001@conda-forge
[Conda 'visualise' environment]
gnuplot = 5.4.10-h187b4c5_1@conda-forge
jmol = 14.32.10-ha770c72_0@conda-forge
[Conda 'wannier90' environment]
wannier90 = 3.1.0-h0652cae_4@conda-forge
[Conda 'yambo' environment]
libxc = 6.2.2-cpu_h5ef0af7_6@conda-forge
openmpi = 4.1.6-hc5af2df_101@conda-forge
yambo = 5.3.0-single_hc14117b_4@conda-forge
[Conda 'aiida' environment]
aiida-abinit = 0.4.0-pyhd8ed1ab_0@conda-forge
aiida-core = 2.8.0-pyhd8ed1ab_0@conda-forge
aiida-nwchem = 3.0.1-pyhd8ed1ab_0@conda-forge
aiida-pseudo = 1.8.0-pyhd8ed1ab_0@conda-forge
aiida-quantumespresso = 4.16.0-pyhd8ed1ab_0@conda-forge
aiida-siesta = 2.0.0-pyhd8ed1ab_0@conda-forge
ipykernel = 7.2.0-pyha191276_1@conda-forge
jupyterlab = 4.5.6-pyhd8ed1ab_0@conda-forge
jupyterlab-spellchecker = 0.8.4-pyhd8ed1ab_0@conda-forge
jupyterlab-tour = 4.0.1-pyhd8ed1ab_1@conda-forge
mamba_gator = 6.1.0-pyhd8ed1ab_0@conda-forge
pip = 26.0.1-pyh8b19718_0@conda-forge
python = 3.10.20-h3c07f61_0_cpython@conda-forge
[Pseudopotentials]
SSSP/PBE/efficiency/1.1 = /usr/local/share/pseudo_sssp_PBE_efficiency_1.1
DOJO/PBE/FR/standard/0.4/psml = /usr/local/share/pseudo_dojo_PBE_FR_standard_0.4_psml
```

**ARM64**

```ini
[Quantum Mobile]
version = 26.03
Operating System = Ubuntu 24.04.3 LTS
Login credentials = max / moritz
[Apt packages]
grace = 1:5.1.25-14
xcrysden = 1.6.2-4
default-jre = 2:1.21-75+exp1
rabbitmq-server = 3.12.1-1ubuntu1.4
postgresql-client = 16+257build1.1
[Conda 'nwchem' environment]
nwchem = 7.3.1-py314_mpi_ts_h23c3b41b_1002@conda-forge
libxc = 7.0.0-cpu_h5ec042d_6@conda-forge
openmpi = 5.0.8-hd47b191_111@conda-forge
[Conda 'qespresso' environment]
qe = 7.5-hc91ee90_1@conda-forge
openmpi = 5.0.8-hd47b191_111@conda-forge
[Conda 'yambo' environment]
yambo = 5.3.0-single_h3db96bd_4@conda-forge
libxc = 6.2.2-cpu_hc20f22c_6@conda-forge
openmpi = 4.1.6-h1f4154d_101@conda-forge
[Conda 'visualise' environment]
gnuplot = 5.4.10-hcbe3477_1@conda-forge
jmol = 14.32.10-h8af1aa0_0@conda-forge
[Conda 'aiida' environment]
aiida-core = 2.8.0-pyhd8ed1ab_0@conda-forge
aiida-nwchem = 3.0.1-pyhd8ed1ab_0@conda-forge
aiida-pseudo = 1.8.0-pyhd8ed1ab_0@conda-forge
aiida-quantumespresso = 4.16.0-pyhd8ed1ab_0@conda-forge
ipykernel = 7.2.0-pyha191276_1@conda-forge
jupyterlab = 4.5.6-pyhd8ed1ab_0@conda-forge
jupyterlab-spellchecker = 0.8.4-pyhd8ed1ab_0@conda-forge
jupyterlab-tour = 4.0.1-pyhd8ed1ab_1@conda-forge
mamba_gator = 6.1.0-pyhd8ed1ab_0@conda-forge
pip = 26.0.1-pyh8b19718_0@conda-forge
python = 3.10.20-h28be5d3_0_cpython@conda-forge
[Pseudopotentials]
SSSP/PBE/efficiency/1.1 = /usr/local/share/pseudo_sssp_PBE_efficiency_1.1
DOJO/PBE/FR/standard/0.4/psml = /usr/local/share/pseudo_dojo_PBE_FR_standard_0.4_psml
[Conda 'siesta' environment]
libxc = 7.0.0-cpu_h5ec042d_6@conda-forge
openmpi = 5.0.8-hd47b191_111@conda-forge
siesta = 5.4.2-nompi_hfa30ceb_1001@conda-forge
[Conda 'wannier90' environment]
wannier90 = 3.1.0-hb3d9914_4@conda-forge
```

