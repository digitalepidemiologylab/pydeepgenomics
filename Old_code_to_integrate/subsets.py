#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import os
import random
import subprocess

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', os.path.dirname("")))

# If custom version of params doesn't exist, copy template
if not os.path.isfile("./params.py"):
    subprocess.call("cp paramstemplate.py params.py", shell=True)
    from params import *
    from pydeepgenomics.preprocess import usefulfunctions as uf
else:
    from params import *
    from pydeepgenomics import preprocess as uf

listchromsdirs = uf.list_elements(PATHENCODED, _type="dir")
listofchroms = [chroms.split("/")[-1] for chroms in listchromsdirs]
# Create the tree for the repartition of the dataset
if not os.path.isdir(PATHSUBSET+"/Subsets"):
    os.mkdir(PATHSUBSET+"/Subsets")
    os.mkdir(PATHSUBSET+"/Subsets/FULL")
    uf.create_chrom_dirs(PATHSUBSET+"/Subsets/FULL", listofchroms)
    subprocess.call("cp -rf {0} {1}".format(
        PATHSUBSET+"/Subsets/FULL",
        PATHSUBSET+"/Subsets/10_PERCENT"),
        shell=True)
    subprocess.call("cp -rf {0} {1}".format(
        PATHSUBSET+"/Subsets/FULL ",
        PATHSUBSET+"/Subsets/1_PERCENT"),
        shell=True)
elif not os.path.isdir(PATHSUBSET+"/Subsets/FULL"):
    os.mkdir(PATHSUBSET+"/Subsets/FULL")
    uf.create_chrom_dirs(PATHSUBSET+"/Subsets/FULL", listofchroms)
    subprocess.call(
        "rm -r {0}/10_PERCENT {0}/1_PERCENT".format(PATHSUBSET+"/Subsets"),
        shell=True)
    subprocess.call(
        "cp -rf {0} {1}".format(
            PATHSUBSET+"/Subsets/FULL",
            PATHSUBSET+"/Subsets/10_PERCENT"),
        shell=True)
    subprocess.call(
        "cp -rf {0} {1}".format(
            PATHSUBSET+"/Subsets/FULL ",
            PATHSUBSET+"/Subsets/1_PERCENT"),
        shell=True)
else:
    subprocess.call(
        "rm -r {0}/10_PERCENT {0}/1_PERCENT".format(PATHSUBSET+"/Subsets"),
        shell=True)
    os.mkdir(PATHSUBSET+"/Subsets/10_PERCENT")
    uf.create_chrom_dirs(PATHSUBSET+"/Subsets/10_PERCENT", listofchroms)
    subprocess.call("cp -rf {0} {1}".format(
        PATHSUBSET+"/Subsets/10_PERCENT/ ",
        PATHSUBSET+"/Subsets/1_PERCENT"),
        shell=True)
# Reorganise the files
for chroms in listchromsdirs:
    listsamples = uf.list_elements(chroms+"/", extension=".txt.gz")
    totalsamples = len(listsamples)
    for samples in range(int(math.floor(totalsamples*PROPTEST))):
        pick = random.choice(listsamples)
        if not os.path.isdir(PATHSUBSET+"/Subsets/FULL/Test/"+chroms.split("/")[-1]):
            os.mkdir(PATHSUBSET+"/Subsets/FULL/Test/"+chroms.split("/")[-1])
        subprocess.call(
            "mv {0} {1}".format(
                pick,
                PATHSUBSET+"/Subsets/FULL/Test/"+chroms.split("/")[-1]),
            shell=True)
        listsamples.remove(pick)
    for samples in range(int(math.floor(totalsamples*PROPVALID))):
        pick = random.choice(listsamples)
        if not os.path.isdir(PATHSUBSET+"/Subsets/FULL/Valid/"+chroms.split("/")[-1]):
            os.mkdir(PATHSUBSET+"/Subsets/FULL/Valid/"+chroms.split("/")[-1])
        subprocess.call(
            "mv {0} {1}".format(
                pick,
                PATHSUBSET+"/Subsets/FULL/Valid/"+chroms.split("/")[-1]),
            shell=True)
        listsamples.remove(pick)
    for samples in listsamples:
        if not os.path.isdir(PATHSUBSET+"/Subsets/FULL/Train/"+chroms.split("/")[-1]):
            os.mkdir(PATHSUBSET+"/Subsets/FULL/Train/"+chroms.split("/")[-1])
        subprocess.call(
            "mv {0} {1}".format(
                samples,
                PATHSUBSET+"/Subsets/FULL/Train/"+chroms.split("/")[-1]),
            shell=True)
# Cut the files to get training examples of similar size
# Filter 90% of the positions
subsets = uf.list_elements(PATHSUBSET + "/Subsets/FULL/", _type="dir")
for sub in subsets:
    for chroms in listofchroms:
        uf.cut_files(uf.list_elements(
            sub+"/"+chroms+"/",
            extension=".txt.gz"),
            SIZEFRAGMENTS,
            sub+"/"+chroms,
            copy=False)
    uf.mask_data(
        sub+"/",
        0.1,
        OUTPUTPATH=PATHSUBSET+"/Subsets/10_PERCENT/"+sub.split("/")[-1])
# Filter 90% of the positions of the prefiltered dataset
subsets = uf.list_elements(PATHSUBSET + "/Subsets/10_PERCENT/", _type="dir")
for sub in subsets:
    uf.mask_data(
        sub+"/",
        0.1,
        OUTPUTPATH=PATHSUBSET+"/Subsets/1_PERCENT/"+sub.split("/")[-1],
        PREFIXSUB="/1PER_")
subsets = uf.list_elements(PATHSUBSET+"/Subsets/FULL/", _type="dir")
for sub in subsets:
    if (
        not os.path.isdir(
                PATHSUBSET+"Subsets/10_PERCENT/"+sub.split("/")[-1]+"/Firstgen")
        and not (os.path.isdir(
                PATHSUBSET+"Subsets/10_PERCENT/"+sub.split("/")[-1]+"/Secondgen"))):
        os.mkdir(PATHSUBSET+"Subsets/10_PERCENT/"+sub.split("/")[-1]+"/Firstgen")
        os.mkdir(PATHSUBSET+"Subsets/10_PERCENT/"+sub.split("/")[-1]+"/Secondgen")
    uf.mask_data(
        sub+"/",
        0.1,
        OUTPUTPATH=PATHSUBSET+"Subsets/10_PERCENT/"+sub.split("/")[-1]+"/Firstgen")
    uf.mask_data(
        sub+"/",
        0.1,
        OUTPUTPATH=PATHSUBSET+"Subsets/10_PERCENT/"+sub.split("/")[-1]+"/Secondgen")
subsets = uf.list_elements(PATHSUBSET+"Subsets/10_PERCENT/", _type="dir")
for sub in subsets:
    subName = sub.split("/")[-1]
    generations = uf.list_elements(sub+"/", _type="dir")
    for gen in generations:
        generationName = gen.split("/")[-1]
        if not (os.path.isdir(PATHSUBSET+"Subsets/1_PERCENT/"+sub.split("/")[-1]+"/"+generationName)):
            os.mkdir(
                PATHSUBSET+"Subsets/1_PERCENT/"+sub.split("/")[-1]+"/"+generationName)
        uf.mask_data(
            sub+"/"+generationName+"/",
            0.1,
            OUTPUTPATH=PATHSUBSET+"Subsets/1_PERCENT/"+sub.split("/")[-1]+"/"+generationName+"/",
            PREFIXSUB="/1PER_")
