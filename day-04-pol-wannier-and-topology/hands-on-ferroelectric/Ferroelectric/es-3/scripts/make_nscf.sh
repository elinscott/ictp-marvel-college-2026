#!/bin/bash
cd ../

directions=("x" "y" "z")

# loop on directions
for disp in "${directions[@]}"; do

    scf_file="scf_Pb_${disp}.in"

    # Loop on gdir
    for gdir in 1 2 3; do

        # KPOINTS associati
        case $gdir in
            1)
                kmesh="3 2 2 1 1 1"
                ;;
            2)
                kmesh="2 3 2 1 1 1"
                ;;
            3)
                kmesh="2 2 3 1 1 1"
                ;;
        esac

        # output name
        nscf_file="nscf_Pb_${disp}_g${gdir}.in"

        awk -v gdir="$gdir" -v kmesh="$kmesh" '

        BEGIN {
            in_control=0
            in_system=0
            in_electrons=0
            skip_k=0
        }

        #################################
        # CONTROL
        #################################
        /^ *&control/ {
            in_control=1
            print
            next
        }

        in_control && /calculation/ {
            print "    calculation   = '\''nscf'\''"
            next
        }

        in_control && /restart_mode/ {
            next
        }

        in_control && /\/$/ {
            print "    lberry        = .true."
            print "    gdir          = " gdir
            print "    nppstr        = 6"
            print " /"
            in_control=0
            next
        }

        #################################
        # SYSTEM
        #################################
        /^ *&system/ {
            in_system=1
            print
            next
        }

        in_system && /nbnd/ {
            print "    nbnd=22"
            next
        }

        in_system && /occupations/ {
            print
            print "    degauss       = 0.00"
            next
        }

        in_system && /\/$/ {
            print " /"
            in_system=0
            next
        }

        #################################
        # ELECTRONS
        #################################
        /^ *&electrons/ {
            in_electrons=1
            print
            next
        }

        in_electrons && /conv_thr/ {
            print "    conv_thr      = 1e-5,"
            next
        }

        in_electrons && /mixing_beta/ {
            print "    mixing_beta   = 0.3,"
            next
        }

        in_electrons && /\/$/ {
            print " /"
            in_electrons=0
            next
        }

        #################################
        # K_POINTS
        #################################
        /^K_POINTS/ {
            print "K_POINTS {automatic}"
            print "  " kmesh
            skip_k=1
            next
        }

        # skip old mesh
        skip_k==1 {
            skip_k=0
            next
        }

        #################################
        # nothing else to change
        #################################
        {
            print
        }

        ' "$scf_file" > "$nscf_file"

        echo "Creato $nscf_file"

    done

done
