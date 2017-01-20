#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys

cmd_subfolder = os.path.dirname(os.path.abspath(__file__))
while not cmd_subfolder .endswith('pydeepgenomics'):
    cmd_subfolder = os.path.dirname(cmd_subfolder)
cmd_subfolder = os.path.dirname(cmd_subfolder)
try:
    from pydeepgenomics.preprocess import settings, subsets
    from pydeepgenomics.preprocess.vcf import vcf
    from pydeepgenomics.tools import generaltools as gt

except ImportError:
    if cmd_subfolder not in sys.path:
        sys.path.append(cmd_subfolder)
    from pydeepgenomics.preprocess import settings, subsets
    from pydeepgenomics.preprocess.vcf import vcf
    from pydeepgenomics.tools import generaltools as gt


PATH_TO_PLAYGROUND = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "playground")


def example_3():
    subprocess.call(
        "python "+os.path.join(os.path.dirname(__file__), "setup_ex_env.py"),
        shell=True)

    vcf.split_vcf_files(PATH_TO_PLAYGROUND, verbose=False)
    subsets.make_subsets(
        os.path.join(PATH_TO_PLAYGROUND, "split_by_chr"),
        os.path.join(PATH_TO_PLAYGROUND, "subsets"))

if __name__ == "__main__":
    example_3()