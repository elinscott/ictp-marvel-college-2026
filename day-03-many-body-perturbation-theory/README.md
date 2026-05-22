# Many-body perturbation theory: Hands-on session

**Tutors**: M. Bonacci, G. Sesti, C. Borghesi

This page provides the instructions and tutorials for the session dedicated to Yambo.

Webpage of the event: [Joint ICTP MARVEL College: Materials simulations in the age of AI](https://indico.ictp.it/event/11146).


## Instructions to load Yambo

First, you need to launch the Quantum Mobile. Remember, the instructions to do so are found [here](https://quantum-mobile.readthedocs.io/en/latest/users/launch.html).

Once accessed the Quantum Mobile, open a terminal. You will see that a `conda` environment is automatically loaded. 

```{code-block} none
(base) max@qmobile:~$
```

The conda base environment does not load the packages neccesary for this tutorial. 
In order to load them, let's switch to the yambo environment. Just type `workon yambo`. You should see

```{code-block} none
 (yambo) max@qmobile:~$
```

Let us now create a directory where we will do the tutorial:

```{code-block} none
$ mkdir yambo
$ cd yambo
```

At this point, download the files used in the tutorial via `wget`:

```{code-block} none
$ wget https://media.yambo-code.eu/educational/tutorials/files/hBN.tar.gz https://media.yambo-code.eu/educational/tutorials/files/hBN-2D.tar.gz 
```

and extract (unzip) them

```{code-block} none
$ tar -xvf hBN.tar.gz
$ tar -xvf hBN-2D.tar.gz
```

````{tip}
For clarity, we suggest you to copy the `hBN` directory twice, as the same system is used in multiple tutorials
```{code-block}
$ cp -r hBN hBN_IPA
$ cp -r hBN hBN_GW
```
Run the independent particle tutorial in `hBN_IPA`, and the _GW_ tutorial in `hBN_GW`.

````

You are now all set for the tutorial. Just for safety, check that the executable works by typing

```{code-block} none
$ yambo -h
```

This should print the help of the Yambo command-line interface.


## Tutorials

You will learn how to get to your first _GW_ calculation with Yambo.

Follow the tutorials listed below. 

```{note}
You may want to skip or just have quick look to the optional sections present in some of these 
tutorials.
```

### First steps: from DFT to optical properties

1. [Generate a Yambo SAVE folder]((https://yambo-code.github.io/yambo-wiki/tutorials/basic/database_generation.html#database-generation-tutorial-target))
2. [Initialize the Yambo SAVE folder](#database-initialization-tutorial-target)
3. [Generate input files using Yambo's command-line interface](#input-file-generation-tutorial-target)
4. [Optics at the independent particle level](#optics-ipa-tutorial-target)
5. [RPA and local field effects](#local-fields-tutorial-target)

### A GW calculation with Yambo

1. [Quasiparticle corrections within the Hartree-Fock approximation](#hf-on-hbn-tutorial-target)
2. [A full GW calculation with Yambo](#gw-on-hbn-tutorial-target)
