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

Following the main QIIME2 tutorial (“Moving Pictures”). Multiplexed file with reads and file with barcodes for demultiplexing
- To import the regular FASTQ files, we need an additional “manifest file”:
   -  ```qiime tools import   --type 'SampleData[SequencesWithQuality]'   --input-path manifest.tsv   --output-path sequences.qza   --input-format SingleEndFastqManifestPhred33V2```

- Checking:
  - ```qiime tools validate sequences.qza ```
  -  We want to see - Result sequences.qza appears to be valid at level=max.
  -  We have single-end reads in FASTQ format with Phred33 encoding

#### 3. Demultiplexing and QC

- The distribution of sequence qualities:
  - ```qiime demux summarize --i-data sequences.qza --o-visualization sequences.qzv```

#### 4. Feature table construction
- The metadata table - we have a unique sequence in the beginning of each sample, and primer sequence, that was used to amplify the V5 region of the rRNA
- To strip it out, and filter chimeric sequences
  - ```qiime dada2 denoise-single   --i-demultiplexed-seqs sequences.qza   --p-trim-left 35 --p-trunc-len 140 --o-representative-sequences rep-seqs.qza --o-table table.qza --o-denoising-stats stats.qza```

- According to visualization choose the correct number nucleotide to trim out -  the primer + adapter length is about 35 bp, and amplicon size is about 145 bp-  m= 35, n = 140
- Check and compare with visualizationL:
  ``` qiime metadata tabulate   --m-input-file stats.qza   --o-visualization stats.qzv```
- Approximatly 200 bp were filtered

#### 5. FeatureTable and FeatureData summaries

- the main results of the DADA2 step is a clustering into an amplicon sequence variant (ASV) -  a higher-resolution analogue of the traditional OTUs
- feature table is a matrix of sample X feature abundances (the number of times each feature was observed in each sample)

- To  create visual summaries of the data - how many sequences are associated with each sample and with each feature
  ``` qiime feature-table summarize   --i-table table.qza   --o-visualization table.qzv   --m-sample-metadata-file sample-metadata.tsv```

- To map feature IDs to sequences, to use these representative sequences in other applications
  ```qiime feature-table tabulate-seqs  --i-data rep-seqs.qza   --o-visualization rep-seqs.qzv```

#### 6. Taxonomic analysis

- To compare the representative sequences with the taxonomy database
  -  download database from the data resources page-  is just a fasta file of the 16S representatives, and QIIME2 uses Naive Bayes classifiers trained on this data
  -  the link: ```https://disk.yandex.ru/d/QxQWKV8x5ucxvw```
  -  ```qiime feature-classifier classify-sklearn   --i-classifier silva-138-99-nb-classifier.qza   --i-reads rep-seqs.qza   --o-classification taxonomy.qza```
  -  visualization: ```qiime metadata tabulate --m-input-file taxonomy.qza --o-visualization taxonomy.qzv```

upd: тут проблема - переобучаем классификатор на новой версии

- To view the taxonomic composition of our samples with interactive bar plots
  ``` qiime taxa barplot \
  --i-table table.qza \
  --i-taxonomy taxonomy.qza \
  --m-metadata-file sample-metadata.tsv \
  --o-visualization taxa-bar-plots.qzv ```

There is an option to play with your data in the online version of MicrobiomeAnalyst. This requires exporting the data to an ASV table and taxonomy file, and making a few adjustments to the metadata file. To avoid the formatting hassle, it is better to use BIOM binary format
-  ```qiime tools export --input-path table.qza --output-path export_biom```
-  ```qiime tools export --input-path  taxonomy.qza --output-path export_biom```

Add taxonomy information to biom file:
- ```biom add-metadata -i export_biom/feature-table.biom -o export_biom/feature-table-with-taxonomy.biom --observation-metadata-fp export_biom/taxonomy.tsv --sc-separated taxonomy --observation-header OTUID,taxonomy,confidence```

Fix header of the metadata file:
- ```sed  's/SampleID/NAME/g' sample-metadata.tsv   > sample-metadata.txt```

To explore the data in detail in MicrobiomeAnalyst

### Part 2. Shotgun sequencing.

- To obtain the ancient sequence of the pathogens and compare them with modern one

#### 1. Shotgun sequence data profiling.

- kmer-based Kraken2.
- Kraken2 пытается отнести чтения к различным таксонам на основе эталонной базы данных геномов. Он работает, сравнивая k-меры в чтениях с k-мерами в эталонной базе данных, чтобы определить таксономическое происхождение чтений.

- too large, but command
```conda install kraken2 \
kraken2-build --standard --db $DBNAME \
kraken2 --db /path/to/kraken2_database --output output_file --report report_file input_fastq_file```

#### 2. Visualization of the Kraken results as a Sankey diagram

#### 3. Comparison with ancient Tannerella forsythia genome
- Download reference 
- Align contigs on the downloaded reference with bwa mem
  ```bwa index Tannerella_forsythia_genome.fasta```
  ```bwa mem Tannerella_forsythia_genome.fasta contigs.fasta > alignment.sam```
  ```samtools view -S -b alignment50.sam > alignment50.bam```
- Snalefile in repository


#### These three bacterial species are called “the red complex”

The red complex—among a number of other complexes—were classified by Sigmund Socransky in 1998.

The three members of the red complex are:

- Porphyromonas gingivalis
- Tannerella forsythia
- Treponema denticola

Немного про Qiime

#### Qiime (Quantitative Insights Into Microbial Ecology)
— это мощный инструмент для анализа микробных сообществ, основанный на данных секвенирования. Он используется в основном для обработки и анализа данных метагеномики, особенно в исследованиях микробиомов (например, кишечника, почвы, воды и других сред). Qiime позволяет исследователям изучать разнообразие микроорганизмов, их функции и взаимодействия в различных экосистемах.

##### Основные функции Qiime:

- Обработка данных секвенирования:
  - Qiime работает с данными, полученными из платформ секвенирования, таких как Illumina.
  - Он помогает фильтровать, очищать и группировать последовательности ДНК (например, операционные таксономические единицы, OTU) или ампликоны (ASV).

- Анализ альфа- и бета-разнообразия:
  - Альфа-разнообразие — это мера разнообразия внутри одной выборки (например, количество видов и их равномерность).
  - Бета-разнообразие — это сравнение разнообразия между разными выборками.

- Таксономическая классификация:
  - Qiime позволяет классифицировать микроорганизмы по таксономическим группам (например, род, семейство, вид) на основе референсных баз данных, таких как Greengenes или SILVA.
  
- Функциональный анализ:
  - С помощью Qiime можно предсказать функциональный потенциал микробного сообщества, используя базы данных, такие как PICRUSt.

- Визуализация данных:
  - Qiime предоставляет инструменты для создания графиков и визуализации результатов, таких как heatmaps, PCoA-графики (Principal Coordinates Analysis) и другие.

- Статистический анализ:
  - Qiime включает методы для статистического сравнения микробных сообществ между группами выборок.


