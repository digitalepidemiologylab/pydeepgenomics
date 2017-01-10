#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contains some functions to work on vcf files.

Adaptation and adding a few functions from
https://gist.github.com/slowkow/6215557
"""
import gzip
import os
import re
import shutil
import subprocess
import sys
from collections import OrderedDict

import pandas as pd

try:
    from Naked.toolshed.shell import execute_js, muterun_js
    success_import_naked = True
except ImportError as error:
    print(error)
    success_import_naked = False

try:
    import pydeepgenomics
    from pydeepgenomics.tools import generaltools as gt
except ImportError:
    cmd_dir = os.path.abspath(os.path.dirname(__file__)).split("alltests")[0]
    if cmd_dir not in sys.path:
        sys.path.append(cmd_dir)
    import pydeepgenomics
    from pydeepgenomics.tools import generaltools as gt

VCF_HEADER = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']

# Modified version of the one from vcf.py, allow to load a complete file into
# a dataframe.
# /!\ Don't load unfiltered vcf files with this function !


def dataframe(filename, large=True):
    if large:
        # Set the proper argument if the file is compressed.
        comp = 'gzip' if filename.endswith('.gz') else None
        # Count how many comment lines should be skipped.
        comments = _count_comments(filename)
        # Return a simple DataFrame without splitting the INFO column.
        return pd.read_table(
            filename,
            compression=comp,
            skiprows=comments,
            names=VCF_HEADER,
            usecols=range(8))

    # Each column is a list stored as a value in this dict. The keys for this
    # dict are the VCF column names and the keys in the INFO column.
    result = OrderedDict()
    # Parse each line in the VCF file into a dict.
    for i, line in enumerate(lines(filename)):
        for key in line.keys():
            # This key has not been seen yet, so set it to None for all
            # previous lines.
            if key not in result:
                result[key] = [None] * i
        # Ensure this row has some value for each column.
        for key in result.keys():
            result[key].append(line.get(key, None))

    return pd.DataFrame(result)


def lines(filename):
    """Open an optionally gzipped VCF file and generate an OrderedDict for
each line.
"""
    fn_open = gzip.open if filename.endswith('.gz') else open

    with fn_open(filename) as f_in:
        for line in f_in:
            if line.startswith('#'):
                continue
            else:
                yield parse(line)


def parse(line):
    """Parse a single VCF line and return an OrderedDict."""
    result = OrderedDict()
    fields = line.rstrip().split('\t')

    # Read the values in the first seven columns.
    for i, col in enumerate(VCF_HEADER[:7]):
        result[col] = _get_value(fields[i])

    # INFO field consists of "key1=value;key2=value;...".
    infos = fields[7].split(';')

    for i, info in enumerate(infos, 1):
        # info should be "key=value".
        try:
            key, value = info.split('=')
        # But sometimes it is just "value", so we'll make our own key.
        except ValueError:
            key = 'INFO{}'.format(i)
            value = info
        # Set the value to None if there is no value.
        result[key] = _get_value(value)

    return result

# Look at all the files in the list vcffiles and see if any snp in the refsnp
# dataframe is present


def find_matches(
        path_to_vcf_files,
        refsnps,
        prefix_to_chr_nb_in_name=None,
        suffix_to_chr_nb_in_name=".vcf.gz"):

    if prefix_to_chr_nb_in_name is None:
        prefix_to_chr_nb_in_name = path_to_vcf_files

    matching_references = pd.DataFrame()
    matching_positions = pd.DataFrame()

    for file in path_to_vcf_files:
        # Filter by chromosome to avoid testing all references on all files
        # + prevent from picking the same position for different chromosomes
        chrnb = int(re.sub(
            prefix_to_chr_nb_in_name,
            '',
            re.sub(suffix_to_chr_nb_in_name, '', file)))

        filtered_ref_snps = refsnps[refsnps.Chr == chrnb]
        ref_ids = filtered_ref_snps["SNP"].tolist()
        ref_positions = filtered_ref_snps["Position"].tolist()

        print("Loading file {} in a dataframe ...".format(file))
        chromosome_file = dataframe(file).drop(
            ["ALT", "REF", "QUAL", "FILTER", "INFO"],
            1)
        # Number of lines to shift to make dataframe index correspond with
        # lines in actual vcf file (comments + 1 (dataframe index starts at 0))
        skip = _count_comments(file) + 1
        chromosome_file["Corresponding row in vcf file"] = range(
            skip,
            chromosome_file.shape[0] + skip)

        print("Searching for matches with the reference dataframes...")
        new_matching_references = pd.concat((matching_references, chromosome_file[
            chromosome_file['ID'].isin(ref_ids)]))
        new_matching_positions = pd.concat((matching_positions, chromosome_file[
            chromosome_file["POS"].isin(ref_positions)]))

        print("{0} ref matching and {1} positions matching in {2}".format(
            new_matching_references.shape[0] - matching_references.shape[0],
            new_matching_positions.shape[0] - matching_positions.shape[0], file))

        matching_references = new_matching_references
        matching_positions = new_matching_positions
    print("Found {} matching ref of snps.".format(
        matching_references.shape[0]))
    print("Found {} matching positions of snps.".format(
        matching_positions.shape[0]))

    return matching_references, matching_positions


def _get_value(value):
    """Interpret null values and return ``None``. Return a list if the value
contains a comma.
"""
    if not value or value in ['', '.', 'NA']:
        return None
    if ',' in value:
        return value.split(',')
    return value


def _count_comments(filename):
    """Count comment lines (those that start with "#") in an optionally
gzipped file.
:param filename:  An optionally gzipped file.
"""
    comments = 0
    fn_open = gzip.open if filename.endswith('.gz') else open
    with fn_open(filename) as f_in:
        for line in f_in:
            try:
                is_comment = line.startswith('#')
            except TypeError:
                is_comment = line.startswith(b'#')
            if is_comment:
                comments += 1
            else:
                break

    return comments


def split_vcf_files(path_to_data, verbose=False):
    current_path = os.getcwd()
    shutil.copy(os.path.join(
        os.path.dirname(pydeepgenomics.__file__),
        "preprocess",
        "vcf",
        "split.js"), path_to_data)
    os.chdir(path_to_data)

    if verbose:
        if success_import_naked:
            success = execute_js(os.path.join(path_to_data, "split"))
            if not success:
                print("split.js did not ended correctly !")
                return
        else:
            with open(os.devnull, "w") as f:
                subprocess.call(
                    "node {}".format(os.path.join(path_to_data, "split")),
                    shell=True,
                    stdout=f)
    else:
        if success_import_naked:
            response = muterun_js(os.path.join(path_to_data, "split"))
            if response.exitcode != 0:
                print("split.js did not ended correctly !")
                return

        else:
            with open(os.devnull, "w") as f:
                subprocess.call(
                    "node {}".format(os.path.join(path_to_data, "split")),
                    shell=True,
                    stdout=f)
    os.remove(os.path.join(path_to_data, "split.js"))
    os.chdir(current_path)


def sort_chr_files_by_sample(
        path_to_data_by_chr,
        make_copy=False,
        force=False):
    if (
            not path_to_data_by_chr.endswith("split_by_chr") and
            not path_to_data_by_chr[:-1].endswith("split_by_chr") and
            not force):
        raise ValueError(
            "Directory name not recognized, directory name should be" +
            "split_by_chr")
    path_to_data_by_sample = os.path.join(os.path.dirname(
        path_to_data_by_chr),
        "split_by_sample")
    if not os.path.isdir(path_to_data_by_sample):
        os.mkdir(path_to_data_by_sample)
    else:
        shutil.rmtree(path_to_data_by_sample)
        os.mkdir(path_to_data_by_sample)
    chromosomes_dirs = gt.list_elements(path_to_data_by_chr, type_="dir")
    for folder in chromosomes_dirs:
        dir_name = os.path.basename(folder)
        files = gt.list_elements(folder, type_="file")
        for file in files:
            file_name = os.path.basename(file)
            destination = os.path.join(
                path_to_data_by_sample,
                file_name.split(".")[0])
            if not os.path.isdir(destination):
                os.mkdir(destination)
            new_name = os.path.join(destination, "chr"+dir_name+"_"+file_name)
            if make_copy:
                shutil.copy(file, new_name)
            else:
                shutil.move(file, new_name)
    if not make_copy:
        shutil.rmtree(path_to_data_by_chr)


def _concat_meta(path_in, path_out):
    meta_files = gt.list_elements(path_in, type_="file", extension=".txt.gz")
    header_written = False
    with gzip.open(os.path.join(path_out, "_meta.txt.gz"), 'wb') as out_file:
        for file in meta_files:
                with gzip.open(file, "rb") as in_file:
                    for line in in_file:
                        try:
                            is_comment = line.startswith('#')
                        except TypeError:
                            is_comment = line.startswith(b'#')
                        if not is_comment or not header_written:
                            out_file.write(line)
                            header_written = True


def _copy_comment(path_in, path_out):
    comment_files = gt.list_elements(path_in, extension=".txt")
    shutil.copy(
        os.path.join(path_in, comment_files[0]),
        os.path.join(path_out, "_comments.txt"))


def concatenate_split_files(
        path_to_input,
        tree_structure="by_sample",
        make_copy=False,
        force=False):
    if not force:
        if (
            (
                not path_to_input.endswith("split_by_chr") and
                not path_to_input[:-1].endswith("split_by_chr") and
                tree_structure == "by_chr") or
            (
                not path_to_input.endswith("split_by_sample") and
                not path_to_input[:-1].endswith("split_by_sample") and
                tree_structure == "by_sample")):
            raise ValueError(
                "Inconsistent combination of path and tree structure.\n" +
                "Received {0} and {1}".format(path_to_input, tree_structure))
        elif (tree_structure != "by_sample") and (tree_structure != "by_chr"):
            raise ValueError(
                "{0} is not managed by this function".format(tree_structure))

    path_to_concat_data = os.path.join(os.path.dirname(
        path_to_input),
        "split_and_concat_data")
    if not os.path.isdir(path_to_concat_data):
        os.mkdir(path_to_concat_data)
    else:
        shutil.rmtree(path_to_concat_data)
        os.mkdir(path_to_concat_data)

    list_users = gt.list_elements(
        path_to_input,
        type_="dir",
        exception=[os.path.join(
            path_to_input, "_meta"),
            os.path.join(path_to_input, "_comments")])

    _concat_meta(
        os.path.join(path_to_input, "_meta"),
        path_to_concat_data)

    _copy_comment(
        os.path.join(path_to_input, "_comments"),
        path_to_concat_data)

    for user in list_users:

        split_files = gt.list_elements(user, type_="file", extension=".txt.gz")
        name_user = os.path.basename(split_files[0])
        name_user = name_user.replace(
            re.sub("[^a-z\d]", "", re.search("^[^_]*", name_user).group(0)),
            "allchr")
        with gzip.open(
                os.path.join(path_to_concat_data, name_user), 'wb') as outfile:
            for file in split_files:
                with gzip.open(file, "rb") as infile:
                    outfile.write(infile.read())
        nb_lines_out = gt.get_nb_lines_file(
            os.path.join(path_to_concat_data, name_user))
        nb_lines_in = 0
        for file in split_files:
            nb_lines_in += gt.get_nb_lines_file(file)
        if nb_lines_in != nb_lines_out:
            sys.stderr.write(
                "Number of lines between original files and the\n" +
                "concatenated file does not match.\n" +
                "Origin: {0}, Concat: {1}\n".format(nb_lines_in, nb_lines_out))
        if not make_copy:
            shutil.rmtree(user)
    if not make_copy:
        shutil.rmtree(path_to_input)


def extract_snps_from_file(
        path_to_vcf_files,
        ref_snps_file,
        sep=",",
        chr_nb_prefix="",
        chr_nb_suffix=".vcf.gz"):

    """
    Load list of snp in a dataframe
    (column1 = snp ref name, column2 = chr, column3 = position)
    Also convert snpref to strings
    """

    # Clean previous results
    subprocess.call(
        "rm -rf " + os.path.join(path_to_vcf_files, "SelectionofSNPs"),
        shell=True)

    ref_snps = pd.read_csv(ref_snps_file, sep=sep)

    # Looking at the files present in the directory before working on them
    vcf_files = gt.list_elements(
        path_to_vcf_files,
        type_="file",
        extension=".vcf.gz")

    # Find the reference SNPs in the actual vcf files
    matching_references, matching_positions = find_matches(vcf_files, ref_snps)

    # Save the list of SNPs found
    if not os.path.isdir(os.path.join(path_to_vcf_files, "SelectionofSNPs")):
        os.mkdir(os.path.join(path_to_vcf_files, "SelectionofSNPs"))
    matching_positions.to_csv(
        path_or_buf=os.path.join(
            path_to_vcf_files,
            "SelectionofSNPs",
            "MatchingPositions.csv"),
        sep="\t",
        index=False)
    matching_references.to_csv(
        path_or_buf=os.path.join(
            path_to_vcf_files,
            "SelectionofSNPs",
            "MatchingReferences.csv"),
        sep="\t",
        index=False)

    for files in vcf_files:

        print("Starting to process file : {}".format(files))
        chrnb = int(re.sub(
            chr_nb_prefix,
            '',
            re.sub(chr_nb_suffix, '', files)))

        if not os.path.isdir(os.path.join(
                path_to_vcf_files, "SelectionofSNPs", "ID")):
            os.mkdir(os.path.join(path_to_vcf_files, "SelectionofSNPs", "ID"))

        if not os.path.isdir(os.path.join(
                path_to_vcf_files, "/SelectionofSNPs", "POS")):
            os.mkdir(os.path.join(path_to_vcf_files, "SelectionofSNPs", "POS"))

        output_file_id = os.path.join(
            path_to_vcf_files,
            "SelectionofSNPs",
            "ID",
            str(chrnb)+"_subset_ID.vcf")
        output_file_pos = os.path.join(
            path_to_vcf_files,
            "SelectionofSNPs",
            "POS",
            str(chrnb) + "_subset_POS.vcf")

        # Copy header and column labels in a subset file
        # (<chrnb>.subset_<type of selction criteria>.vcf) in
        # PATH/SelectionofSNPs

        with gzip.open(files, "r") as fi:
            with open(output_file_id, "w") as fo:
                for line in fi:
                    if line.startswith("#"):
                        fo.write(line)
                    else:
                        break
        subprocess.call(
            "cp {0} {1}".format(output_file_id, output_file_pos),
            shell=True)

        # Filter dataframe to have only snps corresponding to the file

        filtered_match_pos = matching_positions[
            matching_positions[VCF_HEADER[0]] == chrnb]
        filtered_match_ref = matching_references[
            matching_references[VCF_HEADER[0]] == chrnb]

        lines_from_origin_vcf = gzip.open(files, "r").readlines()
        out_pos = open(output_file_pos, 'a')
        out_id = open(output_file_id, 'a')
        it_positions = 0
        it_ids = 0

        print("Extract corresponding positions")
        for line_nb in filtered_match_pos["Corresponding row in vcf file"]:

            out_pos.write(lines_from_origin_vcf[line_nb-1])
            it_positions += 1
            print("Information on {0}/{1} matching positions copied".format(
                it_positions,
                matching_positions.shape[0]))

        print("Extract corresponding references")
        for line_nb in filtered_match_ref["Corresponding row in vcf file"]:
            out_id.write(lines_from_origin_vcf[line_nb-1])
            it_ids += 1
            print("Information on {0}/{1} matching references copied".format(
                it_ids,
                matching_references.shape[0]))

        out_pos.close()
        out_id.close()
        lines_from_origin_vcf.close()
        # compress the output file to .gz
        subprocess.call("gzip {}".format(output_file_pos), shell=True)
        subprocess.call("gzip {}".format(output_file_id), shell=True)
