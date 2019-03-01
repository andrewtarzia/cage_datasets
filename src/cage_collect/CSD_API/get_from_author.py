#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Distributed under the terms of the MIT License.

"""
Script to search for and collect CIFs using a list of authors.

Author: Andrew Tarzia

Date Created: 1 Mar 2019

"""
from ccdc.io import EntryReader, CrystalWriter
from ccdc.search import TextNumericSearch


def write_entry(number, DOI, CSD, solvent, disorder):
    '''Write entry to CIF DB file that contains all names and references for a
    structure.

    '''
    with open('CIF_DB_author.txt', 'a') as f:
        f.write(author+','+number+','+DOI+','+CSD+','+solvent+','+disorder+'\n')


author_file = 'CCDC_code.txt'
# files = []
authors = []
DOIs = []
CSD = []
for line in open(author_file, 'r'):
    authors.append(line.rstrip())

with open('CIF_DB_author.txt', 'w') as f:
    f.write('author,number,DOI,CSD,solvent,disorder\n')

count = 0
count_no = 0
idents = []
for i, number in enumerate(authors):
    count_no += 1
    # print(number)
    query = TextNumericSearch()
    query.add_ccdc_number(int(number))
    hits = query.search(database='CSD')
    if len(hits) == 0:
        print(number)
    for hit in hits:
        # print('%s %s' % (hit.identifier, hit.entry.ccdc_number))
        # print(hit.entry.chemical_name)
        # print(hit.entry.is_polymeric)
        # skip polymeric structures
        if hit.entry.is_polymeric is True:
            continue
        # note structures with solvent
        solvent = 'n'
        if len(hit.entry.chemical_name.split(' ')) > 1:
            solvent = 'y'
        disorder = 'n'
        if hit.entry.has_disorder is True:
            disorder = 'y'
        crystal = hit.crystal
        # write to CIF
        if hit.identifier not in idents:
            idents.append(hit.identifier)
            CrystalWriter(hit.identifier+'.cif').write(crystal.disordered_molecule)
            write_entry(author, hit.entry.ccdc_number,
                        hit.entry.doi, hit.identifier, solvent,
                        disorder)
            count += 1

print(count, 'cifs found from', count_no, 'authors')
