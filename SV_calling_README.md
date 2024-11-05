# Structural Variant Calling Workflow

This pipeline uses the read mapping files produced by the 
[Read Mapping and Variant Calling pipeline](README.md) to detect structural 
variants, and produces image files of each SV region. It is designed to work on 
Compute Canada clusters.

**SECTIONS**

[Setup](#setup)

[Program Requirements](#required-programs-to-run-the-workflow)

[Edit Config File](#edit-config-file)

[Running the Structural Variant Calling workflow](#running-the-SV-calling-workflow)

[Running Manta on DRAC clusters](#running-manta-on-drac-clusters)


## Setup

Requirements:
- Python 3.11+ (This workflow was developed and tested with Python v. 3.11)

## Required programs to run the workflow

These programs must be in your path or specified in the file `config/sv_calling.config.yaml`:

 - [smoove >= 0.2.8](https://github.com/brentp/smoove)
 - [SnpSift >= 5.2e](https://pcingola.github.io/SnpEff/) (The path to SnpSift.jar must be specified in the `config/sv_calling.config.yaml`
 configuration file)

All other programs called by the workflow are loaded as software modules.

 
## Edit Config File

The file `config/sv_calling.config.yaml` controls all configurable options 
relating to the workflow itself. For each rule within the snakemake file found in 
`workflow/svcalling.sm`, there are thread and resource specifications which can be 
edited according to your setup. 

All rules in the workflow are designed to run on a single node of a cluster 
with up to 64Gb RAM, with the exception of the local rules listed at the top of 
the `workflow/svcalling.sm` file. 

Cluster configuration values are listed for each rule and specify the 
following slurm options:
- threads: 1 # Number of threads to use for each job; should be equal to or less than cores
- resources:
	- cores = 1,  # Number of cpus available, or that will be requested from the scheduler
	- runtime = 120,  # Requested walltime in minutes
	- mem_mb = 4000,  # Requested memory in MB

#### Add user-specific files to the reference_files directory

The following files must be added to the `db/` directory.
File names should be specified in `config/svcalling.config.yaml`:

- reference genome in Fasta format
- fai index file
- GFF file containing gene feature information for smoove annotation

## Running the SV calling workflow

### Input files

The workflow expects read mapping (*.bam) files in the directory 
`processed-data/alignment/`. These are created in the process of variant calling using 
the main Variant Calling snakemake workflow. The SV calling workflow can be run 
on any alignment files without running the main workflow, as long as they are 
found in the `processed-data/alignment/` directory. 
 
### Output files

Output files will be generated within subdirectories of `processed-data`. 
For more information on the SV calling workflow, see the [SV Calling Workflow](SV_calling_workflow.md)

## Running the SV calling workflow

If you do not have a slurm profile, [set one up here](https://github.com/stothard-group/variant-calling-pipeline/blob/master/slurm_setup.md).

The workflow can now be run with the following command:

```
snakemake --snakefile svcalling.sm --profile slurm
```

### Singularity/Apptainer

The smoove-related rules require a smoove SIF file. Therefore, the workflow should be run with 
`--use-singularity` or `--use-apptainer` and the appropriate `--singularity-args`. The file 
`smoove.sif` must be generated prior to running the workflow, and must be found in the working 
directory. It can be created with the following command:

```bash
module load apptainer
apptainer build smoove.sif docker pull brentp/smoove:latest
```

## Running Manta on DRAC clusters

Manta opens and writes to hundreds of files, which can cause issues for the Cedar cluster. It is 
recommended that manta_separate be run on another cluster, such as Beluga. Additionally, 
limit the number of threads for the manta_separate rule (six is plenty), as this affects the number 
of times the same files is opened at once.
