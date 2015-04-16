# -*- coding: utf-8 -*-

'''
Testing restriction site finder methods. KEY:
    A
    C
    G
    T
    R = A/G (purine)
    Y = C/T (pyrimidine)
    W = A/T (weak)
    S = C/G (strong)
    M = A/C (amino)
    K = G/T (keto)
    B = C/G/T
    D = A/G/T
    H = A/C/T
    V = A/C/G
    N = A/C/G/T
'''

'''
Crazy thinkin', but if we were looking for n-cutters,
could we possibly iterate through all windows of size N once?
And only add a match when we ... oh wait. I already do this.
'''

import re

nucleotideMatrix = {'R':['A','G'],
                    'Y':['C','T'],
                    'W':['A','T'],
                    'S':['C','G'],
                    'M':['A','C'],
                    'K':['G','T'],
                    'B':['C','G','T'],
                    'D':['A','G','T'],              
                    'H':['A','C','T'],
                    'V':['A','C','G'],
                    'N':['A','C','G','T']}

from pyviko.restriction import restrictionSites
from pyviko.base import findOverprintedGene

def findNonRegexEnzymeSites(site):
    '''
    Builds a list of sequences that correspond to a given 
    restriction enzyme recognition site.
    '''
    possible_seqs = ['']
    for nt in site:
        if nt in 'ACGT':
            for i in xrange(len(possible_seqs)):
                possible_seqs[i] = possible_seqs[i] + nt
        else:
            placeholder = []
            for seq in possible_seqs:
                for possibility in nucleotideMatrix[nt]:
                    placeholder.append(seq+possibility)
            possible_seqs = [ss for ss in placeholder]
    return possible_seqs
    
def findEnzymeSiteRegex(site):
    r_site = ''
    for nt in site:
        if nt in 'ACGT':
            r_site += nt
        else:
            r_site += '['
            try:
                for m in nucleotideMatrix[nt]:
                    r_site += m
            except KeyError:
                print "Unknown nucleotide '" + nt  + "' encountered."
            r_site += ']'
    return r_site

def findNcutters(seq, n):
    '''
    Find restriction sites of length `n` in a sequence `seq`
    in `O(n*m)` where n is the sequence length and m is the
    number of restriction enzymes.
    '''
    n_mers = []
    for i in range(0, len(seq) - (n-1)):
        n_mers.append((i, seq[i:i+n]))
    actualSites = []
    for s in n_mers:
        if s[1] in restrictionSites.keys():
            actualSites.append((s[0],restrictionSites[s[1]]))
            
    # Limitation: assumes dict restrictionSites is in non-regex form (could be very large)
    return actualSites

'''
# testing regex counter.
testSites = ['AA', 'TATGCG', 'ARA', 'RRR', 'NN', 'ABC', 'SS', 'NAV']
for t in testSites:
    print findNonRegexEnzymeSites(t)
# looks good!
'''
#sequence = 'ATGGAACAAGCCCCGGAAGACCAAGGGCCACAAAGAGAGCCATACAATGAATGGACACTAGAATTATTAGATGAACTCAAACAGGAAGCAGTAAGACATTTTCCTAGACAGTGGCTTCATGATTTAGGACAGCACATTTATAACACATATGGAGACACTTGGGCGGGGGTTGAGGCTATCATAAGGATCCTGCAACAATTGCTGTTTATTCATTACAGAATTGGCTGCCAACATAGCAGAATAGGCATTCTGCCACAAGGAAGAAGGAGAAATGGATCCAATAGATCCTAA'

'''
print findNcutters(sequence, 6)
# initial test good
'''
'''
print findOverprintedGene(sequence, -1, 3)
# looks good!
'''

###################################
# Testing enzyme regex search
# This will be important to actually implement as a function! 
# findRestrictionSites or something
sequence = 'AAAGGGCCCTTTAGCTAGAGAGACAGACA'
s = []
sites = ['AAAGGG','AAASSS','SSS','SSSWWW','SWSR']
for si in sites:
    s.append(findEnzymeSiteRegex(si))
    
print s

for ww in s:
    q = re.finditer(ww, sequence)
    for i in q:
        print (i.start(), i.string[i.start():i.end()]),
    print ''
#looks good!
# LIMITATION: Does not search overlapping sequences.
# For palindromes, this is not an issue
###################################

###################################
# weak func testing cutters with a list of restriction sites as input
def testNcutters(seq, n, rlist):
    n_mers = []
    for i in range(0, len(seq) - (n-1)):
        n_mers.append((i, seq[i:i+n]))
    actualSites = []
    for s in n_mers:
        if s[1] in rlist:
            actualSites.append((s[0],s[1]))
    return actualSites

# Testing non-regex search. 
# Ideally, should have the same results for regex and non-regex searches
sequence = 'AAAGGGCCCTTTAGCTAGAGAGACAGACA'
s = []
sites = ['AAAGGG','AAASSS','SSS','SSSWWW','SWSR']
for sis in sites:
    s.append(findNonRegexEnzymeSites(sis))
    
for ww in s:
    print testNcutters(sequence, len(ww[0]), ww)
    
# looks good! 
# This search is complete (including overlapping sequences)
###################################