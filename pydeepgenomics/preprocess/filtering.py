#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import gzip
import math
import os
import random
import subprocess
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


def do_subsets(
        path_data,
        path_subsets):

    list_chrom_dirs = gt.list_elements(path_data, type_="dir")
    list_of_chroms = [os.path.basename(chrom) for chrom in list_chrom_dirs]
    # Create the tree for the repartition of the dataset
    if not os.path.isdir(os.path.join(path_subsets, "Subsets")):
        os.mkdir(os.path.join(path_subsets, "Subsets"))
        os.mkdir(os.path.join(path_subsets, "Subsets", "FULL"))
        create_subsets_dirs(
            os.path.join(path_subsets, "Subsets", "FULL"), list_of_chroms)
        subprocess.call(
            "cp -rf {0} {1}".format(
                os.path.join(path_subsets, "Subsets", "FULL"),
                os.path.join(path_subsets, "Subsets", "10_PERCENT")),
            shell=True)
        subprocess.call("cp -rf {0} {1}".format(
                os.path.join(path_subsets, "Subsets", "FULL"),
                os.path.join(path_subsets, "Subsets", "1_PERCENT")),
            shell=True)
    elif not os.path.isdir(os.path.join(path_subsets, "Subsets", "FULL")):
        os.mkdir(os.path.join(path_subsets, "Subsets", "FULL"))
        create_subsets_dirs(
            os.path.join(path_subsets, "Subsets", "FULL"), list_of_chroms)
        subprocess.call(
            "rm -r {0}/10_PERCENT {0}/1_PERCENT".format(
                os.path.join(path_subsets, "Subsets")),
            shell=True)
        subprocess.call(
            "cp -rf {0} {1}".format(
                os.path.join(path_subsets, "Subsets", "FULL"),
                os.path.join(path_subsets, "Subsets", "10_PERCENT")),
            shell=True)
        subprocess.call(
            "cp -rf {0} {1}".format(
                os.path.join(path_subsets, "Subsets", "FULL"),
                os.path.join(path_subsets, "Subsets", "1_PERCENT")),
            shell=True)
    else:
        subprocess.call(
            "rm -r {0} {1}".format(
                os.path.join(path_subsets, "Subsets", "10_PERCENT"),
                os.path.join(path_subsets, "Subsets", "1_PERCENT")),
            shell=True)
        os.mkdir(os.path.join(path_subsets, "Subsets", "10_PERCENT"))
        create_subsets_dirs(
            os.path.join(path_subsets, "Subsets", "10_PERCENT"), list_of_chroms)
        subprocess.call("cp -rf {0} {1}".format(
            os.path.join(path_subsets, "Subsets", "10_PERCENT"),
            os.path.join(path_subsets, "Subsets", "1_PERCENT")),
            shell=True)
    # Reorganise the files
    for chrom in list_chrom_dirs:
        list_samples = gt.list_elements(chrom, extension=".txt.gz")
        total_samples = len(list_samples)
        for samples in range(int(math.floor(total_samples*proportions["test"]))):
            pick = random.choice(list_samples)
            if not os.path.isdir(
                    os.path.join(
                        path_subsets,
                        "Subsets",
                        "FULL",
                        "Test",
                        os.path.basename(chrom))):
                os.mkdir(
                    os.path.join(
                        path_subsets,
                        "Subsets",
                        "FULL",
                        "Test",
                        os.path.basename(chrom)))
            subprocess.call(
                "mv {0} {1}".format(
                    pick,
                    os.path.join(
                        path_subsets,
                        "Subsets",
                        "FULL",
                        "Test",
                        os.path.basename(chrom))),
                shell=True)
            list_samples.remove(pick)

        for samples in range(int(math.floor(total_samples*settings.PROPVALID))):
            pick = random.choice(list_samples)
            if not os.path.isdir(
                    os.path.join(
                        path_subsets,
                        "Subsets",
                        "FULL",
                        "Valid",
                        os.path.basename(chrom))):
                os.mkdir(
                    os.path.join(
                        path_subsets,
                        "Subsets",
                        "FULL",
                        "Valid",
                        os.path.basename(chrom)))
            subprocess.call(
                "mv {0} {1}".format(
                    pick,
                    os.path.join(
                        path_subsets,
                        "Subsets",
                        "FULL",
                        "Valid",
                        os.path.basename(chrom))),
                shell=True)
            list_samples.remove(pick)
        for samples in list_samples:
            if not os.path.isdir(
                    os.path.join(
                        path_subsets,
                        "Subsets",
                        "FULL",
                        "Train",
                        os.path.basename(chrom))):
                os.mkdir(
                    os.path.join(
                        path_subsets,
                        "Subsets",
                        "FULL",
                        "Train",
                        os.path.basename(chrom)))
            subprocess.call(
                "mv {0} {1}".format(
                    samples,
                    os.path.join(
                        path_subsets,
                        "Subsets",
                        "FULL",
                        "Train",
                        os.path.basename(chrom))),
                shell=True)
    # Cut the files to get training examples of similar size
    # Filter 90% of the positions
    subsets = gt.list_elements(
        os.path.join(path_subsets, "Subsets", "FULL"), type_="dir")
    for sub in subsets:
        for chrom in list_of_chroms:
            cut_files(gt.list_elements(
                os.path.join(sub, chrom),
                extension=".txt.gz"),
                settings.SIZEFRAGMENTS,
                os.path.join(sub, chrom),
                copy=False)
        mask_data(
            sub,
            0.1,
            path_output=os.path.join(
                path_subsets, "Subsets", "10_PERCENT", os.path.basename(sub)))
    # Filter 90% of the positions of the prefiltered dataset
    subsets = gt.list_elements(
        os.path.join(path_subsets, "Subsets", "10_PERCENT"), type_="dir")
    for sub in subsets:
        mask_data(
            sub,
            0.1,
            path_output=os.path.join(
                path_subsets, "Subsets", "1_PERCENT", os.path.basename(sub)),
            prefix_subset="1PER_")
    subsets = gt.list_elements(
        os.path.join(path_subsets, "Subsets", "FULL", type_="dir"))
    for sub in subsets:
        if (
            not os.path.isdir(
                    os.path.join(
                        path_subsets,
                        "Subsets",
                        "10_PERCENT",
                        os.path.basename(sub),
                        "Firstgen"))
            and not (os.path.isdir(
                    os.path.join(
                        path_subsets,
                        "Subsets",
                        "10_PERCENT",
                        os.path.basename(sub),
                        "Secondgen")))):
            os.mkdir(os.path.join(
                path_subsets,
                "Subsets",
                "10_PERCENT",
                os.path.basename(sub),
                "Firstgen"))
            os.mkdir(os.path.join(
                path_subsets,
                "Subsets",
                "10_PERCENT",
                os.path.basename(sub),
                "Secondgen"))
        mask_data(
            sub,
            0.1,
            path_output=os.path.join(
                path_subsets,
                "Subsets",
                "10_PERCENT",
                os.path.basename(sub),
                "Firstgen"))
        mask_data(
            sub,
            0.1,
            path_output=os.path.join(
                path_subsets,
                "Subsets",
                "10_PERCENT",
                os.path.basename(sub),
                "Secondgen"))
    subsets = gt.list_elements(
        os.path.join(path_subsets, "Subsets", "10_PERCENT"),
        type_="dir")
    for sub in subsets:
        sub_name = os.path.basename(sub)
        generations = gt.list_elements(sub, type_="dir")
        for gen in generations:
            generation_name = os.path.basename(gen)
            if not (os.path.isdir(os.path.join(
                    path_subsets,
                    "Subsets",
                    "1_PERCENT",
                    sub_name,
                    generation_name))):
                os.mkdir(
                    os.path.join(
                        path_subsets,
                        "Subsets",
                        "1_PERCENT",
                        sub_name,
                        generation_name))
            mask_data(
                os.path.join(sub, generation_name),
                0.1,
                path_output=os.path.join(
                    path_subsets,
                    "Subsets",
                    "1_PERCENT",
                    sub_name,
                    generation_name),
                prefix_subset="1PER_")


def cut_files(file_list, size_of_output_files, output_path, copy=True):
    for file in file_list:
        filename = file.split("/")[-1].split(".")[0]
        nblines = gt.get_nb_lines_file(file)
        nboffiles = math.ceil(nblines / size_of_output_files)
        overlapping = math.floor(
            (size_of_output_files - nblines % size_of_output_files) / nboffiles)

        begin = 0
        for i in range(int(nboffiles)):
            end = int(min(begin + size_of_output_files, nblines))
            if end - begin < size_of_output_files:
                begin = int(end - size_of_output_files)
            subsetoflines = range(begin, end)
            begin += int(size_of_output_files - overlapping)

            with open(output_path + "/" + filename + "-" + str(i + 1) + ".txt",
                      "w") as \
                    outfile, gzip.open(file, "rt") as infile:

                lines = infile.readlines()
                for index in subsetoflines:
                    outfile.write(lines[index])
            subprocess.call("gzip {}".format(
                output_path + "/" + filename + "-" + str(i + 1) + ".txt"),
                shell=True)

        if not copy:
            subprocess.call("rm {}".format(file), shell=True)


def _build_output_tree_struct(path_in, path_out):

    for (sub_path, _, _) in os.walk(path_in):

        out = sub_path.replace(path_in, path_out)
        os.makedirs(out)


def mask_data(
        path_data,
        fraction_pass,
        path_output=None,
        prefix_subset=None,
        verbose=False,
        logging=False):

    """ fraction_pass = nb between 0 and 1
    This function builds the output directory based on the name of the input dir
    and the prefix.
    """
    print("Starting to filter data from {0} at {1}. ({2} pass)".format(
        path_data,
        datetime.datetime.now(),
        fraction_pass))

    if prefix_subset is None:
        prefix_subset = str(int(100*fraction_pass)) + "PER_"
    out_dir_name = prefix_subset + os.path.basename(path_data)
    if path_output is None:
        path_output = os.path.join(os.path.dirname(path_data), out_dir_name)
    _build_output_tree_struct(path_data, path_output)

    i = 0

    chromosomes = gt.list_elements(path_data, type_='dir', exception=[
        os.path.join(path_data, "floatfiles"),
        os.path.join(path_data, "encodeddata"),
        os.path.join(path_data, "Subsets")])

    for chrom in chromosomes:

        chrom_name = os.path.basename(chrom)
        files = gt.list_elements(chrom, extension='.txt.gz')

        for sample in files:

            name_sample = sample.split("/")[-1].split(".")[0].split("_")[-1]
            nb_lines = gt.get_nb_lines_file(sample)
            subset_of_lines = random.sample(
                range(nb_lines),
                int(math.floor(nb_lines * fraction_pass)))

            with gzip.open(sample, "rt") as infile,\
                open(os.path.join(
                        path_output,
                        chrom_name,
                        prefix_subset+name_sample+".txt"),
                     "w") as outfile:

                lines = infile.readlines()

                for index in subset_of_lines:
                    outfile.write(lines[index])
            subprocess.call("gzip {}".format(os.path.join(
                    path_output,
                    chrom_name,
                    prefix_subset+name_sample+".txt")),
                shell=True)

            if not logging:
                i += 1
                gt.print_progress(
                    i,
                    len(chromosomes)*len(files)-1,
                    decimals=3)
            elif verbose:
                print(
                    "{0}/{1} files tested. Date : {2}".format(
                        i,
                        len(chromosomes)*len(files),
                        str(datetime.datetime.now())))

    print(
        "\nData from {0} filtered at {1}. ({2} pass)".format(
            path_data,
            datetime.datetime.now(),
            fraction_pass))

