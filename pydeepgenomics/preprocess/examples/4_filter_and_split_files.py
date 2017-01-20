#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys

import matplotlib
import matplotlib.pyplot as plt

cmd_subfolder = os.path.dirname(os.path.abspath(__file__))
while not cmd_subfolder .endswith('pydeepgenomics'):
    cmd_subfolder = os.path.dirname(cmd_subfolder)
cmd_subfolder = os.path.dirname(cmd_subfolder)
try:
    from pydeepgenomics.preprocess import settings, subsets, filtering, cutting
    from pydeepgenomics.preprocess.vcf import vcf
    from pydeepgenomics.tools import generaltools as gt

except ImportError:
    if cmd_subfolder not in sys.path:
        sys.path.append(cmd_subfolder)
    from pydeepgenomics.preprocess import settings, subsets, filtering, cutting
    from pydeepgenomics.preprocess.vcf import vcf
    from pydeepgenomics.tools import generaltools as gt


PATH_TO_PLAYGROUND = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "playground")
matplotlib.style.use('ggplot')


def example_4():
    subprocess.call(
        "python "+os.path.join(os.path.dirname(__file__), "setup_ex_env.py"),
        shell=True)
    vcf.split_vcf_files(PATH_TO_PLAYGROUND, verbose=False)
    averages = cutting.density_of_snps(os.path.join(
            PATH_TO_PLAYGROUND,
            "split_by_chr",
            "1",
            "_meta.txt.gz" ),
        window=50)
    plt.ion()
    ax = averages.plot(x="POS", y="averages")
    ax.legend("Moving average")
    plt.ion()
    input("Press Enter to continue...")
    #filtering.mask_data(os.path.join(PATH_TO_PLAYGROUND, "split_by_chr"), 0.1)


if __name__ == "__main__":
    example_4()
