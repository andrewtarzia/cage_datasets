import logging
from rdkit.Chem import AllChem as Chem
import ase
import os
import copy
import numpy as np
import pywindow as pw
def rebuild(file, overwrite=False):
    '''As per example 6 in pywindow - rebuild the PDB system, output and reread.

    '''
    out_file = file.replace('.pdb', '_rebuild.pdb')
    if os.path.isfile(out_file) is False or overwrite is True:
        print('rebuilding:', file)
        molsys = pw.MolecularSystem.load_file(file)
        rebuild_molsys = molsys.rebuild_system()
        # output
        rebuild_molsys.dump_system(out_file,
                                   include_coms=False,
                                   override=True)
        print('rebuild done.')
    else:
        rebuild_molsys = pw.MolecularSystem.load_file(out_file)
    return rebuild_molsys
rb = rebuild(file='ABOZEY_extracted.pdb')
rb
a =pw.MolecularSystem.load_file('ABOZEY_extracted.pdb')
a
a['elements']
a.make_modular()
a
a.system
a.system['elements']
b = a.rebuild_system()
b
b.system
pw.utilities.discrete_molecules(a.system)
pw.utilities.discrete_molecules(a.system, rebuild=supercell_333)
supercell_333 = pw.utilities.create_supercell(a, supercell=supercell=[[-1, 1], [-1, 1], [-1, 1]])
supercell_333 = pw.utilities.create_supercell(a, supercell=[[-1, 1], [-1, 1], [-1, 1]])
supercell_333 = pw.utilities.create_supercell(a.system, supercell=[[-1, 1], [-1, 1], [-1, 1]])
pw.utilities.discrete_molecules(a.system, rebuild=supercell_333)
supercell_333 = pw.utilities.create_supercell(a.system, supercell=[[-2, 2], [-2, 2], [-2, 2]])
pw.utilities.discrete_molecules(a.system, rebuild=supercell_333)
pw.utilities.discrete_molecules(a.system)
supercell_333
supercell_333.elements
supercell_333['elements']

