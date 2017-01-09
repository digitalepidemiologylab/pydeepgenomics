#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A bunch of tests for the functions defined in generaltools.py.
Note : they should be run from the root folder of the library with the command
python -m unittest discover
"""
import gzip
import os
import random
import shutil
import string
import sys
import unittest

try:
    from pydeepgenomics.tools import generaltools as gt
    from pydeepgenomics.tools import generaldecorators as gd
except ImportError:
    cmd_dir = os.path.abspath(os.path.dirname(__file__)).split("alltests")[0]
    if cmd_dir not in sys.path:
        sys.path.append(cmd_dir)
    from pydeepgenomics.tools import generaltools as gt
    from pydeepgenomics.tools import generaldecorators as gd


@gd.accepts(str, str, (None, str), int)
def _write_random_file(file_name, compression=None, nb_lines=100, empty=False):
    possible_compression = [None, "gzip"]
    try:
        assert compression in possible_compression
        if compression is None:
            custom_open = open
            write_mode = "w"
        else:
            custom_open = gzip.open
            write_mode = "wb"
    except AssertionError:
        raise ValueError(
            "Argument \"compression\" not recognized.\n"
            "It should be in {}".format(possible_compression))

    with custom_open(file_name, write_mode) as f_out:
        text = ""
        for i in range(nb_lines):
            if not empty:
                line = ''.join(
                    random.choice(string.ascii_letters) for _ in range(80))
            else:
                line = ""
            text += line + "\n"
        if compression is not None:
            text = text.encode()
        f_out.write(text)


@gd.accepts(str, int, (None, list), int)
def _write_multiple_files(path, nb_of_files, extensions=None, lines_per_file=0):

    if extensions is None:
        extensions = [".txt", ".log", ".vcf", ".py"]
    files = {key: [] for key in ["total"]+extensions}
    for _ in range(nb_of_files):
        file_name = ''.join(
            random.choice(string.ascii_letters) for _ in range(10))
        extension = random.choice(extensions)
        file_name += extension
        file_name_with_path = os.path.join(path, file_name)
        files["total"].append(file_name_with_path)
        files[extension].append(file_name_with_path)
        _write_random_file(file_name_with_path, nb_lines=lines_per_file)
    return files


class TestNaturalSort(unittest.TestCase):

    def test_on_a_sentence(self):
        list_ = ["How", "do", "you", "know", "she", "is", "a", "witch", "?"]
        expected = ["?", "a", "do", "How", "is", "know", "she", "witch", "you"]
        self.assertEqual(gt._natural_sort(list_), expected)

    def test_on_numbers(self):
        expected = [str(i) for i in range(1000)]
        list_ = expected[:]
        random.shuffle(list_)
        self.assertEqual(gt._natural_sort(list_), expected)

    def test_not_alphabetical(self):
        list_ = [str(i) for i in range(1000)]
        random.shuffle(list_)
        not_expected = list_[:]
        not_expected.sort()
        self.assertNotEqual(gt._natural_sort(list_), not_expected)


class TestListElements(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path_to_test = os.path.dirname(__file__)
        cls.path_to_playground = os.path.join(path_to_test, "playground")
        if not os.path. isdir(cls.path_to_playground):
            os.mkdir(cls.path_to_playground)
        else:
            shutil.rmtree(cls.path_to_playground)
            os.mkdir(cls.path_to_playground)

        cls.nb_files = random.randrange(10, 60)
        cls.nb_dirs = random.randrange(5, 20)

        cls.files = _write_multiple_files(cls.path_to_playground, cls.nb_files)
        cls.dirs = []
        for _ in range(cls.nb_dirs):
            dir_name = ''.join(
                random.choice(string.ascii_letters) for _ in range(10))
            dir_name_with_path = os.path.join(cls.path_to_playground, dir_name)
            cls.dirs.append(dir_name_with_path)
            os.mkdir(dir_name_with_path)

        cls.total_elements = cls.files["total"] + cls.dirs

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.path_to_playground)

    def test_simple_ls(self):
        # deep copy of the class variable
        files_in_current_folder = self.total_elements[:]
        files_in_current_folder.sort()
        results = gt.list_elements(
            self.path_to_playground, sort="alphanumeric")
        self.assertEqual(results, files_in_current_folder)

    def test_sorted_ls(self):
        files_in_current_folder = self.total_elements[:]
        files_in_current_folder = gt._natural_sort(files_in_current_folder)
        results = gt.list_elements(self.path_to_playground, sort="natural")
        self.assertEqual(
            results,
            files_in_current_folder)

    def test_ls_with_exception(self):
        files_in_current_folder = self.total_elements[:]
        files_in_current_folder = gt._natural_sort(files_in_current_folder)
        exception = random.sample(
            files_in_current_folder,
            len(files_in_current_folder)//5)
        files_in_current_folder = [
            x for x in files_in_current_folder if x not in exception]
        results = gt.list_elements(
            self.path_to_playground,
            sort="natural",
            exception=exception)
        self.assertEqual(results, files_in_current_folder)

    def test_ls_with_extensions(self):
        files_in_current_folder = self.files[".py"]
        files_in_current_folder = gt._natural_sort(files_in_current_folder)

        results = gt.list_elements(
            self.path_to_playground,
            sort="natural",
            extension=".py")
        self.assertEqual(
            results,
            files_in_current_folder)

    def test_ls_with_type_dir(self):
        dirs_in_current_folder = self.dirs
        dirs_in_current_folder = gt._natural_sort(dirs_in_current_folder)
        results = gt.list_elements(self.path_to_playground, type_="dir")
        self.assertEqual(
            results,
            dirs_in_current_folder)

    def test_ls_with_type_file(self):
        files_in_current_folder = self.files["total"][:]
        files_in_current_folder = gt._natural_sort(files_in_current_folder)
        results = gt.list_elements(
            self.path_to_playground,
            type_="file",
            sort="natural")
        self.assertEqual(
            results,
            files_in_current_folder)


class TestGetNbLinesFile(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path_to_test = os.path.dirname(__file__)
        cls.path_to_playground = os.path.join(path_to_test, "playground")
        if not os.path. isdir(cls.path_to_playground):
            os.mkdir(cls.path_to_playground)
        else:
            shutil.rmtree(cls.path_to_playground)
            os.mkdir(cls.path_to_playground)
        cls.nb_lines_not_empty_1 = random.randrange(1, 100)
        cls.nb_lines_not_empty_2 = random.randrange(1, 100)
        cls.nb_lines_empty_1 = random.randrange(1, 100)
        cls.nb_lines_empty_2 = random.randrange(1, 100)
        _write_random_file(
            os.path.join(cls.path_to_playground, "empty_1.txt"),
            nb_lines=cls.nb_lines_empty_1,
            empty=True)
        _write_random_file(
            os.path.join(cls.path_to_playground, "empty_2.txt"),
            nb_lines=cls.nb_lines_empty_2,
            empty=True)
        _write_random_file(
            os.path.join(cls.path_to_playground, "empty_encoded_1.txt.gz"),
            nb_lines=cls.nb_lines_empty_1,
            compression="gzip",
            empty=True)
        _write_random_file(
            os.path.join(cls.path_to_playground, "empty_encoded_2.txt.gz"),
            nb_lines=cls.nb_lines_empty_2,
            compression="gzip",
            empty=True)
        _write_random_file(
            os.path.join(cls.path_to_playground, "not_empty_1.txt"),
            nb_lines=cls.nb_lines_not_empty_1)
        _write_random_file(
            os.path.join(cls.path_to_playground, "not_empty_2.txt"),
            nb_lines=cls.nb_lines_not_empty_2)
        _write_random_file(
            os.path.join(cls.path_to_playground, "not_empty_encoded_1.txt.gz"),
            nb_lines=cls.nb_lines_not_empty_1,
            compression="gzip")
        _write_random_file(
            os.path.join(cls.path_to_playground, "not_empty_encoded_2.txt.gz"),
            nb_lines=cls.nb_lines_not_empty_2,
            compression="gzip")
        _write_random_file(
            os.path.join(cls.path_to_playground, "really_empty.txt"),
            nb_lines=0,
            empty=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.path_to_playground)

    def test_incorrect_name(self):
        with self.assertRaises(FileNotFoundError):
            _ = gt.get_nb_lines_file(os.path.join(
                self.path_to_playground,
                "this_file_does_not_exist.txt"))

    def test_empty_file(self):
        found_nb_of_lines = gt.get_nb_lines_file(
            os.path.join(self.path_to_playground, "really_empty.txt"))
        self.assertEqual(0, found_nb_of_lines)

    def test_file_with_only_line_breaks_not_compressed(self):

        found_nb_of_lines_1 = gt.get_nb_lines_file(
            os.path.join(self.path_to_playground, "empty_1.txt"))
        found_nb_of_lines_2 = gt.get_nb_lines_file(
            os.path.join(self.path_to_playground, "empty_2.txt"))
        self.assertEqual(self.nb_lines_empty_1, found_nb_of_lines_1)
        self.assertEqual(self.nb_lines_empty_2, found_nb_of_lines_2)

    def test_file_with_only_line_breaks_compressed(self):
        found_nb_of_lines_1 = gt.get_nb_lines_file(
            os.path.join(self.path_to_playground, "empty_encoded_1.txt.gz"))
        found_nb_of_lines_2 = gt.get_nb_lines_file(
            os.path.join(self.path_to_playground, "empty_encoded_2.txt.gz"))
        self.assertEqual(self.nb_lines_empty_1, found_nb_of_lines_1)
        self.assertEqual(self.nb_lines_empty_2, found_nb_of_lines_2)

    def test_file_with_text_not_compressed(self):

        found_nb_of_lines_1 = gt.get_nb_lines_file(
            os.path.join(self.path_to_playground, "not_empty_1.txt"))
        found_nb_of_lines_2 = gt.get_nb_lines_file(
            os.path.join(self.path_to_playground, "not_empty_2.txt"))
        self.assertEqual(self.nb_lines_not_empty_1, found_nb_of_lines_1)
        self.assertEqual(self.nb_lines_not_empty_2, found_nb_of_lines_2)

    def test_file_with_text_compressed(self):
        found_nb_of_lines_1 = gt.get_nb_lines_file(
            os.path.join(self.path_to_playground, "not_empty_encoded_1.txt.gz"))
        found_nb_of_lines_2 = gt.get_nb_lines_file(
            os.path.join(self.path_to_playground, "not_empty_encoded_2.txt.gz"))
        self.assertEqual(self.nb_lines_not_empty_1, found_nb_of_lines_1)
        self.assertEqual(self.nb_lines_not_empty_2, found_nb_of_lines_2)

if __name__ == "__main__":
    unittest.main()
