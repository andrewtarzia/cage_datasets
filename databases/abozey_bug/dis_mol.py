import pywindow as pw
import numpy as np
import ase

####
# parameters
a = pw.MolecularSystem.load_file('ABOZEY_extracted.pdb')
system = a.system

supercell_333 = pw.utilities.create_supercell(
    a.system, 
    supercell=[[-1, 1], [-1, 1], [-1, 1]])
rebuild = supercell_333

tol = 0.4
####

# First we check which operation mode we use.
#    1) Non-periodic MolecularSystem.
#    2) Periodic MolecularSystem without rebuilding.
#    3) Periodic Molecular system with rebuilding (supercell provided).
if rebuild is not None:
    mode = 3
else:
    if 'unit_cell' in system.keys():
        if system['unit_cell'].shape == (6,):
            mode = 2
        else:
            mode = 1
    elif 'lattice' in system.keys():
        if system['lattice'].shape == (3, 3):
            mode = 2
        else:
            mode = 1
    else:
        mode = 1


print(f'mode: {mode}')

# We create a list containing all atoms, theirs periodic elements and
# coordinates. As this process is quite complicated, we need a list
# which we will gradually be reducing.
try:
    elements = system['elements']
    coordinates = system['coordinates']
except KeyError:
    raise _FunctionError(
        "The 'elements' key is missing in the 'system' dictionary "
        "attribute of the MolecularSystem object. Which means, you need to"
        " decipher the forcefield based atom keys first (see manual)."
    )

print(f'elements: {len(elements)}')
print(f'coordinates: {len(coordinates)}')

coordinates = system['coordinates']
args = (elements, coordinates)
adj = 0
# If there are forcefield 'atom ids' as well we will retain them.
if 'atom_ids' in system.keys():
    atom_ids = system['atom_ids']
    args = (elements, atom_ids, coordinates)
    adj = 1
atom_list = pw.utilities.compose_atom_list(*args)
atom_coor = pw.utilities.decompose_atom_list(atom_list)[1 + adj]

print(f'atom_list: {len(atom_list)}')
print(f'atom_coor: {len(atom_coor)}')

# Scenario 1: We load a non-periodic MolecularSystem.
# We will not have 'unit_cell' nor 'lattice' keywords in the dictionary
# and also we do not do any re-building.
# Scenario 2: We load a periodic MolecularSystem. We want to only Extract
# complete molecules that do not have been affected by the periodic
# boundary.
# Scenario 3: We load a periodic Molecular System. We want it to be rebuild
# therefore, we also provide a supercell.
# Scenarios 2 and 3 require a lattice and also their origin is at origin.
# Scenario 1 should have the origin at the center of mass of the system.
# EDIT 09-04-18: All origins/pseudo_origin had to be skewed towards some
# direction (x + 0.01) so that there would be no ambiguity in periodic
# ang highly symmetric systems where the choice of the closest atom would
# be random from a set of equally far choices - bug found in the testing
# this way rebuild system should always look the same from the same input
# and on different machines.
if mode == 2 or mode == 3:
    print(f'Scen 2,3')
    # Scenarios 2 or 3.
    origin = np.array([0.01, 0., 0.])
    if 'lattice' not in system.keys():
        matrix = pw.utilities.unit_cell_to_lattice_array(system['unit_cell'])
    else:
        matrix = system['lattice']
    print(f'matrix: {matrix}')
    pseudo_origin_frac = np.array([0.26, 0.25, 0.25])
    pseudo_origin = pw.utilities.cartisian_from_fractional(pseudo_origin_frac, matrix)
    # If a supercell is also provided that encloses the unit cell for the
    # reconstruction of the molecules through the periodic boundary.
    if rebuild is not None:
        selements = rebuild['elements']
        sids = rebuild['atom_ids']
        scoordinates = rebuild['coordinates']
        satom_list = pw.utilities.compose_atom_list(selements, sids, scoordinates)
        satom_coor = pw.utilities.decompose_atom_list(satom_list)[1 + adj]
        print(f'satom_list: {len(satom_list)}')
        print(f'satom_coor: {len(satom_coor)}')
    # There is one more step. We need to sort out for all the
    # reconstructed molecules, which are the ones that belong to the
    # unit cell. As we did the reconstruction to every chunk in the unit
    # cell we have now some molecules that belong to neighbouring cells.
    # The screening is simple. If the COM of a molecule translated to
    # fractional coordinates (so that it works for parallelpiped) is
    # within the unit cell boundaries <0, 1> then it's it. There is
    # an exception, for the trajectories, very often the unit cell
    # is centered at origin. Therefore we need to use <-0.5, 0.5>
    # boundary. We will simply decide which is the case by calculating
    # the centre of mass of the whole system.
    system_com = pw.utilities.center_of_mass(elements, coordinates)
    if np.allclose(system_com, origin, atol=1e-00):
        boundary = np.array([-0.5, 0.5])
    else:
        boundary = np.array([0., 1.])
    print(f'boundary: {boundary}')
else:
    # Scenario 1.
    pseudo_origin = center_of_mass(
        elements, coordinates) + np.array([0.01, 0., 0.])
# Here the final discrete molecules will be stored.
molecules = []
print(f'no molecules: {len(molecules)}')
# Exceptions. Usually end-point atoms that create single bonds or
# just a separate atoms in the system.
exceptions = ['H', 'CL', 'BR', 'F', 'HE', 'AR', 'NE', 'KR', 'XE', 'RN']
# The upper limit for distances analysed for bonds will be assigned for
# a given system (to save time). We take set('elements') and then find
# the largest R(cov) in the system and set the max_dist as a double
# of it plus the 150% tolerance (tol).
set_of_elements = set(system['elements'])
max_r_cov = max([
    pw.utilities.atomic_covalent_radius[i.upper()] for i in set_of_elements])
max_dist = 2 * max_r_cov + tol
# We continue untill all items in the list have been analysed and popped.
count = 0
while atom_list:
    inside_atoms_heavy = [
        i for i in atom_list if i[0].upper() not in exceptions
    ]
    if inside_atoms_heavy:
        # Now we create an array of atom coordinates. It does seem
        # somehow counter-intuitive as this is what we started with
        # and made it into a list. But, in my opinion it's the only
        # way to do it. It's hard to control and delete items in two
        # separate arrays that we started with and we don't want
        # atoms already assigned in our array for distance matrix.
        inside_atoms_coord_heavy = pw.utilities.decompose_atom_list(inside_atoms_heavy)[
            1 + adj]
        dist_matrix = pw.utilities.euclidean_distances(inside_atoms_coord_heavy,
                                          pseudo_origin.reshape(1, -1))
        atom_index_x, _ = np.unravel_index(dist_matrix.argmin(),
                                           dist_matrix.shape)
        # Added this so that lone atoms (even if heavy) close to the
        # periodic boundary are not analysed, as they surely have matching
        # symmetry equivalence that bind to a bigger atom cluster inside
        # the unit_cell.
        potential_starting_point = inside_atoms_heavy[atom_index_x]
        pot_arr = np.array(potential_starting_point[1 + adj:])
        dist_matrix = pw.utilities.euclidean_distances(
            atom_coor, pot_arr.reshape(1, -1)
            )
        idx = (dist_matrix > 0.1) * (dist_matrix < max_dist)
        if len(idx) < 1:
            pass
        else:
            working_list = [potential_starting_point]
    else:
        # Safety check.
        break
    final_molecule = []
    while working_list:
        working_list_temp = []
        try:
            atom_coor = pw.utilities.decompose_atom_list(atom_list)[1 + adj]
        except _FunctionError:
            atom_coor = None
        for i in working_list:
            if i[0].upper() not in exceptions:
                # It's of GREATEST importance that the i_arr variable
                # is assigned here before entering the atom_coor loop.!
                # Otherwise it will not be re-asigned when the satom_list
                # still iterates, but the atom_list is already empty...
                i_arr = np.array(i[1 + adj:])
                if atom_coor is not None:
                    dist_matrix = pw.utilities.euclidean_distances(
                        atom_coor, i_arr.reshape(1, -1)
                        )
                    idx = (dist_matrix > 0.1) * (dist_matrix < max_dist)
                    neighbours_indexes = np.where(idx)[0]
                    for j in neighbours_indexes:
                        j_arr = np.array(atom_coor[j])
                        r_i_j = pw.utilities.distance(i_arr, j_arr)
                        r_cov_i_j = pw.utilities.atomic_covalent_radius[
                            i[0].upper()] + pw.utilities.atomic_covalent_radius[
                                atom_list[j][0].upper()]
                        if r_cov_i_j - tol < r_i_j < r_cov_i_j + tol:
                            working_list_temp.append(atom_list[j])
                if rebuild is not None:
                    sdist_matrix = pw.utilities.euclidean_distances(
                        satom_coor, i_arr.reshape(1, -1))
                    sidx = (sdist_matrix > 0.1) * (sdist_matrix < max_dist)
                    sneighbours_indexes = np.where(sidx)[0]
                    for j in sneighbours_indexes:
                        if satom_list[j] in atom_list:
                            pass
                        else:
                            j_arr = np.array(satom_coor[j])
                            r_i_j = pw.utilities.distance(i_arr, j_arr)
                            r_cov_i_j = pw.utilities.atomic_covalent_radius[
                                i[0].upper()
                                ] + pw.utilities.atomic_covalent_radius[
                                    satom_list[j][0].upper()]
                            if r_cov_i_j - tol < r_i_j < r_cov_i_j + tol:
                                working_list_temp.append(satom_list[j])
                final_molecule.append(i)
            else:
                final_molecule.append(i)
        for i in working_list:
            try:
                atom_list.remove(i)
            except ValueError:
                pass
        # We empty the working list as all the items were analysed
        # and moved to the final_molecule list.
        working_list = []
        # We make sure there are no duplicates in the working_list_temp.
        working_list_temp = pw.utilities.unique(working_list_temp)
        # Now we move the entries from the temporary working list
        # to the working list for looping analysys.
        for i in working_list_temp:
            # We make sure that only new and unassigned atoms are
            # being transfered.
            if i not in final_molecule:
                working_list.append(i)
    final_molecule_dict = {}
    final_molecule_dict['elements'] = np.array(
        [x[0] for x in final_molecule], dtype='str')
    final_molecule_dict['coordinates'] = np.array(
        [[*xyz[1 + adj:]] for xyz in final_molecule])
    if adj == 1:
        final_molecule_dict['atom_ids'] = np.array(
            [x[1] for x in final_molecule], dtype='str')
    # write final molecule dict to file
    B = final_molecule_dict
    D = ase.Atoms() 
    for i, j in enumerate(B['elements']):
        D.append(ase.Atom(position=B['coordinates'][i], symbol=j))
    D.write(f'test_molecule{count}.pdb')
    count += 1
    print(f"no atoms in {count}: {len(final_molecule_dict['elements'])}")
    # In general we always want the molecule so the initial bool_ is True.
    bool_ = True
    # But, for periodic only if the molecule is in the initial unit cell.
    if rebuild is not None:
        com = pw.utilities.center_of_mass(final_molecule_dict['elements'],
                             final_molecule_dict['coordinates'])
        com_frac = pw.utilities.fractional_from_cartesian(com, matrix)[0]
        # If we don't round the numerical errors will come up.
        com_frac_round = np.around(com_frac, decimals=8)
        print(f'com: {com}, com_frac: {com_frac}, com_frac_round: {com_frac_round}')
        print(f'gt?: {com_frac_round >= boundary[0]}, lt?: {com_frac_round < boundary[1]}')
        bool_ = np.all(np.logical_and(com_frac_round >= boundary[0]-boundary[0]*0.01,
                                      com_frac_round < boundary[1]+boundary[1]*0.01),
                       axis=0)
    print(f'BOOL: {str(bool_)}')
    input()
    if bool(bool_) is True:
        molecules.append(final_molecule_dict)
        print(f'no molecules: {len(molecules)}')


print(f'DONE')
print(f'no molecules: {len(molecules)}')
# write all molecules to file
count2 = 0
for B in molecules:
    D = ase.Atoms() 
    for i, j in enumerate(B['elements']):
        D.append(ase.Atom(position=B['coordinates'][i], symbol=j))
    D.write(f'test_outmolecule{count2}.pdb')
    count2 += 1
