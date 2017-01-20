#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil

cmd_subfolder = os.path.dirname(os.path.abspath(__file__))
while not cmd_subfolder .endswith('pydeepgenomics'):
    cmd_subfolder = os.path.dirname(cmd_subfolder)
cmd_subfolder = os.path.dirname(cmd_subfolder)
try:
    from pydeepgenomics.tools import generaltools as gt
except ImportError:
    if cmd_subfolder not in sys.path:
        sys.path.append(cmd_subfolder)
    from pydeepgenomics.tools import generaltools as gt

if __name__ == "__main__":
    print("Initializating the playground ...")
    PATH_TO_VCF = os.path.join(
        cmd_subfolder,
        "alltests",
        "sim_data",
        "vcf_files")
    PATH_TO_OUTPUT = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "playground")

    if not os.path.isdir(PATH_TO_OUTPUT):
        os.mkdir(PATH_TO_OUTPUT)
    else:
        shutil.rmtree(PATH_TO_OUTPUT)
        os.mkdir(PATH_TO_OUTPUT)

    vcf_files = gt.list_elements(PATH_TO_VCF, type_="file", extension=".vcf.gz")
    for file in vcf_files:
        shutil.copy(file, PATH_TO_OUTPUT)
        name_file = os.path.basename(file)
        copied_file = os.path.join(PATH_TO_OUTPUT, name_file)
