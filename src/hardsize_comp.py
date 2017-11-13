#!usr/bin/python3
"""
    This script contains functions that copy .eio file results to
    .idf input files for different type of E+ objects

    Name: Howard Cheung, Jiefang Gu
    Date: 2017/11/13
"""

# internal libraries
from io import StringIO
import re


# external libraries
import pandas as pd


# user-defined libraries


# global variables


# uesr-defined classes


# user-defined functions
def copy_sizing_system_info(old_idf_txt: str, eio_txt: str):
    """
          Return the text with all autosized inputs of Sizing:System objects
          as a string object in UTF-format in a .idf file being replaced by
          their corresponding value in the given eio file text.

        Inputs:
        ==========
        old_idf_txt: strings
            strings of the old idf file in UTF-coding

        eio_txt: strings
        strings of the eio file in UTF-coding
    """

    # read the eio_txt for all Sizing:System and AirLoopHVAC objects that
    # require autosizing
    sys_size_data = pd.read_csv(
        StringIO(eio_txt[eio_txt.find(
                b'! <System Sizing Information>'
        ):eio_txt.find(b'! <Component Sizing Information>')].decode()),
        sep=','
    )
    comp_size_data = pd.read_csv(StringIO(eio_txt[eio_txt.find(
        b'! <Component Sizing Information>'
    ):eio_txt.find(
        b'!<Controller:MechanicalVentilation>'
    )].decode()), sep=',')

    # for each item of sizing:system, find the corresponding text and replace
    # the heating and cooling capacities
    new_txt = old_idf_txt
    for ind in sys_size_data.index:
        # use upper text only to search for consistent
        upper_txt = new_txt.upper()
        # find the location of the object
        obj_txt_re = re.compile(b''.join([
            b'SIZING:SYSTEM,\s*\n\s*',
            sys_size_data.loc[
                ind, ' System Name'
            ].encode().replace(b'_', b'\_'), b'[^;]+'
        ])).search(upper_txt)
        if obj_txt_re is not None:  # to bypass error
            obj_txt = upper_txt[obj_txt_re.span()[0]:obj_txt_re.span()[1]]
            if sys_size_data.loc[ind, ' Load Type'] == ' Cooling':
                # find the location of the particular string to be replaced
                # for the cooling capacity
                txt_re = re.compile(
                    b''.join([b'.+\n']*30+[b'\s*AUTOSIZE'])
                ).search(obj_txt)  # find the 30th field in Sizing:System
            elif sys_size_data.loc[ind, ' Load Type'] == ' Heating':
                # find the location of the particular string to be replaced
                # for the heating capacity
                txt_re = re.compile(
                    b''.join([b'.+\n']*34+[b'\s*AUTOSIZE'])
                ).search(obj_txt)  # find the 34th field in Sizing:System
            if txt_re is not None:
                # replace the string
                new_txt = str(
                    sys_size_data.loc[ind, ' User Design Capacity']
                ).encode().join([
                    new_txt[0:obj_txt_re.span()[0]+txt_re.span()[1]-8],
                    new_txt[obj_txt_re.span()[0]+txt_re.span()[1]:]
                ])

    # copy the design airflow from the AirLoopHVAC objects
    for ind in comp_size_data.index:
        # use upper text only to search for consistent
        upper_txt = new_txt.upper()
        # find the location of the object
        obj_txt_re = re.compile(b''.join([
            b'SIZING:SYSTEM,\s*\n\s*',
            comp_size_data.loc[
                ind, ' Component Name'
            ].encode().replace(b'_', b'\_'), b'[^;]+'
        ])).search(upper_txt)
        if obj_txt_re is not None and \
                comp_size_data.loc[
                    ind, ' Component Type'
                ] == ' AirLoopHVAC' and comp_size_data.loc[
                    ind, ' Input Field Description'
                ] == ' Design Supply Air Flow Rate [m3/s]':
            # to bypass error
            obj_txt = upper_txt[obj_txt_re.span()[0]:obj_txt_re.span()[1]]
            txt_re = re.compile(
                b''.join([b'.+\n']*3+[b'\s*AUTOSIZE'])
            ).search(obj_txt)  # find the 3rd field in Sizing:System
            if txt_re is not None:
                # replace the string
                new_txt = str(
                    comp_size_data.loc[ind, ' Value']
                ).encode().join([
                    new_txt[0:obj_txt_re.span()[0]+txt_re.span()[1]-8],
                    new_txt[obj_txt_re.span()[0]+txt_re.span()[1]:]
                ])

    # return the file
    return new_txt


# file testing code
if __name__ == '__main__':

    with open('../dat/comp_idf_file_for_testing.txt', 'rb') as fileopened:
        testidf = fileopened.read()

    with open('../dat/eplusout.eio', 'rb') as fileopened:
        testeio = fileopened.read()

    # check the correctness of the copying for the system:sizing
    assert copy_sizing_system_info(testidf, testeio).find(
        b'75214.72,                !- Cooling Design Capacity {W}'
    ) > 0  # for cooling capacity
    assert copy_sizing_system_info(testidf, testeio).find(
        b'45424.36,                !- Heating Design Capacity {W}'
    ) > 0 # for heating capacity
    assert copy_sizing_system_info(testidf, testeio).find(
        b'4.94579,                !- Design Outdoor Air Flow Rate {m3/s}'
    ) > 0  # for airflow
    print(copy_sizing_system_info(testidf, testeio).decode())

    # print statement
    print('File hard_size_comp.py is OK!')
