#!/bin/bash

# This file contains bash script to run the main function in hardsizeplus.py
# and conducts the corresponding verification tasks
# Name: Howard Cheung
# Date: 2017/11/13

# run the main function to output the new idf
python3 hardsizeeplus.py ../dat/ASHRAE90.1_OfficeLarge_STD2013_Miami.idf ../dat/eplusout.eio ./results/new.idf
