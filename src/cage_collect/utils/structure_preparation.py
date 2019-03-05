#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Distributed under the terms of the MIT License.

"""
Script to clean up duplicate atom disorder using trivial text rules.

Author: Andrew Tarzia

Date Created: 05 Mar 2019

"""

import glob
import sys
import pandas as pd
import pymatgen as pmg
from pymatgen.io.cif import CifParser
from cage_collect.utils.analyse_CIFs import read_cif_pmg


def write_entry(file, string):
    '''Write entry DB file with certain properties.

    Keyword Arguments:
        file (str) - output file
        string (str) - string of changes for CIF

    '''
    with open(file, 'a') as f:
        f.write(string)

if __name__ == "__main__":
    if (not len(sys.argv) == 2):
        print("""
Usage: structure_preparation.py out_file
    out_file: file to output to
""")
        sys.exit()
    else:
        out_file = sys.argv[1]
    # prepare names file
    print('This script overwrites the DB file and is only cheap analysis.')
    if input('Are you sure you want to continue? (t/f)') == 'f':
        sys.exit('exitting.')
    with open(out_file, 'w') as f:
        f.write('')

    # read in initial CIF DB
    CIF_init_DB = pd.read_csv('CIF_DB_author.txt')

    all_cifs = sorted(glob.glob('*extracted*.cif'))
    for cif in all_cifs:
        if 'cleaned' in cif:
            continue
        # if cif != 'KOJXAJ_extracted.cif':
        #     continue
        cif_out_string = '---------------------------------------------\n'
        cif_out_string += cif+':\n'
        REFCODE = cif.split('_')[0]
        try:
            solvent = CIF_init_DB[CIF_init_DB['CSD'] == REFCODE].iloc[0]['solvent']
            disorder = CIF_init_DB[CIF_init_DB['CSD'] == REFCODE].iloc[0]['disorder']
            if solvent == 'y':
                cif_out_string += '- has solvent by CSD\n'
            else:
                cif_out_string += '- no solvent by CSD\n'
            if disorder == 'y':
                cif_out_string += '- has disorder by CSD\n'
            else:
                cif_out_string += '- no disorder by CSD\n'
        except IndexError:
            cif_out_string += '- solvent and disorder info not in CSD DB file.\n'
        cif_out_1 = cif.replace('.cif', '_cleaned1.cif')
        cif_out_2 = cif.replace('.cif', '_cleaned_P1.cif')
        # read in original CIF
        with open(cif, 'r') as f:
            cif_lines = f.readlines()
        # iterate through each line, in the correct loop we want to remove
        # lines containing '*' (symmetry equivalent atoms) and '?' (atoms that
        # are duplicate by disorder)
        # section starts with '_atom_site_label'
        # section ends with 'loop_'
        # this is a crude way to do this.......
        output_lines = []
        atoms_removed = 0
        switch = 0  # turned to 1 if in the correct section
        for i, line in enumerate(cif_lines):
            if switch == 1:
                if 'loop_' in line:
                    # exit section
                    output_lines.append(line)
                    switch = 0
                else:
                    if '?' in line:
                        cif_out_string += 'disorder repeated (?) atom deleted:'
                        cif_out_string += line
                        atoms_removed += 1
                    elif '*' in line:
                        cif_out_string += 'symm op (*) atom deleted:'
                        cif_out_string += line
                        atoms_removed += 1
                    else:
                        output_lines.append(line)
            elif '_atom_site_label' in line and '_atom_site_type_symbol' in cif_lines[i+1]:
                switch = 1
                output_lines.append(line)
            else:
                output_lines.append(line)
        cif_out_string += '--> '+str(atoms_removed)+' atoms removed in total.\n'
        # print(cif_out_string)
        # write out modified CIF
        with open(cif_out_1, 'w') as f:
            for line in output_lines:
                f.write(line)
        # read in CIF to pymatgen
        try:
            structure_pmg = read_cif_pmg(cif, primitive=True)
            cif_out_string += '- structure read into pymatgen.\n'
            cif_out_string += '- converted to primitive cell and P1 symm. \n'
            cif_out_string += '- saved to '+cif_out_2+'. \n'
            structure_pmg.to(filename=cif_out_2, fmt='cif')
        except ValueError:
            cif_out_string += '- structure failed to load into pymatgen.\n'
            cif_out_string += '- end of the line \n'
        # output all changes to file
        print(cif_out_string)
        write_entry(file=out_file, string=cif_out_string)
