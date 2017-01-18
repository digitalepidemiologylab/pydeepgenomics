README
######

.. figure:: https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Plasmid_with_insert.svg/2000px-Plasmid_with_insert.svg.png
   :align: center
   :height: 120px
   :width: 120 px
   :scale: 50 %

   (`Image reference
   <https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Plasmid_with_insert.svg/2000px-Plasmid_with_insert.svg.png>`_.)

| **Note**:
| Documentation on: https://salathegroup.github.io/pydeepgenomics/
| Code on: https://github.com/salathegroup/pydeepgenomics

.. attention::
   | Not yet retrocompatible with python 2.*
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
contains only the part on preprocessing but other packages (including the
Deep Learning part) will be included when ready.

Usage
*****

Modules structure:
------------------

::

   pydeepgenomics
   ├── preprocess
   │   ├── cutting.py
   │   ├── encoding.py
   │   ├── examples
   │   │   ├── 1_split_vcf_files.py
   │   │   ├── 2_encode_genotypes.py
   │   │   ├── 3_form_subsets.py
   │   │   ├── 4_filter_and_split_files.py
   │   │   └── setup_ex_env.py
   │   ├── filtering.py
   │   ├── settings_template.py
   │   ├── subsets.py
   │   ├── vcf
   │   │   ├── split.js
   │   │   └── vcf.py
   │   └── verifications.py
   └── tools
       ├── generaldecorators.py
       └── generaltools.py


The library contains a few examples on how to use the tools present here.

Limitations
***********

| For the moment, only preprocessing is present
| Works exclusively with text (*.vcf*) files.


Requirements
************

.. include:: ./requirements.rst
   :literal:
