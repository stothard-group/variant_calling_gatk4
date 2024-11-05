# Read Mapping and Variant Calling Pipeline for GATK4

#### Updated Variant Calling Pipeline

The original version of this workflow was developed for the 1000 Bulls Genome Project. 
See the [variant-calling-pipeline](https://github.com/stothard-group/variant-calling-pipeline) 
for more details.

For the related SV calling workflow, see [the SV calling README document](SV_calling_README.md)

**SECTIONS**

[Installation](#installation)

[Setup](#setup)

[Program Requirements](#required-programs-to-run-the-workflow)

[Edit Config Files](#edit-configuration)

[Running the Variant Calling workflow](#running-the-variant-calling-workflow)


## Installation

Download the repository and un-tar the software directory:

```
git clone https://github.com/stothard-group/variant_calling_gatk4.git

```

## Setup

Requirements:
- Python 3.11+ (This workflow was developed and tested with Python v. 3.11)
- setuptools
- cython
- gcc 12.3.1

Install the following python modules using pip:
- pandas>=1.5.0
- numpy>=1.21.2

Or run the setup.py script to install the required modules:

`python setup.py install`


## Required programs to run the workflow

The workflow is designed to run on a DRAC HPC cluster such as Cedar or Beluga. 
The programs listed in the Snakemake rules as "module load [program]" can be 
installed as Conda packages. 

The following R libraries are required:

- caTools
- ggplot2
- gplots
- gsalib
- reshape

These can be installed in the R shell with 

`install.packages(c('caTools','ggplot2','gplots','gsalib','reshape'))`


## Edit Configuration

The file `config/variant_calling.config.yaml` controls all configurable options 
relating to the workflow itself. For each rule within the snakemake file found in 
`workflow/snakemake`, there are thread and resource specifications which can be 
edited according to your setup. 

All rules in the workflow are designed to run on a single node of a cluster 
with up to 30 CPUs 
and 100Gb RAM, with the exception of the local rules listed at the top of the 
`workflow/snakemake` file. 

Cluster configuration values are listed for each rule and specify the 
following slurm options:
- threads: 1 # Number of threads to use for each job; should be equal to or less than cores
- resources:
	- cores = 1,  # Number of cpus available, or that will be requested from the scheduler
	- runtime = 120,  # Requested walltime in minutes
	- mem_mb = 4000,  # Requested memory in MB

#### Add user-specific files to the database directory

The following files must be added to the `db/` directory.
File names should be specified in `variant_calling.config.yaml`:

- reference genome in Fasta format
- fai index file
- file containing a list of all contig names in the reference 
genome, one item per line
- vcf file containing known variants for base quality score recalibration
- gff file containing gene feature information for SV annotation
- read group labels file in the format 

```
ID	PU	SM	LB	PL
```
For more information on read groups, see [Read groups](https://gatk.broadinstitute.org/hc/en-us/articles/360035890671-Read-groups).

## Running the Variant Calling workflow

For more information about the workflow, see the [Variant_calling_workflow.md](Variant_calling_workflow.md)

### Input files

The workflow expects paired-end fastq files as inputs, within a directory 
in `variant_calling`. The relative path to this directory should be specified 
in the `variant_calling.config.yaml` file.


#### Note on sequence filenames

This workflow was designed for sequence files named as follows:

`{sample}_R[1,2].fastq.gz`

For other filename patterns, the snakefile's regular expression matching the 
forward mate FASTQ files must be modified.

### Output files

Output files will be generated within subdirectories of `processed-data`. The final 
VCF files will be generated in `results/snps_indels/`.

#### Command line options

Resource allocations are given within each rule, and it is strongly 
recommended that users create or use a snakemake profile to run the workflow.

For example, if you have a [slurm profile](https://github.com/Snakemake-Profiles/slurm), 
you can run snakemake with the following command:
```
snakemake --profile slurm
```

[This guide](https://github.com/stothard-group/variant-calling-pipeline/blob/master/slurm_setup.md) 
can be used to set up a slurm profile. Other profiles can be found [here](https://github.com/snakemake-profiles/doc)
