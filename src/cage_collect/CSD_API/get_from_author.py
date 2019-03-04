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


def write_entry(author, number, DOI, CSD, solvent, disorder):
    '''Write entry to CIF DB file that contains all names and references for a
    structure.

    '''
    with open('CIF_DB_author.txt', 'a') as f:
        f.write(author+','+number+','+DOI+','+CSD+','+solvent+','+disorder+'\n')


def write_REFCODES(CSD):
    '''Write REFCODE to file.

    '''
    with open('DB.gcd', 'a') as f:
        f.write(CSD+'\n')


author_file = 'author_list.txt'
# files = []
authors = []
DOIs = []
CSD = []
for line in open(author_file, 'r'):
    authors.append(line.rstrip())

with open('CIF_DB_author.txt', 'w') as f:
    f.write('author,number,DOI,CSD,solvent,disorder\n')

with open('DB.gcd', 'w') as f:
    f.write('')

count = 0
count_no = 0
idents = []
for i, author in enumerate(authors):
    # break at '-----'
    if '-----' in author:
        break
    count_no += 1
    query = TextNumericSearch()
    query.add_author(author)
    hits = query.search(database='CSD')
    if len(hits) == 0:
        print(author)
    for hit in hits:
        # print('%s %s' % (hit.identifier, hit.entry.ccdc_number))
        # print(hit.entry.chemical_name)
        # print(hit.entry.is_polymeric)
        author_list = [i.strip() for i in hit.entry.publication.authors.split(',')]
        # skip polymeric structures
        if hit.entry.chemical_name is not None:
            if 'catena' in hit.entry.chemical_name:
                continue
        if hit.entry.is_polymeric is True:
            continue
        # skip if structure is powder study
        if hit.entry.is_powder_study is True:
            continue
        # skip structures that are purely organic
        if hit.entry.is_organometallic is False:
            continue
        # print('passed!')
        # note structures with solvent
        solvent = 'n'
        if hit.entry.chemical_name is not None:
            if len(hit.entry.chemical_name.split(' ')) > 1:
                solvent = 'y'
        # note structures with disorder
        disorder = 'n'
        if hit.entry.has_disorder is True:
            disorder = 'y'
        crystal = hit.crystal
        # write to CIF
        if hit.identifier not in idents:
            idents.append(hit.identifier)
            # CrystalWriter(hit.identifier+'.cif').write(crystal)
            write_entry(author, str(hit.entry.ccdc_number),
                        hit.entry.doi, hit.identifier, solvent,
                        disorder)
            write_REFCODES(hit.identifier)
            count += 1

print(count, 'cifs found from', count_no, 'authors')
