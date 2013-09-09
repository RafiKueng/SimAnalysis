#!/bin/bash
echo "this expects that you have already run make"
echo "and no major changes happend"
echo "will regenerate all tex files and copy over the plots"

read -p "Press [Enter] key to start..."

echo " "
echo "/===================================="
echo "=> generating plots (gen_plots.py)"
cd plots
python -c "from gen_plots import *; all_tex(); plotAllRE()"
cd ..

echo " "
echo "/===================================="
echo "=> generating tables (gen_tables.py)"
cd plots
python gen_table.py
cd ..

echo " "
echo "/===================================="
echo "finished update"