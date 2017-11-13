#!/bin/bash

# This file contains bash script to run the main function in hardsizeplus.py
# and conducts the corresponding verification tasks
# Name: Howard Cheung
# Date: 2017/11/13

# run the main function to output the new idf
python3 main.py ../dat/ASHRAE90.1_OfficeLarge_STD2013_Miami.idf ../dat/eplusout.eio ../results/new.idf

# diff the file
diff ../dat/ASHRAE90.1_OfficeLarge_STD2013_Miami.idf ../results/new.idf > ../results/idf_diff.txt

# run the new idf
energyplus -w ../dat/USA_FL_Tampa.Intl.AP.722110_TMY3.epw -p neweplus -r ../results/new.idf

# copy all files with neweplus heading to the results directory
for file in ./neweplus*; do 
    mv "$file" ../results/
done

# compare eio files
diff ../dat/eplustbl.csv ../results/neweplustbl.csv > ../results/tbl.csv.diff
