for CIF in glob.glob('*.cif'): 
    ...:     try: 
    ...:         pdb_file, struct = convert_CIF_2_PDB(CIF) 
    ...:     except IndexError: 
    ...:         continue 
    ...:     rebuilt_structure = rebuild_system(file=pdb_file) 
    ...:     #print('modularising...') 
    ...:     rebuilt_structure.make_modular() 
    ...:     #print('done.') 
    ...:     no_atoms_orig = len(struct) 
    ...:     n_atoms_list = [] 
    ...:     for molecule in rebuilt_structure.molecules: 
    ...:         n_atoms_list.append(rebuilt_structure.molecules[molecule].no_of_atoms) 
    ...:     max_count = max(n_atoms_list) 
    ...:     print(CIF, Counter(n_atoms_list), max_count, no_atoms_orig) 
    ...:     #break 

