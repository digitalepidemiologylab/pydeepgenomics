#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys

cmd_subfolder = os.path.abspath(os.path.dirname(__file__)).split(
    "pydeepgenomics")[0]
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


@gd.accepts(str, (list, tuple))
def create_subsets_dirs(path_to_dirs, list_of_chrs):

    for chrom in list_of_chrs:
        os.makedirs(os.path.join(path_to_dirs, "Train", chrom))
        os.makedirs(os.path.join(path_to_dirs, "Test", chrom))
        os.makedirs(os.path.join(path_to_dirs, "Valid", chrom))


@gd.accepts(str, str, (dict, None), bool)
def make_subsets(path_data, path_subsets, proportions=None, copy=False):

    if proportions is None:
        proportions = {
            "test": settings.PROPTEST,
            "train": settings.PROPTRAIN,
            "valid": settings.PROPVALID}
    if copy:
        moving = shutil.copy
    else:
        moving = shutil.move

    list_chroms = gt.list_elements(path_data, type_="dir")
    list_chroms_names = [os.path.basename(i).split(".")[0] for i in list_chroms]

    create_subsets_dirs(path_subsets, list_chroms_names)

    for index_1, (chrom, chrom_name) in enumerate(
            zip(list_chroms, list_chroms_names)):

        files = gt.list_elements(
            chrom,
            type_="file",
            extension=".txt.gz",
            exception=[os.path.join(chrom, "_meta.txt.gz")])

        subsets = gt.random_chunks(files, (
            proportions["test"],
            proportions["train"],
            proportions["valid"]))

        test_files, train_files, valid_files = subsets

        test_files_out = [os.path.join(
            path_subsets,
            "Test",
            chrom_name) for _ in range(len(test_files))]
        train_files_out = [os.path.join(
            path_subsets,
            "Train",
            chrom_name) for _ in range(len(train_files))]
        valid_files_out = [os.path.join(
            path_subsets,
            "Valid",
            chrom_name) for _ in range(len(valid_files))]

        for index_2, (in_, out_) in enumerate(
                zip(
                    test_files+train_files+valid_files,
                    test_files_out+train_files_out+valid_files_out)):
            moving(in_, out_)
        shutil.move(
            os.path.join(chrom, "_meta.txt.gz"),
            os.path.join(path_subsets, "_meta_"+chrom_name+".txt.gz"))
        shutil.move(
            os.path.join(chrom, "_comments.txt"),
            os.path.join(path_subsets, "_comments_"+chrom_name+".txt"))
