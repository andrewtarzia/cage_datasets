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
import pymatgen as pmg

def write_entry(file, number, DOI, CSD, NA_ase, NA_pmg):
    '''Write entry to CIF DB file that contains all names and references for a
    structure. NA = number of atoms in crystal structure.

    '''
    with open('CIF_atom_DB.txt', 'a') as f:
        f.write(file+','+number+','+DOI+','+CSD+','+NA_ase+','+NA_pmg+'\n')

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
        try:
            structure_ase = read(CSD+'.cif')
            NA_ase = len(structure_ase)
        except RuntimeError:
            NA_ase = 0
        try:
            structure_pmg = pmg.Structure.from_file(CSD+'.cif')
            NA_pmg = len(structure_pmg)
        except ValueError:
            NA_pmg = 0
        print(NA_ase)
        print(NA_pmg)
        write_entry(file, number, DOI, CSD, str(NA_ase), str(NA_pmg))
