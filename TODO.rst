TODO
####

General
*******


* recode the bash scripts in python 
* assemble the scripts to have some small scripts who use the library and will serve as examples of how to use it
* write tests (everywhere !)
* decompose into smaller units
* write documentation (docstring (**google style standard**) + sphinx + README + requirements + TODO (Yes, it's here))
* replace the way the paths are written: use os.path.join, os.path.sep  instead of wrting everything manually (Already started but not corrected everywhere yet)
* add proper logging with the logging library instead of printing everythings
* specify

    .. code-block:: python 

                #!/usr/bin/env python
                #-*- coding: utf-8 -*-

  at the top of every files instead of what was specified before (more portable)
  
* Don't be lazy on exceptions raising (*Errors should never pass silently* !)
* Use a library to get the time spent in different functions, the number time they are called etc.
* Modify the settings duplication from template so that it does not copy the warning on the do not modify + make sure it is always present (so duplicated from template if not there) evenif you import some specic subpackages from the library (for the moment, copying from the template is done by the :code:`__init__.py` from pydeepgenomics which might not be called if a subpackage is imported directly)
* Change the :code:`settings_template` file to read only ?
* Move the requirement.txt building in a setup.py (And write the whole setup.py)
* Avoid trying to correct the name of the files to make them easier to read (*e.g.* transforming :code:`name_name.txt` into :code:`name.txt`) --> Some places of the code still try to do that and it can add unwanted side effects (it used to be clean on my specific work but it is not portable). Plus it is the responsability of the user to give clean files.
* Hide the complexity of some processes behind generators (Example: when we process files, it might be cleaner to work with generators)
* Find a way to keep consistent file naming and tree structure conventions all over the project
* If we want to be more flexible on the file naming and tree structure, it might be interesting to give a file where the user can specify custom name patterns etc
* Clean old code commented and still present
* Make the whole thing quiet !

Documentation
*************

* Almost every modules still need to be documented ...
* Try to host the whole documentation as a static website on github
* Include the documentation generation script inside the repo

Library
*******

Tools
-----
Generaltools
~~~~~~~~~~~~

* Recode the function list_elements: 
    * It should be cleaner
    * It should be able to handle a tuble of extensions
* Add Exceptions (Incorrect path to list_elements, not a list of strings to _natural_sort ...)
* Add options to the timers (:code:`time_since_first_call` and :code:`time_since_last_call`) so that they can give the raw time and not systematically the formated time
* :code:`_custom_output` should take care of the other possible options when logging is ready
* Add some filters :code:`get_nb_lines_file`

Generaldecorators
~~~~~~~~~~~~~~~~~

* RAS for the moment

Preprocessing
-------------

Encoding
~~~~~~~~
* When iter in batch of elements use generator with this kind of solutions:

        .. code-block:: python

                from itertools import chain, islice
                 
                def morceaux(iterable, taille, format=tuple):
                    it = iter(iterable)
                    while True:
                        yield format(chain((next(it),), islice(it, taille - 1)))

  (For python 2. Find how to convert that to python 3)
* Give the task of logging/printing information to a _function to lighten the code from unnecessary information (also calculation of the time points ...)
* By the way, a generator might also become useful to give the time spent
* Change the way the decoding of each position is done .......... It's really too slow (For the moment, 50000 decodings require > 2 minutes on my computer...).
* Clean the function :code:`verify_decoding` to have smaller functionnal units and a code easier to read.

vcf
~~~

* rewrite split.js in python and/or at least in a more portable version.
* add tests
* Change the name of this module
* Break into smaller functionnal units
* Create a more general "get_nb_lines" in generaltool able to handle the case used in the function "lines" ?

Subsets:
~~~~~~~~
* Use the os, sys and shutil libraries instead of the os calls
* Use a generator when doing some action on a list files in a loop and removing the last element processed after each round of the loop

Examples:
~~~~~~~~~

* Check size of the vcf files folder before making a copy
* Clean playground when script is over ?
* verify which version of node is needed
* Add the second part of example 4

Tests
*****

General
-------
* Note: the tests were added a few months after the beginning of the project, thus their sparsity and the diffculty to test some functions
* In general, add new cases to be tested for the different test sets to be sure that the extrem cases are taken into account.
* I used unittest to familiarize myself with unit testing but it would be better to have everything in py.test or nose later.

Tools
-----

General tools
~~~~~~~~~~~~~

* Use :code:`_write_multiple_files` and playground to do the tests instead of testing on a directory of the module
* Document the tests ?
* Add tests to be sure the functions which manage files handle both relative and absolute paths

General decorators
~~~~~~~~~~~~~~~~~~

* Prepare tests for the
* Document the tests

VCF
---

vcf
~~~
* Do everything !
* (But first the vcf module may be broken into smaller units so that unit testing has a sens ...)
* Document the tests

import time
def time_since_first_call():
    previous_time = None
    current_time = time.time()
    yield 0

    while True:

        previous_time, current_time = current_time, time.time()
        yield current_time - previous_time