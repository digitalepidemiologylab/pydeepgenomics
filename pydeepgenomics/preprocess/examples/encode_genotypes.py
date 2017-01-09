#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys


cmd_subfolder = os.path.abspath(os.path.dirname(__file__)).split(
    "pydeepgenomics")[0]
try:
    from pydeepgenomics.preprocess import encoding, settings
    from pydeepgenomics.preprocess.vcf import vcf
    from pydeepgenomics.tools import generaltools as gt
except ImportError:
    if cmd_subfolder not in sys.path:
        sys.path.append(cmd_subfolder)
    from pydeepgenomics.preprocess import encoding, settings
    from pydeepgenomics.preprocess.vcf import vcf
    from pydeepgenomics.tools import generaltools as gt

PATH_TO_PLAYGROUND = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "playground")


def example_2(VERBOSE=True):
    subprocess.call(
        "python "+os.path.join(os.path.dirname(__file__), "setup_ex_env.py"),
        shell=True)
    vcf.split_vcf_files(PATH_TO_PLAYGROUND, verbose=False)
    # chr_to_be_processed = 2

    for chr_to_be_processed in range(1, 4):
        print(
            "###########################################\n" +
            "Processing chr {}".format(chr_to_be_processed))
        path_to_data = os.path.join(
            PATH_TO_PLAYGROUND, "split_by_chr", str(chr_to_be_processed))
        encoding.encode_file_positions(
            chr_to_be_processed,
            path_to_data,
            PATH_TO_PLAYGROUND,
            verbose=VERBOSE)
        encoding.verify_decoding(
            os.path.join(PATH_TO_PLAYGROUND, "split_by_chr"),
            os.path.join(PATH_TO_PLAYGROUND, "encoded_files"),
            str(chr_to_be_processed),
            nb_of_tests_per_file=10,
            max_nb_of_files_to_test=100,
            verbose=VERBOSE)

if __name__ == "__main__":
    example_2()
