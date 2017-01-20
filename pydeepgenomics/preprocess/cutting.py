#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip
import math
import os
import subprocess
import sys

import pandas as pd


cmd_subfolder = os.path.dirname(os.path.abspath(__file__))
while not cmd_subfolder .endswith('pydeepgenomics'):
    cmd_subfolder = os.path.dirname(cmd_subfolder)
cmd_subfolder = os.path.dirname(cmd_subfolder)

try:
    from pydeepgenomics.preprocess import encoding, settings
    from pydeepgenomics.tools import generaltools as gt
    from pydeepgenomics.tools import generaldecorators as gd
except ImportError:
    if cmd_subfolder not in sys.path:
        sys.path.append(cmd_subfolder)
    from pydeepgenomics.preprocess import encoding, settings
    from pydeepgenomics.tools import generaltools as gt
    from pydeepgenomics.tools import generaldecorators as gd


def density_of_snps(meta_file, window=1000):

    meta_ = pd.read_csv(meta_file, compression="gzip", sep="\t", index_col=False).drop(
        ["ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT"], axis=1)
    meta_['diffPOS'] = meta_['POS'] - meta_['POS'].shift(+1)
    meta_["averages"] = meta_["diffPOS"].rolling(window=window, min_periods=math.ceil(window/5)).mean()
    meta_["averages"] = meta_["averages"].dropna()

    return meta_


def cut_file(file, size_of_output_files, output_path, copy=True):

    filename = os.path.basename(file).split(".")[0]
    nb_lines = gt.get_nb_lines_file(file)
    nb_of_files = math.ceil(nb_lines / size_of_output_files)
    overlapping = math.floor(
        (size_of_output_files-nb_lines % size_of_output_files)/nb_of_files)

    begin = 0
    for i in range(int(nb_of_files)):
        end = int(min(begin + size_of_output_files, nb_lines))
        if end - begin < size_of_output_files:
            begin = int(end - size_of_output_files)
        subset_of_lines = range(begin, end)
        begin += int(size_of_output_files - overlapping)

        with open(os.path.join(
                    output_path,
                    filename+"_"+str(i + 1)+".txt"), "w") as outfile,\
                gzip.open(file, "rt") as infile:

            lines = infile.readlines()
            for index in subset_of_lines:
                outfile.write(lines[index])
        subprocess.call("gzip {}".format(
            os.path.join(output_path, filename+"_"+str(i + 1)+".txt")),
            shell=True)

    if not copy:
        subprocess.call("rm {}".format(file), shell=True)


