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

Introduction
************

The idea behind this project is to give a few tools to work with deep neural
networks on genomic data. This library regroups features which were
originally designed for two distinct projects currently in progress in the
digital epidemiology lab: the first one on `predictions of a
quantitative trait
<https://github.com/salathegroup/deep-height>`_
and the second one on genotype imputation. For the moment, this library
contains only the part on preprocessing but other packages might arrive
eventually.

What's in here ?
****************

Preprocessing
-------------

The preprocessing can be separated in two main parts:

#. The general transformation of the vcf text files (often used in
   bioinformatics applications) to a format simpler to use in our projects with
   decoupled meta information files and sample files.
#. A more application specific part consisting for example in grouping all
   the information on each sample of a GWAS to train a model on genome wide
   information.

We chose to do these steps with homemade custom solutions although some tools
certainly already exist.

#. Blabla

General transformations:
~~~~~~~~~~~~~~~~~~~~~~~~

BUILD 37 http://www.internationalgenome.org/category/ncbi36/
Explaination of the structure of a vcf file

::

   ##fileformat=VCFv4.1
   ##FILTER=<ID=PASS,Description="All filters passed">
   ##fileDate=20150218
   ##reference=ftp://ftp.1000genomes.ebi.ac.uk//vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz
   ##source=1000GenomesPhase3Pipeline
   ##contig=<ID=1,assembly=b37,length=249250621>
   ##contig=<ID=2,assembly=b37,length=243199373>
   ...
   ...
   ##INFO=<ID=VT,Number=.,Type=String,Description="indicates what type of variant the line represents">
   ##INFO=<ID=EX_TARGET,Number=0,Type=Flag,Description="indicates whether a variant is within the exon pull down target boundaries">
   ##INFO=<ID=MULTI_ALLELIC,Number=0,Type=Flag,Description="indicates whether a site is multi-allelic">
   #CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  HG00096 HG00097
   22      16050075        rs587697622     A       G       100     PASS    .    GT    0/0     0/0
   22      16050115        rs587755077     G       A       100     PASS    .    GT    0/0     0/0
   22      16050213        rs587654921     C       T       100     PASS    .    GT    0/0     0/0

Blabla

Application specific transformations:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Idea
Workflow

Limitations
***********


| For the moment, it only works with text (*.vcf*) files.


Requirements
************

.. include:: ./requirements.rst
   :literal:

------------

