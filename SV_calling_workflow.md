# Structural Variant Calling Workflow Overview

This document outlines the steps performed by the snakemake workflow
`svcalling.sm`. The input files are read alignment .bam files found in the 
directory `processed-data/alignment/`. They can be produced separately, or as part of 
the Variant Calling snakemake workflow. This workflow uses 
[smoove](https://github.com/brentp/smoove) and [Manta](https://github.com/Illumina/manta) as the main SV calling tools.

## Smoove Structural Variant Calling

### 0. Create .bai/.fai files if not present

**Rule: make_fai, make_bai**

If the index files for the reference genome fasta file or the {sample}.bam 
read alignment files do not exist, use samtools to generate them.

### 1. Call genotypes with Smoove

**Rule: smoove_call**

Call genotypes in each sample. 

### 2. Merge genotype calls

**Rule: smoove_merge**

Get the union of all sites across all samples as a single VCF file.

### 3. Genotyping

**Rule: smoove_genotype**

Genotype each sample at all sites in the merged file, and use the program 
[duphold](https://github.com/brentp/duphold) to add depth annotations.

### 4. Create a joint-called file

**Rule: smoove_paste**

Paste all single-sample VCFs with the same number of variants to get a single, 
squared, joint-called file.

### 5. Annotate

**Rule: smoove_annotate**

Annotate the variants with exons and UTRs that overlap from a GFF, and annotate 
high-quality heterozygotes. This is done using the file listed for 
`annotation_gff` in `config/svcalling.config.yaml`.

### 6. Filter variants

**Rule: smoove_filter**

Use SnpSift to filter the variants using the following criteria:
 - MSHQ > 3 for all SV types
 - DHFFC < 0.7 for deletions
 - DHFFC > 1.25 for duplications

Briefly, the `smoove annotate` function adds an SHQ (Smoove Het Quality) tag to 
every sample format. These values range from 1 to 4, where 1 is low quality and 
4 is high quality. A value of -1 is non-het. The MSHQ, or mean SHQ is a score 
added to the INFO field; the average SHQ for all heterozygous samples for that 
variant. The filtering thresholds used here are suggested on the 
[Smoove](https://github.com/brentp/smoove) project GitHub.


### 7. Compress chromosome statistics file for Manta

**Rule bgzip_chromstats**

Compress a given bed file containing chromosome positions for all chromosomes to be analyzed. 

### 8. Run Manta per-chromosome

**Rule manta_separate**

Generate Manta PyFlow with the configManta.py script on a per-chromosome basis, and then 
run the pyflow program. Note that this rule instructs Manta to write to node storage, so 
all results files are copied back to local storage once Manta is complete. This also means 
that although Manta technically allows restarting the workflow, it is not supported here.

### 9. Combine Manta chromosomes

**Rule manta_combine**

Merge the per-chromosome VCFs using Picard MergeVcfs.

### 10. Index SV files
**Rule: index_svs**

Sort Smoove results file with Picard SortVcf. Compress files with bgzip, and use tabix to index 
the Smoove and Manta output files.

### 11. Get program version info
**Rule: pipeline_info**

Creates a file containing version information from each program in the workflow

### 12. Create md5 checksum files
**Rule: create_md5s**

Uses md5sum to create checksums for all output files, the snakefile, and 
the program versions file. 
