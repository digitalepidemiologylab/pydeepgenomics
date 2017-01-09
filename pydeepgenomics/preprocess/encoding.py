#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import threading
import math
import random
import sys

import pandas as pd

cmd_subfolder = os.path.abspath(
    os.path.dirname(__file__)).split("pydeepgenomics")[0]
try:
    from pydeepgenomics.tools import generaltools as gt
    from pydeepgenomics.preprocess import settings
except ImportError:
    if cmd_subfolder not in sys.path:
        sys.path.append(cmd_subfolder)
    from pydeepgenomics.tools import generaltools as gt
    from pydeepgenomics.preprocess import settings


def write_encoded_output(
        path_data,
        chromosome,
        dataframe,
        sve,
        liste_names,
        namedir="floatfiles"):
    for i in range(len(liste_names)):
        # First allele encoding
        # REF
        dataframe.loc[
            ((dataframe.REF == "A") &
             (dataframe.loc[:, liste_names[i]].str[0] == "0")),
            "output" + liste_names[i]] = sve[0]
        dataframe.loc[
            ((dataframe.REF == "T") &
             (dataframe.loc[:, liste_names[i]].str[0] == "0")),
            "output" + liste_names[i]] = sve[1]
        dataframe.loc[
            ((dataframe.REF == "G") &
             (dataframe.loc[:, liste_names[i]].str[0] == "0")),
            "output" + liste_names[i]] = sve[2]
        dataframe.loc[
            ((dataframe.REF == "C") &
             (dataframe.loc[:, liste_names[i]].str[0] == "0")),
            "output" + liste_names[i]] = sve[3]
        # ALT
        dataframe.loc[
            ((dataframe.ALT == "A") &
             (dataframe.loc[:, liste_names[i]].str[0] == "1")),
            "output" + liste_names[i]] = sve[0]
        dataframe.loc[
            ((dataframe.ALT == "T") &
             (dataframe.loc[:, liste_names[i]].str[0] == "1")),
            "output" + liste_names[i]] = sve[1]
        dataframe.loc[
            ((dataframe.ALT == "G") &
             (dataframe.loc[:, liste_names[i]].str[0] == "1")),
            "output" + liste_names[i]] = sve[2]
        dataframe.loc[
            ((dataframe.ALT == "C") &
             (dataframe.loc[:, liste_names[i]].str[0] == "1")),
            "output" + liste_names[i]] = sve[3]

        # Second allele encoding
        # REF
        dataframe.loc[
            ((dataframe.REF == "A") &
             (dataframe.loc[:, liste_names[i]].str[-1] == "0")),
            "output" + liste_names[i]] += sve[4]
        dataframe.loc[
            ((dataframe.REF == "T") &
             (dataframe.loc[:, liste_names[i]].str[-1] == "0")),
            "output" + liste_names[i]] += sve[5]
        dataframe.loc[
            ((dataframe.REF == "G") &
             (dataframe.loc[:, liste_names[i]].str[-1] == "0")),
            "output" + liste_names[i]] += sve[6]
        dataframe.loc[
            ((dataframe.REF == "C") &
             (dataframe.loc[:, liste_names[i]].str[-1] == "0")),
            "output" + liste_names[i]] += sve[7]
        # ALT
        dataframe.loc[
            ((dataframe.ALT == "A") &
             (dataframe.loc[:, liste_names[i]].str[-1] == "1")),
            "output" + liste_names[i]] += sve[4]
        dataframe.loc[
            ((dataframe.ALT == "T") &
             (dataframe.loc[:, liste_names[i]].str[-1] == "1")),
            "output" + liste_names[i]] += sve[5]
        dataframe.loc[
            ((dataframe.ALT == "G") &
             (dataframe.loc[:, liste_names[i]].str[-1] == "1")),
            "output" + liste_names[i]] += sve[6]
        dataframe.loc[
            ((dataframe.ALT == "C") &
             (dataframe.loc[:, liste_names[i]].str[-1] == "1")),
            "output" + liste_names[i]] += sve[7]

        # Add position
        dataframe.loc[:, "output" + liste_names[i]] += dataframe.POS

    # Write files

    if len(liste_names) > 1:
        jobs = []
        for i in range(len(liste_names)):
            thread = threading.Thread(target=save_samples(
                path_data,
                chromosome,
                dataframe,
                liste_names,
                i,
                name_dir=namedir))
            jobs.append(thread)
        for j in jobs:
            j.start()
        for j in jobs:
            j.join()
    else:
        save_samples(
            path_data,
            chromosome,
            dataframe,
            liste_names,
            0,
            name_dir=namedir)


def decode_position(to_test, ln):
    fbp = math.pow(2, 28)
    enc_al1 = fbp
    enc_al2 = math.pow(2, 31)
    position = 0
    _iter = 20
    al1 = al2 = "N"

    while (
            (to_test - enc_al2 - enc_al1 - position != 0) and
            (enc_al1 <= math.pow(2, 33) and (enc_al2 <= math.pow(2, 37))) and
            (_iter > 0)
    ):

        if (
            (enc_al2 * 2 < to_test) and
            (enc_al1 == math.pow(2, 28)) and
            (position == 0)
        ):

            enc_al2 *= 2
            al2 = ln[enc_al2]
        elif (enc_al1 * 2 + enc_al2 < to_test) and (position == 0):
            enc_al1 *= 2
            al1 = ln[enc_al1]
        elif to_test - enc_al1 - enc_al2 < fbp:
            position = int(to_test - enc_al1 - enc_al2)
        _iter -= 1

    if _iter <= 0:
        position = -1
    return al1[0], al2[0], position


def save_samples(
        path_data,
        chromosome,
        dataframe,
        list_names,
        i,
        name_dir="floatfiles"):
    # Save
    dataframe.loc[:, ["output" + list_names[0]]].to_csv(
        os.path.join(path_data, name_dir, chromosome, list_names[i] + ".txt.gz"),
        index=False,
        header=False,
        compression="gzip")


def _build_output_tree_structure(
        path_to_output,
        name_output_dir,
        chromosome_name):
    if not os.path.isdir(os.path.join(path_to_output, name_output_dir)):
        os.mkdir(os.path.join(path_to_output, name_output_dir))
    if not os.path.isdir(
            os.path.join(path_to_output, name_output_dir, chromosome_name)):
        os.mkdir(
            os.path.join(path_to_output, name_output_dir, chromosome_name))


def _custom_output(text, print_parameters):

    if print_parameters["verbose"] and\
            print_parameters["printing"]and\
            print_parameters["in_loop"]:
        print(text, end="\r")
    elif print_parameters["verbose"] and print_parameters["printing"]:
        print(text)


def encode_file_positions(
        chr_to_be_processed,
        path_to_data,
        path_to_output,
        name_output_dir="encoded_files",
        verbose=True,
        printing=True,
        logging=False):

    # Start timer
    timer = gt.time_since_first_call()
    timer.__next__()
    print_parameters = {
        "verbose": verbose,
        "printing": printing,
        "logging": logging,
        "in_loop": False
    }

    _custom_output(
        "\nFunction {0} started at {1}".format(
            encode_file_positions.__name__,
            str(datetime.datetime.now())) +
        "\nProcessing files in {0}:".format(path_to_data), print_parameters)

    chromosome_name = str(chr_to_be_processed)
    _build_output_tree_structure(
        path_to_output,
        name_output_dir,
        chromosome_name)

    # load the meta data in a pandas data frame
    _meta = pd.read_csv(
        os.path.join(path_to_data, "_meta.txt.gz"),
        sep="\t",
        index_col=False)
    list_files = gt.list_elements(
        path_to_data,
        extension=".txt.gz",
        exception=[
            os.path.join(path_to_data, "_meta.txt.gz"),
            os.path.join(path_to_data, "_comments.txt.gz")])

    nb_processed_files = 0
    batch_iter = 0
    list_ = []
    df = _meta.drop(["#CHROM", "ID", "QUAL", "FILTER", "INFO", "FORMAT"], 1)

    for files in list_files:
        print_parameters["in_loop"] = True
        sample_name = files.split("/")[-1].split(".")[0].split("_")[-1]
        list_.append(sample_name)

        df[sample_name] = pd.read_csv(files, index_col=None, header=None)

        if (batch_iter < settings.FILEBATCHSIZE - 1) and \
                (files is not list_files[-1]):
            batch_iter += 1
        else:
            # Reinitialize stuff
            write_encoded_output(
                path_to_output,
                chromosome_name,
                df,
                settings.SVE,
                list_,
                namedir=name_output_dir)
            batch_iter = 0
            list_ = []
            df = _meta.drop(
                ["#CHROM", "ID", "QUAL", "FILTER", "INFO", "FORMAT"], 1)
            nb_processed_files += settings.FILEBATCHSIZE

            h, m, s = timer.__next__()
            _custom_output(
                "\r{0}/{1}".format(nb_processed_files, len(list_files)) +
                " files processed after {0}h{1}m{2}s.".format(h, m, s) +
                " Date: {}".format(str(datetime.datetime.now())),
                print_parameters)

    print_parameters["in_loop"] = False
    sys.stdout.write("\n")
    h, m, s = timer.__next__()
    _custom_output(
        "Finished after {0}h{1}m{2}s.\n".format(h, m, s),
        print_parameters)


def verify_decoding(
        path_to_original_data,
        path_to_encoded_data,
        chromosome_verified,
        max_nb_of_files_to_test=100,
        nb_of_tests_per_file=100,
        verbose=True,
        printing=True,
        logging=False):

    print_parameters = {
        "verbose": verbose,
        "printing": printing,
        "logging": logging,
        "in_loop": False
    }

    errors_file = []
    errors_sup_pos = []
    errors_real_pos = []
    errors_type = []
    errors_prev_pos = []
    errors_next_pos = []

    _custom_output(
        "\nFunction {0} started at {1}".format(
            verify_decoding.__name__,
            str(datetime.datetime.now())) +
        "\nTesting files in {0}:".format(
            path_to_encoded_data),
        print_parameters)
    timer = gt.time_since_first_call()
    timer.__next__()

    _meta = pd.read_csv(
        os.path.join(
            path_to_original_data,
            chromosome_verified,
            "_meta.txt.gz"),
        sep="\t",
        index_col=False).drop(
        ["#CHROM", "ID", "QUAL", "FILTER", "INFO", "FORMAT"], 1)

    files = gt.list_elements(
        os.path.join(
            path_to_encoded_data,
            chromosome_verified),
        extension=".txt.gz")

    print_parameters["in_loop"] = True
    for j in range(min(max_nb_of_files_to_test, len(files))):
        testfile = random.choice(files)
        name = testfile.split("/")[-1].split(".")[0]
        _meta["originaldata"] = pd.read_csv(
            os.path.join(
                path_to_original_data,
                chromosome_verified,
                name+"_"+name+".txt.gz"),
            index_col=None, header=None)
        _meta["totest"] = pd.read_csv(testfile, index_col=None, header=None)
        for i in range(nb_of_tests_per_file):
            to_test = random.choice(_meta.totest.tolist())
            allele_1, allele_2, position = decode_position(
                float(to_test),
                settings.LN)

            if position == -1:
                index = _meta.loc[
                        (_meta.totest == to_test), :].index.tolist()[0]
                errors_file.append(testfile)
                errors_sup_pos.append(position)
                errors_real_pos.append(_meta.iloc[max(index, 0), 0])
                errors_type.append("Impossible to decode")
                errors_prev_pos.append(_meta.iloc[max(index - 1, 0), 0])
                errors_next_pos.append(
                    _meta.iloc[min(index + 1, _meta.shape[0]), 0])

                _custom_output("{0}/{1} files tested. Date : {2}".format(
                    j+1,
                    min(max_nb_of_files_to_test, len(files)),
                    str(datetime.datetime.now())),
                    print_parameters)
                continue
            original_alleles =\
                _meta.loc[(_meta.totest == to_test), :]["originaldata"].tolist()[0].split("/")
            original_pos =\
                _meta.loc[(_meta.totest == to_test), :]["POS"].tolist()[0]
            ref = _meta.loc[(_meta.totest == to_test), :]["REF"].tolist()[0]
            alt = _meta.loc[(_meta.totest == to_test), :]["ALT"].tolist()[0]
            if position != original_pos:
                index = _meta.loc[
                        (_meta.totest == to_test), :].index.tolist()[0]
                errors_file.append(testfile)
                errors_sup_pos.append(position)
                errors_real_pos.append(_meta.iloc[max(index, 0), 0])
                errors_type.append("Position")
                errors_prev_pos.append(_meta.iloc[max(index - 1, 0), 0])
                errors_next_pos.append(
                    _meta.iloc[min(index + 1, _meta.shape[0]), 0])
            if ((original_alleles[0] == 0) and (allele_1 != ref)) or\
                    ((original_alleles[0] == 1) and (allele_1 != alt)):
                index = _meta.loc[
                        (_meta.totest == to_test), :].index.tolist()[0]
                errors_file.append(testfile)
                errors_sup_pos.append(position)
                errors_real_pos.append(_meta.iloc[max(index, 0), 0])
                errors_type.append("Allele 1")
                errors_prev_pos.append(_meta.iloc[max(index - 1, 0), 0])
                errors_next_pos.append(
                    _meta.iloc[min(index + 1, _meta.shape[0]), 0])
            if ((original_alleles[-1] == 0) and (allele_1 != alt)) or\
                    ((original_alleles[-1] == 1) and (allele_1 != alt)):

                index = _meta.loc[
                        (_meta.totest == to_test), :].index.tolist()[0]
                errors_file.append(testfile)
                errors_sup_pos.append(position)
                errors_real_pos.append(_meta.iloc[max(index, 0), 0])
                errors_type.append("Allele 2")
                errors_prev_pos.append(_meta.iloc[max(index - 1, 0), 0])
                errors_next_pos.append(
                    _meta.iloc[min(index + 1, _meta.shape[0]), 0])

        h, m, s = timer.__next__()
        _custom_output(
            "{0}/{1} files tested ".format(
                j+1,
                min(max_nb_of_files_to_test, len(files))) +
            "after  {0}h{1}m{2}s. ".format(h, m, s) +
            "Date : {0}".format(str(datetime.datetime.now())),
            print_parameters)

    print_parameters["in_loop"] = False

    errors = pd.DataFrame({"File": errors_file,
                           "Supposed_position": errors_sup_pos,
                           "Real_position": errors_real_pos,
                           "Error_type": errors_type,
                           "Previous_positions": errors_prev_pos,
                           "Next_position": errors_next_pos})
    if not errors.empty:
        errors_al_1 = errors.loc[(errors.Error_type == "Allele 1"), :].shape[0]
        errors_al_2 = errors.loc[(errors.Error_type == "Allele 2"), :].shape[0]
        errors_pos = errors.loc[(errors.Error_type == "Position"), :].shape[0]
        impossible_to_decode =\
            errors.loc[
                (errors.Error_type == "Impossible to decode"), :].shape[0]
        total_error = errors.shape[0]
        _custom_output(
            "\nAllele 1 errors: {}".format(errors_al_1) +
            "\nAllele 2 errors: {}".format(errors_al_2) +
            "\nPosition errors: {}".format(errors_pos) +
            "\nImpossible to decode: {}".format(impossible_to_decode) +
            "\nTotal errors: {}".format(total_error) +
            "\nIn total: {}% errors !\n".format(
                100*total_error/(nb_of_tests_per_file*min(
                    max_nb_of_files_to_test,
                    len(files)))),
            print_parameters
        )
        print("Date : {}".format(str(datetime.datetime.now())))
        errors.to_csv(
            "Errors_found_in{}.csv".format(chromosome_verified), sep="\t")
    else:
        _custom_output("\nNo error found !", print_parameters)
