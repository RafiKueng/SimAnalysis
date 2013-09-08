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

echo " > generating data (many.py)"
cd systems
python many.py
cd ..

echo " > generating plots (gen_plots.py)"
cd plots
python -c "import gen_plots; run()"
cd ..

echo " > generating tables (gen_tables.py)"
cd plots
python gen_tables.py
cd ..

echo "finished. you can start working on the tex files in /text"
echo "please only compile the master file <ms.tex>"