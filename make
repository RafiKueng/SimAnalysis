#!/bin/bash

#PYV=$(python -c 'import sys; print `sys.version_info.major`+`sys.version_info.minor`')
#ISPY=$?
#if [ "$ISPY" == "0" ]; then
#    echo "found python version " $PYV
#    if [ $PYV -le 26 ]; then
#      echo "Version too old"
#      exit 1
#    fi
#  else
#    echo 'Could not find python, please install'
#    exit 1
#fi
#
#echo "moar"

echo "make sure to have python installed"
echo "and the requests package using"
echo " 'pip install requests'"
echo " 'easy_install requests'"
echo "or similar"
echo "(but you should really use virtualenv and pip)"
echo "and of course numpy and matplotlib"

echo " > running many.."
cd systems
python many.py
cd..

echo " > running gen_plots.."
cd plots
python -c "import gen_plots; run()"
