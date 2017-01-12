What's in here ?
################

Preprocessing
*************

The preprocessing can be separated in two main parts:

#. The general transformation of the vcf text files (often used in
   bioinformatics applications) to a format simpler to use in our projects with
   decoupled meta information files and sample files.
#. A more application specific part consisting for example in grouping all
   the information on each sample of a GWAS to train a model on genome wide
   information.

We chose to do these steps with homemade custom solutions although some tools
certainly already exist for a few reasons:

#. We had no good knowledge of these tools nor someone with a real expertise
   within easy reach. We had a try with GATK, bcf tools or PLINK and we still
   use them for some purpose but they are quite heavy to manipulate when your
   not used to it. Moreover, some features to keep the files shaped according
   to the standards classic standard were not necessary for our exploratory
   analysis and slow down the whole process.
#. We had little prior knowledge of the conventions in genomic data formating
   nor how it was structured. Thus, making the preprocessing ourselves could
   help us familiarize ourselves with this kind of dataset.

General transformations:
------------------------

Background
~~~~~~~~~~
The datasets we received
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
   #CHROM  POS             ID              REF     ALT     QUAL    FILTER  INFO FORMAT  HG00096 HG00097
   22      16050075        rs587697622     A       G       100     PASS    .    GT      0/0     0/0
   22      16050115        rs587755077     G       A       100     PASS    .    GT      0/0     0/0
   22      16050213        rs587654921     C       T       100     PASS    .    GT      0/0     0/0


What do we actually do
~~~~~~~~~~~~~~~~~~~~~~


Application specific transformations:
-------------------------------------

Idea
Workflow

------------
