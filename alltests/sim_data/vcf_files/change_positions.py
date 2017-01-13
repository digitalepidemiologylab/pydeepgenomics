#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip
import math
import os
import random
import sys

try:
    from pydeepgenomics.tools import generaltools as gt
except ImportError:
    cmd_dir = os.path.abspath(os.path.dirname(__file__)).split("alltests")[0]
    if cmd_dir not in sys.path:
        sys.path.append(cmd_dir)
    from pydeepgenomics.tools import generaltools as gt

if __name__ == "__main__":

    prob_rich_region_to_normal = 0.03
    prob_normal_to_rich_region = 0.03

    files = gt.list_elements(os.path.abspath("."),  extension=".vcf")
    header_size = 6

    for index_f, file in enumerate(files):

        size = gt.get_nb_lines_file(file) - header_size
        size_chromosome_a_priori = 200000 / math.pow(1.1, index_f)
        mean_distance = size_chromosome_a_priori / size

        with open(file, "r") as in_file, gzip.open(file+".gz", "wb") as out_file:

            in_rich = False
            position = 0
            for index_l, line in enumerate(in_file):

                if in_rich:
                    position += max(1, random.gauss(mean_distance/3, mean_distance/10))
                    if random.random() < prob_rich_region_to_normal:
                        in_rich = False
                else:
                    position += max(1, random.gauss(mean_distance * 1.5, mean_distance/5))
                    if random.random() < prob_normal_to_rich_region:
                        in_rich = True
                position = int(position)

                pattern_in_line = str(1) + "\t" + str(index_l - 5) + "\t" + "QTL"
                pattern_out_line = str(index_f + 1) + "\t" + str(position) + "\t" + "QTL"

                out_line = line.replace(pattern_in_line, pattern_out_line)
                out_file.write(out_line.encode())

    os.remove(file)
