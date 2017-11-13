#!usr/bin/python3
"""
    This script reads the .eio file of an eplus simulation result and
    replace the autosize inputs in the eplus file with the actual value
    in the eio file. Only applicable for the idf files in the ../dat/
    folder.

    Name: Howard Cheung, Jiefang Gu
    Date: 2017/11/13
"""

# internal libraries
import sys


# external libraries


# user-defined libraries


# global variables


# uesr-defined classes


# user-defined functions
def main(old_idf_file: str, eio_file: str, new_idf_file: str):
    """
        Main function to be excuted to read an idf file, read the eio file,
        replace the autosized terms in the strings with the eio file values,
        and write the new results into a new file.

        Inputs:
        ==========
        old_idf_file: strings
            path to the idf file with autosized values

        eio_file: strings
            path to the eio file of the idf

        new_idf_file: strings
            path to the new idf file without autosized values
    """

    # write script to read the the old idf
    inputidf = read_file(old_idf_file)

    # write script to read the eio file
    eio = read_file(eio_file)

    # write script to transfer the values from the eio file to the idf file

    # output the new idf file


def read_file(filepath: str) -> str:
    """
        Read the text file in filepath and return the corresponding
        string in UTF-8 coding

        Inputs:
        ==========
        filepath: str
            path to the file to be written.
    """

    with open(filepath, 'rb') as fileopened:
        txt = fileopened.read()

    return txt

# running the script file
if __name__ == '__main__':

    main(sys.argv[1], sys.argv[2], sys.argv[3])
