#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math

# TEMPLATE ---> DO NOT MODIFY ! MAKE YOUR CHANGES TO THE FILE PARAMS.PY
# FIRST_ALLELE_BIT_POS
FBP = int(math.pow(2, 28))  # --> 268435456
# NUCLEOTIDE_LABELS
NL = {
    "A": int(math.pow(2, 0)),  # --> 1
    "T": int(math.pow(2, 1)),  # --> 2
    "G": int(math.pow(2, 2)),  # --> 4
    "C": int(math.pow(2, 4))}  # --> 8
# SNPS_VALUES_ENCODED --> A-C 1st allele and then A-C 2nd allele
SVE = [
    NL["A"] * FBP,  # --> 268435456
    NL["T"] * FBP,  # --> 536870912
    NL["G"] * FBP,  # --> 1073741824
    NL["C"] * FBP,  # --> 4294967296
    (NL["A"]) * FBP * int(math.pow(2, 5)),  # --> 8589934592
    (NL["T"]) * FBP * int(math.pow(2, 5)),  # --> 17179869184
    (NL["G"]) * FBP * int(math.pow(2, 5)),  # --> 34359738368
    (NL["C"]) * FBP * int(math.pow(2, 5))]  # --> 137438953472

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


