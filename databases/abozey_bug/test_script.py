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
    
# this rebuild leads to no atoms    
rb = rebuild(file='ABOZEY_extracted.pdb')

a = pw.MolecularSystem.load_file('ABOZEY_extracted.pdb')
a.make_modular()
a.dump_system('testa.pdb')  # same atom positions as 'ABOZEY_extracted.pdb'
b = a.rebuild_system()
b.dump_system('testb.pdb')  # no atoms
# build super cell
supercell_333 = pw.utilities.create_supercell(a.system, supercell=[[-1, 1], [-1, 1], [-1, 1]])
# write to PDB
super_cell_struct = ase.Atoms()
for i, j in enumerate(supercell_333['elements']):
    # print(supercell_333['coordinates'][i], j)
    super_cell_struct.append(ase.Atom(position=supercell_333['coordinates'][i], symbol=j))
super_cell_struct.write('test_super.pdb') # this structure is not empty
# 
					
pw.utilities.discrete_molecules(a.system)  # not empty
pw.utilities.discrete_molecules(a.system, rebuild=supercell_333) # empty - this is what
# is done by default in .rebuild_system()

# try and decipher part of discrete molecule that gives issue
# get discrete molecules out with tol = 0.1
disc_struct = ase.Atoms()
D = pw.utilities.discrete_molecules(a.system, rebuild=supercell_333, tol=0.1)[0]
for i, j in enumerate(D['elements']):
    # print(supercell_333['coordinates'][i], j)
    disc_struct.append(ase.Atom(position=D['coordinates'][i], symbol=j))
disc_struct.write('test_tol01.pdb') # this structure is just a benzene ring.

## steps in discrete_molecules()
# rebuild = supercell_333 --> mode 3
# write lists 'elements' and 'coordinates' from system input to edit
# mode 3 implies scenario 3: - periodic system
# everything up to line 948 of pywindow on github (and in anaconda) works

# trying to recreate one loop through while list at line 997
# this should tell me if it is not collecting molecules.

# write discrete_molecules() into a python script to rnu and edit with
# print statements

###### it seems the bug is with the check whether any molecules are inside the UC
# this seems to stem from the ODD chance that the COM of the molecules are
# not within the UC, this seems like a bug (something I handled in epitmof)
# I should be able to fix this in the pywindow code




