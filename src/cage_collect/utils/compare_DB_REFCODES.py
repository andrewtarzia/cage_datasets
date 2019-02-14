#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Distributed under the terms of the MIT License.

"""
Script to compare the REFCODES in two DB files.

Author: Andrew Tarzia

Date Created: 14 Feb 2019 (Happy Valentine's Day)

"""
import sys

def read_gcd(file):
    '''Read REFCODES from gcd file from ConQuest.

    '''
    REFCODES = []
    for line in open(file, 'r'):
        REFCODES.append(line.rstrip())
    return REFCODES

if __name__ == "__main__":
    if (not len(sys.argv) == 2):
        print("""
Usage: compare_DB_REFCODES.py test_DB
    test_DB: file of REFCODEs you want to compare.""")
        sys.exit()
    else:
        test_db = sys.argv[1]
    # base DB file is the one from the MOF subset
    base_db = '/home/atarzia/projects/cage_collect/databases/MOF/MOF_subset.gcd'
    base_REFCODES = list(set(read_gcd(base_db)))
    test_REFCODES = list(set(read_gcd(test_db)))
    print('--------------------------------')
    print('base: %s -  test:%s' % (len(base_REFCODES), len(test_REFCODES)))
    print('--------------------------------')
    # which REFCODEs are in test and not in base?
    intest = []
    with open(test_db.replace('.gcd', '_intest.gcd'), 'w') as f:
        for i in test_REFCODES:
            if i not in base_REFCODES:
                intest.append(i)
                f.write(i+'\n')
    print('--------------------------------')
    print('%s in test but not in base' % (len(intest)))
    print('--------------------------------')
    # which REFCODEs are in base and not in test?
    inbase = []
    with open(test_db.replace('.gcd', '_inbase.gcd'), 'w') as f:
        for i in base_REFCODES:
            if i not in test_REFCODES:
                inbase.append(i)
                f.write(i+'\n')
    print('--------------------------------')
    print('%s in base but not in test' % (len(inbase)))
    print('--------------------------------')
    # how many REFCODES are from 2017 -> now?
