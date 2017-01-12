#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math

# TEMPLATE ---> DO NOT MODIFY ! MAKE YOUR CHANGES TO THE FILE PARAMS.PY
# FIRST_ALLELE_BIT_POS
FBP = int(math.pow(2, 28))
# NUCLEOTIDE_LABELS
NL = {
    "A": int(1),
    "T": int(2),
    "G": int(4),
    "C": int(8)}
# SNPS_VALUES_ENCODED --> A-C 1st allele and then A-C 2nd allele
SVE = [
    NL["A"]*FBP,
    NL["T"]*FBP,
    NL["G"]*FBP,
    NL["C"]*FBP,
    (NL["A"])*FBP*16,
    (NL["T"])*FBP*16,
    (NL["G"])*FBP*16,
    (NL["C"])*FBP*16]

# Reverse dictionary to decode information
LN = {
    int((NL["C"])*FBP*16): "C2",
    int((NL["G"])*FBP*16): "G2",
    int((NL["T"])*FBP*16): "T2",
    int((NL["A"])*FBP*16): "A2",
    int(NL["C"]*FBP): "C1",
    int(NL["G"]*FBP): "G1",
    int(NL["T"]*FBP): "T1",
    int(NL["A"]*FBP): "A1"}


# Encoding
FILEBATCHSIZE = 10

# Subsets
PROPTRAIN = 0.6
PROPTEST = 0.2
PROPVALID = 1 - PROPTRAIN - PROPTEST


