#  Лабный журнал 

###  Записаны основые команды, которые были использованы для реализации проектов.

## Проекты

- [**Проект №1**](## "Проект №1. What causes abtibiotic resistance?")
- [**Проект №2**](## "Проект №2. “Why did I get the flu?”. Deep sequencing, error control, p-value, viral evolution..")

## Проект №1. What causes abtibiotic resistance?

Создание окружения:

```sh
conda create -n hw_1_anib_resis
conda activate hw_1_anib_resis
```

Скачивание файла: 

- wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/
  
- wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.gff.gz
  
Перейти на сайт https://doi.org/10.6084/m9.figshare.10006541.v3 и там скачать два файла amp_res_1.fastq.gz и amp_res_2.fastq.gz

### Смотрим статистику по файлу 

```sh
conda install -c bioconda seqkit
```

### Установка FastQC файла 

```sh
brew install fastqc
```

### Отчет FastQC

```sh
fastqc -o . /pathtofile1/file1.fastq /pathtofile2/file2.fastq 
```

file:///Users/valeriaistuganova/Desktop/BioInf/project1/amp_res_1_fastqc.html

file:///Users/valeriaistuganova/Desktop/BioInf/project1/amp_res_2_fastqc.html

Анализ:

- Низкое качество к концу прочтений
- Среднее качество неплохое
- Шум от адаптеров - неоднородность состава нуклеотидов
- GC-состав - пик один
- N нуклеотидов небольшое количество

Необходимо отфильтровать - несколько первых нуклеотидовт (13), 10 последних нуклеотидов 

Обрезаем прочтения с помощью Trimmomatic через conda:bioconductor

```sh
trimmomatic PE -phred33 amp_res_1.fastq amp_res_2.fastq -baseout amp.results CROP:86 HEADCROP:20 | wc -l
```

Результат: 

Reverse Only Surviving: 0 (0,00%) Dropped: 0 (0,00%)

TrimmomaticPE: Completed successfully

### FastQC после обрезки 

```sh
fastqc amp.results_1P amp.results_2P
```

Все хорошо!

### Выравнивание

- index 

```sh
bwa index GCF_000005845.2_ASM584v2_genomic.fna.gz 
```
- Alignment 

```sh
bwa mem GCF_000005845.2_ASM584v2_genomic.fna.gz amp.results_1P amp.results_2P > alignment.sam 
```
- Переводим в bam

```sh
samtools view -S -b alignment.sam > alignment.bam
samtools flagstat alignment.bam
```

- Невыровненные файлы запишем отдельно 

```sh
samtools view -f 4 -h alignment.sam | samtools fasta | head -40 > unmapped_reads.alignment.fa  
```

 - индексируем и сортируем bam 

```sh
samtools sort alignment.bam -o alignment_sorted.bam

samtools index alignment_sorted.bam
```

### Variant calling

```sh
samtools mpileup -f GCF_000005845.2_ASM584v2_genomic.fna alignment_sorted.bam >  my.mpileup

conda install bioconda::varscan
```

- поиск однонуклеотидных замен

```sh
VarScan mpileup2snp my.mpileup --min-var-freq 0.1 --output-vcf 1 > VarScan_results.vcf 
```

- статистика
  
Min coverage:	8

Min reads2:	2

Min var freq:	0.1

Min avg qual:	15

P-value thresh:	0.01

Reading input from my.mpileup

4640878 bases in pileup file

8 variant positions (7 SNP, 1 indel)

0 were failed by the strand-filter

7 variant positions reported (7 SNP, 0 indel)


###  Variant effect prediction

- автоаннотиация

```sh
conda install bioconda::snpeff

touch snpEff.config 

add k12.genome : ecoli_K12

mkdir -p data/k12

gunzip GCF_000005845.2_ASM584v2_genomic.gbff.gz

cp GCF_000005845.2_ASM584v2_genomic.gbff data/k12/genes.gbk 

snpEff build -genbank -v k12

snpEff ann k12 VarScan_results.vcf > VarScan_results_annotated.vcf
```

### Подгружаем в IGV


## Проект №2. “Why did I get the flu?”. Deep sequencing, error control, p-value, viral evolution..









