#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A bunch of tests for the functions defined in generaltools.py.
Note : they should be run from the root folder of the library with the command
python -m unittest discover
"""
import math
import os
import random
import sys
import unittest

try:
    import pydeepgenomics
    import pydeepgenomics.preprocess.settings as settings
    import pydeepgenomics.preprocess.encoding as encoding
    from pydeepgenomics.tools import generaltools as gt
    from pydeepgenomics.tools import generaldecorators as gd
except ImportError:
    cmd_subfolder = os.path.dirname(os.path.abspath(__file__))
    while not cmd_subfolder.endswith('alltests'):
        cmd_subfolder = os.path.dirname(cmd_subfolder)
    cmd_subfolder = os.path.dirname(cmd_subfolder)
    if cmd_subfolder not in sys.path:
        sys.path.append(cmd_subfolder)
    import pydeepgenomics
    import pydeepgenomics.preprocess.settings as settings
    import pydeepgenomics.preprocess.encoding as encoding
    from pydeepgenomics.tools import generaltools as gt
    from pydeepgenomics.tools import generaldecorators as gd


class TestDecodePosition(unittest.TestCase):

    def setUpClass(cls):
        cls.NL = {
            "A": int(math.pow(2, 0)),  # --> 1
            "T": int(math.pow(2, 1)),  # --> 2
            "G": int(math.pow(2, 2)),  # --> 4
            "C": int(math.pow(2, 4))}  # --> 8

    def test_on_a_sentence(self):
        starting_bit = 28
        first_allele_bit_position = math.pow(2, starting_bit)
        LN = {
            int((self.NL["C"]) * first_allele_bit_position * int(math.pow(2, 5))): "C2",
            int((self.NL["G"]) * first_allele_bit_position * int(math.pow(2, 5))): "G2",
            int((self.NL["T"]) * first_allele_bit_position * int(math.pow(2, 5))): "T2",
            int((self.NL["A"]) * first_allele_bit_position * int(math.pow(2, 5))): "A2",
            int(self.NL["C"] * first_allele_bit_position): "C1",
            int(self.NL["G"] * first_allele_bit_position): "G1",
            int(self.NL["T"] * first_allele_bit_position): "T1",
            int(self.NL["A"] * first_allele_bit_position): "A1"}
        SVE = [
            self.NL["A"] * first_allele_bit_position,  # --> 268435456
            self.NL["T"] * first_allele_bit_position,  # --> 536870912
            self.NL["G"] * first_allele_bit_position,  # --> 1073741824
            self.NL["C"] * first_allele_bit_position,  # --> 4294967296
            (self.NL["A"]) * first_allele_bit_position * int(math.pow(2, 5)),# --> 8589934592
            (self.NL["T"]) * first_allele_bit_position * int(math.pow(2, 5)),# --> 17179869184
            (self.NL["G"]) * first_allele_bit_position * int(math.pow(2, 5)),# --> 34359738368
            (self.NL["C"]) * first_allele_bit_position * int(math.pow(2, 5))]  # --> 137438953472

        expected_position = random.randrange( math.pow(2, starting_bit-1))
        expected_allele_1 = random.choice(["A", "T", "G", "C"])
        expected_allele_2 = random.choice(["A", "T", "G", "C"])

        to_test = expected_position


        allele_1, allele_2, position = encoding.decode_position(
            to_test,
            LN,
            first_allele_bit_position)



if __name__ == "__main__":
    unittest.main()
