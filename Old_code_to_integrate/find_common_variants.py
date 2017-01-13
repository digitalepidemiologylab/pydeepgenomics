##!/usr/bin/env python
## -*- coding: utf-8 -*-
#import os
#import sys#

#import pandas as pd#

#PATH_TO_ROOT_OF_MODULE = os.path.abspath(os.path.join(os.getcwd(), ".."))
#sys.path.append(PATH_TO_ROOT_OF_MODULE)#

#cmd_subfolder = os.path.abspath(os.path.dirname(__file__)).split(
#    "Old_code_to_integrate")[0]
#try:
#    from pydeepgenomics.tools import generaltools as gt
#    from pydeepgenomics.tools.generaldecorators import outdated
#except ImportError:
#    if cmd_subfolder not in sys.path:
#        sys.path.append(cmd_subfolder)
#    from pydeepgenomics.tools import generaltools as gt
#    from pydeepgenomics.tools.generaldecorators import outdated#
#

#@outdated
#def find_common_variants_in_vcf(path_to_selection_of_snps, header=6):#

#    nb_shared_variants_in_total = 0
#    nb_diff_variants_in_total = 0
#    vcf_files = gt.list_elements(path_to_selection_of_snps, extension=".vcf.gz")#

#    for files in vcf_files:
#        nb_shared_variants_in_file = 0
#        nb_diff_variants_in_file = 0
#        df_chr = pd.read_csv(
#            files, header=header, compression="gzip", sep="\t").drop([
#                "#CHROM",
#                "POS",
#                "ID",
#                "REF",
#                "ALT",
#                "QUAL",
#                "FILTER",
#                "INFO",
#                "FORMAT"], 1)
#        for index, row in df_chr.iterrows():
#            if len(row.unique()) == 1:
#                nb_shared_variants_in_file += 1
#            else:
#                nb_diff_variants_in_file += 1
#        nb_shared_variants_in_total += nb_shared_variants_in_file
#        nb_diff_variants_in_total += nb_diff_variants_in_file
#        print("{0} variants and {1} shared position in file {2}".format(
#            nb_diff_variants_in_file,
#            nb_shared_variants_in_file,
#            files))#

#if __name__ == "__main__":
#    find_common_variants_in_vcf("./")
