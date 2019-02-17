#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Distributed under the terms of the MIT License.

"""
Script to output the number of atoms in a CIF unit cell for a series of CIFs.

Author: Andrew Tarzia

Date Created: 17 Feb 2019

"""

import glob
from ase.io import read

def write_entry(file, number, DOI, CSD, NA):
    '''Write entry to CIF DB file that contains all names and references for a
    structure. NHA = number of atoms in crystal structure.

    '''
    with open('CIF_atom_DB.txt', 'a') as f:
        f.write(file+','+number+','+DOI+','+CSD+','+NA+'\n')

if __name__ == "__main__":
    # prepare names file
    with open('CIF_atom_DB.txt', 'w') as f:
        f.write('file,number,DOI,CSD,NA\n')
    items = open('CIF_DB.txt', 'r').readlines()[1:]
    items = [i.rstrip().split(',') for i in items]
    # iterate through all CIFs, read with ASE, determined number of atoms, save
    for item in items:
        print(item)
        file, number, DOI, CSD = item
        print(file, number, DOI, CSD)
        structure = read(CSD+'.cif')
        NA = len(structure)
        print(NA)
        write_entry(file, number, DOI, CSD, str(NA))
