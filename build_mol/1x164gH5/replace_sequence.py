#!/usr/bin/env python
# Author:  Steven C. Howell
# Purpose: Replace DNA sequence with another sequence
# Created: 04/24/2014
# $Id: replace_sequence.py 176 2015-03-17 03:32:38Z xraylab $
'''
This script loads a pdb structure file of DNA, replaces the DNA sequence,
then saves the result as a new pdb.  The pdb input should just be the DNA
backbone (this can be achieved by loading a pdb into VMD, then saving just
the backbone of the DNA into a new PDB). It is important to check that the
same number of residues are in the two inputs.
'''


import sys
import os
import os.path as op
import subprocess
import logging
import sassie.sasmol.sasmol as sasmol
import numpy as np

# chain1_out = 'dimer/dna1_right_seq.pdb'
# chain1_pdb = 'dimer/dna1_wrong_seq.pdb'
# chain1 = sasmol.SasMol(0)
# chain1.read_pdb(chain1_pdb)
# sequenceFile = 'dimer/dimer_dna1_correct.seq'

chain1_out = 'gH5_NCP_dna1.pdb'
chain1_pdb = 'gH5_NCP_dna1bb.pdb'
chain1 = sasmol.SasMol(0)
chain1.read_pdb(chain1_pdb)
sequenceFile = 'correct_dna1.seq'

chain2_out = 'gH5_NCP_dna2.pdb'
chain2_pdb = 'gH5_NCP_dna2bb.pdb'
chain2 = sasmol.SasMol(0)
chain2.read_pdb(chain2_pdb)

with open(sequenceFile) as f:
    lines = f.read().splitlines()
sequence = lines[0]
reverse = sequence[::-1]

amino_acids_pdb2seq = {'ALA': 'A',
                       'ARG': 'R',
                       'ASN': 'N',
                       'ASP': 'D',
                       'CYS': 'C',
                       'GLU': 'E',
                       'GLN': 'Q',
                       'GLY': 'G',
                       'HIS': 'H',
                       'ILE': 'I',
                       'LEU': 'L',
                       'LYS': 'K',
                       'MET': 'M',
                       'PHE': 'F',
                       'PRO': 'P',
                       'SER': 'S',
                       'THR': 'T',
                       'TRP': 'W',
                       'TYR': 'Y',
                       'VAL': 'V'}

dna_pdb2seq = {'DG': 'G',
               'DA': 'A',
               'DT': 'T',
               'DC': 'C',
               'GUA': 'G',
               'ADE': 'A',
               'THY': 'T',
               'CYT': 'C'}

dna_seq2pdb = {'G': 'GUA',
               'A': 'ADE',
               'T': 'THY',
               'C': 'CYT'}

dna_compliment = {'G': 'C',
                  'A': 'T',
                  'T': 'A',
                  'C': 'G'}

last_atom = 0
res = 0
for (i, atom) in enumerate(chain1.resid()):
    if atom != last_atom:
        res += 1
        last_atom = atom
    print atom, '- changing aa.resname()[', i, '] from: ', chain1.resname()[i], 'to: ', dna_seq2pdb[sequence[res - 1]]
    chain1.resname()[i] = dna_seq2pdb[sequence[res - 1]]
    chain1.resid()[i] = res

last_atom = 0
res = 0
for (i, atom) in enumerate(chain2.resid()):
    if atom != last_atom:
        res += 1
        last_atom = atom
    compliment = dna_compliment[reverse[res - 1]]
    print 'atom: ', atom, ' compliment: ', compliment
    chain2.resname()[i] = dna_seq2pdb[compliment]
    chain2.resid()[i] = res

chain1.setResname(chain1.resname())
chain2.setResname(chain2.resname())
chain1.setResid(chain1.resid())
chain2.setResid(chain2.resid())

chain1.write_pdb(chain1_out, 0, 'w')
chain2.write_pdb(chain2_out, 0, 'w')


print 'COMPLETE'
