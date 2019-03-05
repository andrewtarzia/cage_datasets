#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Distributed under the terms of the MIT License.

"""
Script to analyze CIFs in a directory.

Author: Andrew Tarzia

Date Created: 04 Mar 2019

"""

import glob
import sys
import pymatgen as pmg
from pymatgen.io.cif import CifParser


def read_cif_pmg(file, primitive=False):
    '''A function to read CIFs with pymatgen and suppress warnings.

    '''
    s = CifParser(file, occupancy_tolerance=100)
    struct = s.get_structures(primitive=primitive)[0]
    return struct


def write_entry(file, CIF, NA):
    '''Write entry DB file with certain properties.

    Keyword Arguments:
        file (str) - output file
        CIF (str) - name of CIF
        NA (int) - number of atoms per UC from pymatgen

    '''
    with open(file, 'a') as f:
        f.write(CIF+','+str(NA)+'\n')

if __name__ == "__main__":
    if (not len(sys.argv) == 2):
        print("""
Usage: analyze_CIFs.py DB_file
    DB_file: file to output to
""")
        sys.exit()
    else:
        DB_file = sys.argv[1]
    # prepare names file
    print('This script overwrites the DB file and is only cheap analysis.')
    if input('Are you sure you want to continue? (t/f)') == 'f':
        sys.exit('exitting.')
    with open(DB_file, 'w') as f:
        f.write('CIF,NAperUC\n')

    all_cifs = sorted(glob.glob('*extracted*.cif'))
    manual_cifs = [i for i in all_cifs if 'extractedm' in i]
    auto_cifs = [i for i in all_cifs if i not in manual_cifs]
    print('there are', len(all_cifs), 'cifs.',
          len(manual_cifs), 'were collected manually',
          len(auto_cifs), ' were collected automatically.')

    error_cifs = []
    for cif in all_cifs:
        print(cif)
        # read in CIF to pymatgen
        try:
            structure_pmg = read_cif_pmg(cif)
            # get pymatgen number of atoms
            NA_pmg = len(structure_pmg)
            print(NA_pmg)
            write_entry(file=DB_file, CIF=cif, NA=NA_pmg)
        except ValueError:
            # NA_pmg = 0
            error_cifs.append(cif)
    print(len(error_cifs), 'did not load into pymatgen')
