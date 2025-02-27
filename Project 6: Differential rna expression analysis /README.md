
# Differential RNA expression analysis

## New bioinformatics skills covered: splice-junction aware alignment, guided transcript assembly, differential expression analysis

- В данном проекте мы будем анализировать изменение экспрессии генов в клетках дрожжей во время процесса ферментации
- В репозитории имется Snakemake file с реализованными командами

1) Input Data

   - There are two replicates of RNA-seq data from yeast before and during fermentation

SRR941816ftp.sra.ebi.ac.uk/vol1/fastq/SRR941/SRR941816/SRR941816.falsstq.gz (413 Mb)
SRR941817: fermentation 0 minutes replicate 2 
ftp.sra.ebi.ac.uk/vol1/fastq/SRR941/SRR941817/SRR941817.fastq.gz (455 Mb)
SRR941818: fermentation 30 minutes replicate 1 ftp.sra.ebi.ac.uk/vol1/fastq/SRR941/SRR941818/SRR941818.fastq.gz (79.3 Mb)
SRR941819: fermentation 30 minutes replicate 2 ftp.sra.ebi.ac.uk/vol1/fastq/SRR941/SRR941819/SRR941819.fastq.gz (282 Mb)

As a reference genome we will use *Saccharomyces cerevisiae*

reference genome file: 
ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/146/045/GCF_000146045.2_R64/GCF_000146045.2_R64_genomic.fna.gz

annotation file:
ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/146/045/GCF_000146045.2_R64/GCF_000146045.2_R64_genomic.gff.gz

Глянем на сырые прочтения - multifastqc

Использованный код : 
 - ```multiqc fastqc_reports -o multiqc_output```

В целом по качеству данные нормальные, но адаптеры надо отрезать - 12 п.о.
- ```trimmomatic SE -phred33 SRR941816.fastq SRR941816.results HEADCROP:12```

2) Analysis Pipeline

Можно глянуть на - kallisto + sleuth - с помощью псевдовыравнивания и построения графов де Брюйна

- Используем стандартный вариант сначала HISAT2 + deseq2,
- Используем пакет deseq2 в R для статистической обработки полученных результатов

a)  Aligning with HISAT2
build genome index:
run hisat2-build
hisat2-build <reference.fasta> <genome index>


б) Выравнивание (картирование) на геном дрожжей  - с HISAT2

- hisat2 -p 8 -x reference_index -U SRR941816.fastq -S SRR941816.sam

  Конвертация в бам
- samtools view -@ 8 -Sb output.sam > output.bam

  Сортировка и индексирование
  
- samtools sort -@ 8 -o sorted_output.bam output.bam
- samtools index sorted_output.bam

Результаты работы hisat2:

```9043877 reads; of these:
  9043877 (100.00%) were unpaired; of these:
    512972 (5.67%) aligned 0 times
    7930593 (87.69%) aligned exactly 1 time
    600312 (6.64%) aligned >1 times
94.33% overall alignment rate
```

в) Подсчет с  featureCounts

featureCounts не может работать с файлами GFF. Нам необходимо преобразовать файл GFF в формат GTF. Для этого  воспользуемся программой gffread. 

- Convert from GFF to GTF (+ надо отфильтровать по gene_id):

``` sh gffread <input GFF> -T -o <output GTF>```

- Run the feature counts program:
```featureCounts -g transcript_id -a GCF_000146045.2_R64_genomic.gtf -o counts.txt -T 8  SRR941818_sort.bam SRR941819_sort.bam SRR941817_sort.bam SRR941816_sort.bam```

Результаты работы:

```sh 

 Load annotation file GCF_000146045.2_R64_genomic.gtf ...                   ||
||    Features : 6852                                                         ||
||    Meta-features : 6478                                                    ||
||    Chromosomes/contigs : 17                                                ||
||                                                                            ||
|| Process BAM file SRR941816_sort.bam...                                     ||
||    Single-end reads are included.                                          ||
||    Total alignments : 9773838                                              ||
||    Successfully assigned alignments : 7305537 (74.7%)                      ||
||    Running time : 0.05 minutes                                             ||
||                                                                            ||
|| Write the final count table.                                               ||
|| Write the read assignment summary.                                         ||
||                                                                            ||
|| Summary of counting results can be found in file "SRR941816_counts.txt.su  ||
|| mmary" 

```

Нам не нужны все колонки из выходного файла featureCounts для дальнейшего анализа, поэтому давайте упростим его.

Simplify the counts:
cat <output file from featureCounts> | cut -f 1,7-10 > simple_counts.txt

calculate metrics:
cat simple_counts.txt | R -f deseq2.r

3) Анализируем полученные результаты и строим heatmap 

- in text file: id	baseMean	log2FoldChange	lfcSE	stat	pvalue	padj
- norm-matrix-deseq2.txt содержит нормализованные подсчеты, которые мы будем использовать в визуализации

  По ним (norm-matrix-deseq2.txt) уже строим тепловую карту
- выбираем первые 50 генов
- ```head -n 50 result.txt | cut -f 1 | cut -d "-" -f 2 > genes.txt```
- Проводим GO







