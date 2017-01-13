#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contains functions used in most of the packages of this project.

The functions designed in this modules are not specific to the project and are
used in a lot of the modules.

.. moduleauthor:: Theo Dupuis
"""
import doctest
import glob
import gzip
import math
import os
import random
import re
import sys
import time

from itertools import chain, islice

cmd_subfolder = sys.path.append(
    os.path.dirname(os.path.abspath(__file__)).split("pydeepgenomics")[0])
try:
    from pydeepgenomics.tools import generaldecorators as gd
except ImportError:
    if cmd_subfolder not in sys.path:
        sys.path.append(cmd_subfolder)
    from pydeepgenomics.tools import generaldecorators as gd



@gd.accepts(str, (str, None), str, bool, str, (list, tuple, None))
def list_elements(
        path_to_folder,
        type_=None,
        extension="",
        sort="natural",
        exception=None,
        verbose=False):
    """Lists the items in a given folder with a few filters.

    This function lists all the elements in the folder given.
    You can choose to select only one type of object with :code:`type_`. It is
    also possible to look only for the objects ending with a specific
    string given to :code:`extension`.
    The output is a list that can be sorted by alphanumerical or natural
    order with :code:`sort`
    VERBOSE makes the function print all the
    files found in the specified path (by default VERBOSE=False), It is
    possible to sort the list of files by natural order before it is
    returned with :code:`sort="natural"` (activated by default) or
    alphanumerical order.

    Args:
        path_to_folder (:obj:`str`): Complete or relative path to the folder\
         you want to explore.

        type_ (:obj:`str|None`, optional): Type of items you want to list,\
         can be :code:`"dir"`, :code:`"file"` or :code:`None` (default\
         behavior). When set to :code:`None`, the function does not care\
         about the type and returns all items.

        extension (:obj:`str`, optional): Adds a filter to the function to\
         only return the items whose name finish with the string given to\
         extension. By default extension is an empty string.

        sort (:obj:`str`, optional): Indicates how the output list is\
         sorted. By default, the output is sorted by natural order (\
         :code:`sort="natural"`). It can also be set to\
         :code:`sort="alphanumeric"`.

        exception (:obj:`list|tuple|None`, optional): List or tuple of\
         specific items to ignore. None by default

        verbose (:obj:`bool`, optional): Makes the function print more\
         information (by default :code:`verbose=False`).

    Returns:
        :obj:`list`:

    Raises:
        AssertError: Raised when the types of the arguments are not respected.

    Examples:
        To get the list of the vcf files in the current directory:
            >>> # Indicate path to example data (depends on the repo structure)
            >>> path_to_root_repo = os.path.abspath(os.path.join(
            ...                             os.path.dirname(__file__),
            ...                             "..",
            ...                             ".."))
            >>> path_ = os.path.join(
            ...         path_to_root_repo,
            ...         "alltests",
            ...         "sim_data",
            ...         "vcf_files")
            >>> # List the files of interest
            >>> elements = list_elements(path_, extension=".vcf.gz")
            >>> expected_out = [
            ...     os.path.join(path_, '1.vcf.gz'),
            ...     os.path.join(path_, '2.vcf.gz'),
            ...     os.path.join(path_, '3.vcf.gz')]
            >>> elements == expected_out
            True

        Similarly, with relative paths:
            >>> # Save the current path and go to the folder containg the module
            >>> cwd = os.getcwd()
            >>> os.chdir(os.path.dirname(__file__))
            >>> # Indicate path to example data (depends on the repo structure)
            >>> path_to_root_repo = os.path.join("..", "..")
            >>> path_ = os.path.join(
            ...         path_to_root_repo,
            ...         "alltests",
            ...         "sim_data",
            ...         "vcf_files")
            >>> elements = list_elements(path_, extension=".vcf.gz")
            >>> expected_out = [
            ...     os.path.join(path_, '1.vcf.gz'),
            ...     os.path.join(path_, '2.vcf.gz'),
            ...     os.path.join(path_, '3.vcf.gz')]
            >>> elements == expected_out
            True
            >>> # Return to previous directory
            >>> os.chdir(cwd)

    Todo:
        * Make it cleaner and easier to read :
            * Reduce redundancy
            * Outsource the prints to :code:`custom_output` when this
              function is moved to the current module.
        * add some modularity ?
        * Raise exceptions when incorrect parameters are given (Wrong
          string, inconsitent value etc.)
    """

    if exception is None:
        exception = []
    file_list = []
    iterator_dirs = 0
    iterator_files = 0
    # List all files
    if type_ == "file" or type_ is None:
        for files in glob.glob(os.path.join(path_to_folder, '*'+extension)):
            if os.path.isfile(files) and (files not in exception):
                iterator_files += 1
                file_list.append(files)
                if verbose:
                    print("File found at {0} : {1}".format(
                        path_to_folder, files))

        if verbose:
            print("Number of{0} files found in {1} : {2}".format(
                extension, path_to_folder, iterator_files))

    # List all directories
    if type_ == "dir" or type_ is None:
        for files in glob.glob(os.path.join(path_to_folder, '*'+extension)):
            if os.path.isdir(files) and (files not in exception):
                iterator_dirs += 1
                file_list.append(files)
                if verbose:
                    print(
                        "File found at {0} : {1}".format(
                            path_to_folder, files))

        if verbose:
            print("Number of{0} directories found in {1} : {2}".format(
                extension,
                path_to_folder,
                iterator_dirs))

    if type_ is None and verbose:
        print("In total {0} elements found in {1}".format(
            iterator_dirs+iterator_files,
            path_to_folder))

    if sort == "natural":
        file_list = _natural_sort(file_list)
    elif sort == "alphanumeric":
        file_list.sort()
    return file_list


@gd.accepts(list)
def _natural_sort(list_):
    """Sorts a list by natural order.

    Args:
        list_ (:obj:`list`): Complete or relative path to the folder
        you want to explore.

    Returns:
        :obj:`list`:

    Raises:
        AssertError: Raised when the types of the arguments are not respected.

    Examples:
        To sort a simple list of strings :
        >>> list_ = [str(i) for i in range(20)]
        >>> expected_out =  ['0', '1', '2', '3', '4', '5', '6', '7', '8',
        ... '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19']
        >>> out = _natural_sort(list_)
        >>> out == expected_out
        True
        >>> out == sorted(list_)
        False

    """
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(list_, key=alphanum_key)


@gd.accepts(int, int, str, str, int, int)
def print_progress(
        iteration,
        total,
        prefix='',
        suffix='',
        decimals=1,
        bar_length=100):
    """A nice way to show that your code is still running.

    This function prints a progress bar corresponding to the ratio between
    the number of iterations and the expected total number of iterations.
    The percentage is also shown in a numeric form.
    It can also display some custom information in two fields (prefix and
    suffix).

    Args:
        iteration (:obj:`int`): the number of iterations already past

        total (:obj:`int`): the expected total number of iterations

        prefix (:obj:`str`, optional): field to display custom information (\
         default is ``''``).

        suffix (:obj:`str`, optional): field to display custom information (\
         default is ``''``).

        decimals (:obj:`int`, optional): number of decimals to show.

        bar_length (:obj:`int`, optional)

    Returns:
        None

    Raises:
        None

    Todo:
        * Disable the "fancy bar" by default (use simple \# or = instead)
    """
    format_str = "{0:." + str(decimals) + "f}"
    percents = format_str.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    if iteration / float(total) < 0.333:
        filler = "░"
    elif iteration / float(total) < 0.666:
        filler = "▒"
    elif iteration / float(total) < 1:
        filler = "▓"
    else:
        filler = "█"
    bar = filler * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(
        '\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


@gd.accepts(str)
def get_nb_lines_file(infile):
    """Opens a potentially zipped file and return its number of lines.

    This function opens the file received as argument and opens it depending
    on its extension (For the moment, only classic text files and gzipped
    files can be opened.)

    Args:
        infile (:obj:`str`): Complete or relative path to the file you want\
         to open.

    Returns:
        :obj:`int`: The number of lines in the file.

    Raises:
        AssertError: Raised when the types of the arguments are not respected.
    """
    opener_dict = {".gz": gzip.open}
    opener = open
    for extension, opener_type in opener_dict.items():
        if infile.endswith(extension):
            opener = opener_type
            break
    with opener(infile) as f:
        lines = 0
        for _ in f:
            lines += 1
    return lines


@gd.accepts((float, int), (float, int), bool)
def time_points_to_time_length_in_h_min_sec(begin_time, end_time, to_int=True):
    """Takes to time points in second and returns the difference in h, min, s.

    Args:
        begin_time (:obj:`float|int`): First time point in seconds (*e.g.*\
         given by :code:`time.time()`)
        end_time (:obj:`float|int`): Second time point in seconds (*e.g.*\
         given by :code:`time.time()`)
        to_int (:obj:`bool`): Forces the output to be a tuple of integers

    Returns:
        :obj:`tuple`: Tuple containing the result in the form (h, min,\
         s) where h, min and s are integers or floats depending on
         :code:`to_int`

    Raises:
        AssertError: Raised when the types of the arguments are not respected.
    """
    m, s = divmod(end_time - begin_time, 60)
    h, m = divmod(m, 60)
    if to_int:
        h = int(math.floor(h))
        m = int(math.floor(m))
        s = int(math.floor(s))
    return h, m, s


@gd.accepts(bool)
def time_since_first_call(raw=False):
    """A basic timer which returns the time spent since the first call.

    Generator of time durations. The first call initialise the generator with
    the current time and yields 0. All further calls yield the time spent
    since the first call.

    Args:
        raw (:obj:`bool`, optional): Indicate if the time yielded is\
         formatted (:code:`raw=False`, by default) or not.

    Yields:
        :obj:`tuple|float`: Depending on :code:`raw` yields a tuple of\
         integers *(h, min, s)* or a float.

    Raises:
        AssertError: Raised when the types of the arguments are not respected.

    Examples:

        >>> import time
        >>> timer = time_since_first_call()
        >>> for _ in range(10):
        ...     t = timer.__next__()
        ...     time.sleep(0.1)
        >>> result = timer.__next__()
        >>> result == (0, 0, 1)
        True
    """
    begin_time = time.time()
    yield 0.0
    while True:
        current_time = time.time()
        if raw:
            yield current_time - begin_time
        else:
            yield time_points_to_time_length_in_h_min_sec(
                begin_time,
                current_time)


@gd.accepts(bool)
def time_between_two_calls(raw=False):
    """A basic timer that returns the time spent since the last call.

    Generator of time durations. The first call initialises the generator with
    the current time and yields 0. All further calls yield the time spent
    since the precedent call.

    Args:
        raw (:obj:`bool`, optional): Indicate if the time yielded is\
         formatted (:code:`raw=False`, by default) or not.

    Yields:
        :obj:`tuple|float`: Depending on :code:`raw` yields a tuple of\
         integers *(h, min, s)* or a float.

    Raises:
        AssertError: Raised when the types of the arguments are not respected.

    Examples:

        >>> import time
        >>> timer = time_between_two_calls()
        >>> for _ in range(10):
        ...     t = timer.__next__()
        ...     time.sleep(0.1)
        >>> result = timer.__next__()
        >>> result == (0, 0, 0)
        True
    """
    current_time = time.time()
    yield 0.0
    while True:
        previous_time, current_time = current_time, time.time()
        if raw:
            yield current_time - previous_time
        else:
            yield time_points_to_time_length_in_h_min_sec(
                previous_time,
                current_time)


@gd.accepts(list, (list, tuple), type, bool)
def random_chunks(l, subset_proportions, output_format=tuple, force=False):
    """Shuffles the list and returns chunks.

    This generator takes a list and the proportions in which you want to
    subdivide it and yields random subsets of this list.

        .. warning::
           The sizes of the chunks is equal to the floored multiplication of
           the size of the original list by the given proportions. Thus,
           a rounding error might often happen and the size of the all the
           chunks would not match the size of the original list. To correct
           that, the remaining elements of the list are added to the last
           chunk (corresponding to :code:`subset_proportions[-1]`). We let it
           that way as it didn't affect our work a lot but this behaviours
           will probably change in further versions.


    Args:
        l (:obj:`list`): original list
        subset_proportions (:obj:`list|tuple`): sizes of the chunks given as\
         proportions of the original list.
        output_format (:obj:`type`, optional): type of output format. By\
         default, chunks are returned in tuples (:code:`output_format=tuple`)\
         but can also be list.
        force (:obj:`bool`, optional): Ignores the *ValueError* raised when the\
         sum of the proportions is not equal to 1.

    Yields:
        :obj:`tuple|list`:

    Raises:
        AssertError: Raised when the types of the arguments are not respected.
        ValueError: Raised when the sum of the proportions (rounded at\
         :math:`10^{-9}`)\ is different than 1.

    Examples:

        >>> list_ = list(range(100))
        >>> a, b, c = random_chunks(list_, (0.2, 0.5, 0.3))
        >>> len(a) == 20
        True
        >>> len(b) == 50
        True
        >>> len(c) == 30
        True
        >>> type(a)
        <class 'tuple'>
        >>> for value in a+b+c:
        ...     try:
        ...         list_.remove(value)
        ...     except ValueError:
        ...         print("Value not in list !")
        >>> list_
        []
    """
    sum_proportions = sum(subset_proportions)
    if round(sum_proportions, 9) != 1 and not force:
        raise ValueError(
            "Sum of proportions != 1.\n{0} != {1}".format(sum_proportions, 1))
    subsets_sizes = [
        int(math.floor(len(l))*i) for i in subset_proportions]
    # Add one element to the last chunk if flooring the number introduced
    # a rounding error
    if sum(subsets_sizes) <= len(l) - 1:
        subsets_sizes[-1] += len(l) - sum(subsets_sizes)
    elif sum(subsets_sizes) != len(l) and not force:
        raise ValueError(
            "Chunks sizes do not match with list size.\n" +
            "{0} != {1}".format(sum(subsets_sizes), len(l)))
    random.shuffle(l)
    it = iter(l)
    for size in subsets_sizes:
        yield output_format(chain((next(it),), islice(it, size - 1)))

if __name__ == "__main__":
    doctest.testmod()
    print(__doc__)


def custom_output(text, print_parameters):

    if print_parameters["verbose"] and\
            print_parameters["printing"]and\
            print_parameters["in_loop"]:
        print(text, end="\r")
    elif print_parameters["verbose"] and print_parameters["printing"]:
        print(text)