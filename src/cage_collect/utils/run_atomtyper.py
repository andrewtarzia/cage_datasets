#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Distributed under the terms of the MIT License.

"""
Script to read in a structure into ASE, run Damien Coupry atom typer using
new Autografs API.

Author: Andrew Tarzia

Date Created: 19 Feb 2019

"""

import sys
from ase.io import read
from autografs.utils.io import write_gin
from autografs.utils.mmanalysis import analyze_mm

if __name__ == "__main__":
    if (not len(sys.argv) == 4):
        print("""
Usage: run_atomtyper.py file view version
    file: file (XYZ or CIF) to run atomtyper on.
    view: t/T if you want to visualize the ASE structure first.
    version: 2: python2 verison, 3: latest version on GitHub.""")
        sys.exit()
    else:
        file = sys.argv[1]
        view = sys.argv[2].lower()
        version = sys.argv[3]
    # get output file name
    if file[-4:] == '.cif':
        file_type = 'cif'
        path = file.replace('.cif', '.gin')
    elif file[-4:] == '.xyz':
        file_type = 'xyz'
        path = file.replace('.xyz', '.gin')
    else:
        sys.exit('file type should be CIF or XYZ in current code. Exitting.')
    if version == '3':
        # read structure
        structure = read(file)
        if view == 't':
            from ase.visualize import view
            view(structure)
            input('done?')
        # run typer
        bonds, types = analyze_mm(sbu=structure)
        # write GULP gin file
        write_gin(path, structure, bonds, types)
    elif version == '2':
        import os
        # use atom_typer to write .gin file for GULP energy calculation
        # python2 /home/atarzia/AuToGraFS/atomtyper.py -f CuOH2_CuBDC2_int.cif -l ~/AuToGraFS/libraries/uff4mof.csv -r ~/AuToGraFS/libraries/rappe.csv
        TYPER_DIR = "/home/atarzia/software/atomtyper/"
        TYPER_LIB = TYPER_DIR
        TYPER = TYPER_DIR+"atomtyper.py"
        TYPER_l = TYPER_LIB+"uff4mof.csv"
        TYPER_r = TYPER_LIB+"rappe.csv"
        os.system("python2 "+TYPER+" -f "+file+" -l "+TYPER_l+" -r "+TYPER_r)
    else:
        sys.exit('incorrect version selected. Exitting.')
