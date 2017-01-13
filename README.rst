README
######

.. figure:: https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Plasmid_with_insert.svg/2000px-Plasmid_with_insert.svg.png
   :align: center
   :height: 200px
   :width: 200 px
   :scale: 50 %

   Still under constructions ....
   (*ref.* `image of this beautiful plasmid
   <https://upload.wikimedia
   .org/wikipedia/commons/thumb/3/34/Plasmid_with_insert.svg/2000px-Plasmid_with_insert.svg.png>`_.)

| **General notes:**
| Documentation on: https://odissea.github.io/pydeepgenomics
| Code on: https://github.com/Odissea/pydeepgenomics

.. attention::
   | Not retrocompatible with python 2.*
   | Requires Node.js v6.9.4

Brief comment
*************

The idea behind this project is to give a few tools to work with deep neural
networks on genomic data. This library regroups features which were
originally designed for two distinct projects currently in progress in the
digital epidemiology lab: the first one on `predictions of a
quantitative trait
<https://github.com/salathegroup/deep-height>`_
and the second one on genotype imputation. For the moment, this library
contains only the part on preprocessing but other packages might arrive
eventually.

Usage
*****

Modules structure:
------------------

::

   pydeepgenomics
   ├── __init__.py
   ├── preprocess
   │   ├── cutting.py
   │   ├── encoding.py
   │   ├── examples
   │   │   ├── 1_split_vcf_files.py
   │   │   ├── 2_encode_genotypes.py
   │   │   ├── 3_form_subsets.py
   │   │   ├── 4_filter_and_split_files.py
   │   │   ├── __init__.py
   │   │   └── setup_ex_env.py
   │   ├── filtering.py
   │   ├── __init__.py
   │   ├── settings.py
   │   ├── settings_template.py
   │   ├── subsets.py
   │   ├── vcf
   │   │   ├── __init__.py
   │   │   ├── split.js
   │   │   └── vcf.py
   │   └── verifications.py
   └── tools
       ├── generaldecorators.py
       ├── generaltools.py
       └── __init__.py

Limitations
***********


| For the moment, it only works with text (*.vcf*) files.


Requirements
************

.. include:: ./requirements.rst
   :literal:
