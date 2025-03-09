# Dead Man’s Teeth. Introduction to metagenomics analysis

- Scientists extracted DNA from the material underneath the dental calculus.
- In this project, we will explore these samples and study the history of oral diseases in humans.

### The results of sequencing portions of V5 16S ribosomal RNA obtained by an instrument Roche GS Junior

- Download the raw data:
```conda env create -n qiime2-amplicon-2024.10 --file https://data.qiime2.org/distro/amplicon/qiime2-amplicon-2024.10-py310-osx-conda.yml```

**All data from the original research are available  in the NCBI Short Read Archive (SRA) under number SRP029257 (BioProject PRAJNA 216965)** 

### 1) Part 1. Amplicon sequencing.

- We want to show that sets of similar fragments originate from the same organism
- Chosing - QIIME2

- QIIME 2 provides comprehensive end-to-end analysis of diverse microbiome data and comparative studies with publicly available data

#### 1. QIIME2 installation - the latest version

```conda install qiime2/label/r2024.5::qiime2```

#### 2. Importing data

- following the main QIIME2 tutorial (“Moving Pictures”)
- multiplexed file with reads and file with barcodes for demultiplexing
- To import the regular FASTQ files, we need an additional “manifest file”

- ```qiime feature-classifier classify-sklearn   --i-classifier silva-138-99-nb-classifier.qza   --i-reads rep-seqs.qza   --o-classification taxonomy.qza ```
- learning - import fasta format data 
