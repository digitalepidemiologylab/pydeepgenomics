import os
import subprocess
import sys


cmd_subfolder = os.path.abspath(os.path.dirname(__file__)).split(
    "pydeepgenomics")[0]
try:
    from pydeepgenomics.preprocess.vcf import vcf
    from pydeepgenomics.tools import generaltools as gt
except ImportError:
    if cmd_subfolder not in sys.path:
        sys.path.append(cmd_subfolder)
    from pydeepgenomics.preprocess.vcf import vcf
    from pydeepgenomics.tools import generaltools as gt

PATH_TO_PLAYGROUND = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "playground")


def example_1(MAKE_COPY=True, VERBOSE=True):
    subprocess.call(
        "python "+os.path.join(os.path.dirname(__file__), "setup_ex_env.py"),
        shell=True)
    MAKE_COPY = True
    if VERBOSE:
        print("Concatenate vcf files ...")
    vcf.split_vcf_files(PATH_TO_PLAYGROUND, verbose=VERBOSE)
    vcf.sort_chr_files_by_sample(
        os.path.join(PATH_TO_PLAYGROUND, "split_by_chr"), make_copy=MAKE_COPY)
    vcf.concatenate_split_files(
        os.path.join(PATH_TO_PLAYGROUND, "split_by_sample"),
        make_copy=MAKE_COPY)


if __name__ == "__main__":
    example_1()
