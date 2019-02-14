#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Distributed under the terms of the MIT License.

"""
Script to split CIF files from the CSD that are collations of multiple entries.

Author: Andrew Tarzia

Date Created: 14 Feb 2019 (Happy Valentine's Day)

"""
import glob
import numpy as np


def write_entry(file, number, DOI, CSD):
    '''Write entry to CIF DB file that contains all names and references for a
    structure.

    '''
    with open('CIF_DB.txt', 'a') as f:
        f.write(file+','+number+','+DOI+','+CSD+'\n')


def get_entries(file):
    '''Extract full entry strings from CIF.

    '''
    with open(file , 'r') as f:
        lines = f.readlines()
    # this is a hack that relies on the CCDC formatting.
    joined = '______'.join(lines)
    sections = joined.split('####################################################################### \n______# \n')
    entries = []
    for i in sections:
        if i != '':
            item = i.split('______')
            item[0] =  '####################################################################### \n# \n'
            entries.append(item)
    return entries


def get_number(entry):
    '''Extract CCDC number from CIF string in _database_code_depnum_ccdc_archive line.

    '''
    for line in entry:
        if '_database_code_depnum_ccdc_archive' in line:
            number = line.rstrip().replace('_database_code_depnum_ccdc_archive ', '')
            number = number.split('CCDC ')[1].replace("'", '')
            return number


def get_doi(entry):
    '''Extract DOI from CIF string in _citation_doi loop line.

    '''
    for i, line in enumerate(entry):
        if '_citation_year' in line:
            # its on the next line
            DOI = entry[i+1].rstrip()
            DOI = DOI.split(' ')
            DOI = DOI[1]
            return DOI

def get_csd(entry):
    '''Extract CSD REFCODE from CIF string in XX lineself.

    Currently not in use.

    '''


def write_CIF(entry, number):
    '''Write entry string to CIF named after CCDC number.

    '''
    with open(number+'.cif', 'w') as f:
        for string in entry:
            f.write(string)

if __name__ == "__main__":
    # prepare names file
    with open('CIF_DB.txt', 'w') as f:
        f.write('file,number,DOI,CSD\n')
    # read in all CIF files with '-' in name
    for file in glob.glob('*-*.cif'):
        print(file)
        # get entries
        entries = get_entries(file)
        for i, entry in enumerate(entries):
            # get CIF number
            number = get_number(entry)
            print(number)
            # get DOI
            DOI = get_doi(entry)
            print(DOI)
            # get CSD code - currently not done
            CSD = '-'  # get_csd(entry)
            # save to new file with CSD code as name
            write_CIF(entry, str(number))
            write_entry(file, number, DOI, CSD)
