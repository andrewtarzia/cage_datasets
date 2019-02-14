#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Distributed under the terms of the MIT License.

"""
Script to search for and collect CIFs using CCDC number from manually collated
list.

Author: Andrew Tarzia

Date Created: 14 Feb 2019 (Happy Valentine's Day)

"""
from ccdc.io import EntryReader, CrystalWriter
from ccdc.search import TextNumericSearch

def write_entry(file, number, DOI, CSD):
    '''Write entry to CIF DB file that contains all names and references for a
    structure.

    '''
    with open('CIF_DB.txt', 'a') as f:
        f.write(file+','+number+','+DOI+','+CSD+'\n')

number_file = '/home/atarzia/projects/cage_collect/databases/cage_manual/from_website/CIF_DB.txt'
files = []
numbers = []
DOIs = []
CSD = []
for line in open(number_file, 'r'):
    if line[0] != 'f':
        l = line.rstrip().split(',')
        files.append(l[0])
        numbers.append(l[1])
        DOIs.append(l[2])
        CSD.append(l[3])

with open('CIF_DB.txt', 'w') as f:
    f.write('file,number,DOI,CSD\n')

# dois = ['10.1021/jacs.8b07494']
for i, number in enumerate(numbers):
    query = TextNumericSearch()
    query.add_ccdc_number(int(number))
    hits = query.search(database='CSD')
    for hit in hits:
        print('%s %s' % (hit.identifier, hit.entry.ccdc_number))
        print(hit.entry.chemical_name)
        print(hit.entry.is_polymeric)
        # skip polymeric structures
        if hit.entry.is_polymeric is True:
            continue
        crystal = hit.crystal
        # write to CIF
        CrystalWriter(hit.identifier+'.cif').write(crystal)
        write_entry(files[i], number, DOIs[i], hit.identifier)
