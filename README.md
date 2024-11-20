#  Лабный журнал 

###  Записаны основые команды, которые были использованы для реализации проектов.

## Проекты

- [**Проект №1**](#проект-1-what-causes-abtibiotic-resistance)
- [**Проект №2**](#проект-2-why-did-i-get-the-flu-deep-sequencing-error-control-p-value-viral-evolution)

Создание окружения:

```sh
conda create -n bioINF
conda activate bioINF
```

## Проект №1. What causes abtibiotic resistance?

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

### 1. Скачиваем файлы секвенирования (SRA) с лейблом SRR1705851

- линк: https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/001/SRR1705851/

Проверим качество 

### Отчет FastQC

```sh
fastqc -o SRR1705851.fastq 
```

file:///Users/valeriaistuganova/Desktop/BioInf/project2/BioProject2/SRR1705851_fastqc.html


Анализ:

- Качество прочтений хорошее
- Среднее качество хорошее
- Шум от адаптеров - неоднородность состава нуклеотидов
- GC-состав - пик один
- Высокий уровень дупликаций - некотором смещении в сторону обогащения

Необходимо отфильтровать - 10 первых нуклеотидов обрежем

Обрезаем прочтения с помощью Trimmomatic через conda:bioconductor

```sh
trimmomatic PE -phred33 SRR1705851.fastq SRR1705851.results HEADCROP:10 | wc -l
```

### FastQC после обрезки 

```sh
fastqc SRR1705851.results
```

Все хорошо!


### 2. Скачивание референсного генома - reference sequence for the influenza hemagglutinin gene.

- линк:

Скачиваем через efetch по индентификатору:

Установка в окружение:

```sh
sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"
```
Комманда: 

```sh
efetch -db nucleotide -id KF848938.1 -format fasta > influenza_hemagglutinin.fa
```

Snakemake file - выравнивание

- Сортировка

```sh
samtools sort influenza_hemagglutinin.SRR1705851.unsorted.bam -o influenza_hemagglutininюSRR1705851.sorted.bam
```
- Индексация

```sh
samtools index influenza_hemagglutinin.SRR1705851юsorted.bam
```

total length:	52717864
average length:	147
Number of reads: 361116

- Статистика по выравниванию

361349 + 0 in total (QC-passed reads + QC-failed reads)
358265 + 0 primary
0 + 0 secondary
3084 + 0 supplementary
0 + 0 duplicates
0 + 0 primary duplicates
361116 + 0 mapped (99.94% : N/A)
358032 + 0 primary mapped (99.93% : N/A)
0 + 0 paired in sequencing
0 + 0 read1
0 + 0 read2
0 + 0 properly paired (N/A : N/A)
0 + 0 with itself and mate mapped
0 + 0 singletons (N/A : N/A)
0 + 0 with mate mapped to a different chr
0 + 0 with mate mapped to a different chr (mapQ>=5))

## Сортировка и индексация 

```sh
samtools sort influenza_hemagglutinin.SRR1705851.unsorted.bam -o influenza_hemagglutinin.SRR1705851.sorted.bam

samtools index influenza_hemagglutinin.SRR1705851.sorted.bam
```

samtools mpileup -d 3 -f influenza_hemagglutinin.fa influenza_hemagglutinin.SRR1705851.sorted.bam > influenza_hemagglutinin.SRR1705851.mpileup

VarScan mpileup2snp influenza_hemagglutinin.SRR1705851.mpileup --min-var-freq 0.95 --output-vcf 1 > VarScan_results.vcf 

cat VarScan_results.vcf | awk 'NR>24 {print $1, $2, $4, $10}'

cat VarScan_results.vcf | awk 'NR>24 {print $1, $2, $4, $10}' | awk -F ':' '{print $NF}' | awk -F ',' '{print $1}'

(How many variants are reported back?) - 5 SNV

Считаем глубину покрытия 

awk '{sum += $3} END {if (NR > 0) print "Average coverage:", sum / NR; else print "No data"}' coverage.txt
Average coverage: 29158,9 - Количество прочтений 


grep -v '^>' influenza_hemagglutinin.fa | tr -d '\n' | wc -c
    1665 - длина рефефренса



awk - awk 'NR%4==2 { total += length($0); count++ } END { print total/count }' SRR1705851.results

137,148 - Средняя длина рида 



samtools depth influenza_hemagglutinin.SRR1705851.sorted.bam | awk '{sum += $3; count++} END {if (count > 0) print sum/count; else print 0}'

29158,9

Выставим d - 29159  - это средняя глубина прочтения


Скачиваем контрольные образцы 

wget -c -O SRR1705858.fastq.gz  ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/008/SRR1705858/SRR1705858.fastq.gz 
wget -c -O SRR1705859.fastq.gz  ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/009/SRR1705859/SRR1705859.fastq.gz
wget -c -O SRR1705860.fastq.gz  ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/000/SRR1705860/SRR1705860.fastq.gz 

SRR1705858: ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/008/SRR1705858/SRR1705858.fastq.gz 
SRR1705859: ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/009/SRR1705859/SRR1705859.fastq.gz 
SRR1705860: ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/000/SRR1705860/SRR1705860.fastq.gz 

gunzip SRR1705858.fastq.gz SRR1705859.fastq.gz SRR1705860.fastq.gz


bwa mem -t 16 influenza_hemagglutinin.fa SRR1705858.fastq 2> log | samtools view -b - | samtools sort -o SRR1705858.influenza_hemagglutinin.sorted.bam - | samtools index SRR1705858.influenza_hemagglutinin.sorted.bam
bwa mem -t 16 influenza_hemagglutinin.fa SRR1705859.fastq 2> log | samtools view -b - | samtools sort  -o SRR1705859.influenza_hemagglutinin.sorted.bam - | samtools index SRR1705859.influenza_hemagglutinin.sorted.bam
bwa mem -t 16 influenza_hemagglutinin.fa SRR1705860.fastq 2> log | samtools view -b - | samtools sort  -o SRR1705860.influenza_hemagglutinin.sorted.bam - | samtools index > SRR1705860.influenza_hemagglutinin.sorted.bam


samtools mpileup  -f influenza_hemagglutinin.fa SRR1705858.influenza_hemagglutinin.sorted.bam > SRR1705858.influenza_hemagglutinin.mpileup
samtools mpileup  -f influenza_hemagglutinin.fa SRR1705859.influenza_hemagglutinin.sorted.bam > SRR1705859.influenza_hemagglutinin.mpileup
samtools mpileup  -f influenza_hemagglutinin.fa SRR1705860.influenza_hemagglutinin.sorted.bam > SRR1705860.influenza_hemagglutinin.mpileup

VarScan mpileup2snp SRR1705858.influenza_hemagglutinin.mpileup --min-var-freq 0.001 --output-vcf 1 > VarScan_resultsSRR1705858.vcf 
VarScan mpileup2snp SRR1705859.influenza_hemagglutinin.mpileup --min-var-freq 0.001 --output-vcf 1 > VarScan_resultsSRR1705859.vcf 
VarScan mpileup2snp SRR1705860.influenza_hemagglutinin.mpileup --min-var-freq 0.001 --output-vcf 1 > VarScan_resultsSRR1705860.vcf 


котрые надо проверить - 999 позиция и 72 позиция

cat VarScan_resultsSRR1705858.vcf | awk 'NR>24 {sum += $10; count++} END {if (count > 0) print "Среднее значение:", sum/count; else print "Нет данных."}'

#  Лабный журнал 

###  Записаны основые команды, которые были использованы для реализации проектов.

## Проекты

- [**Проект №1**](#проект-1-what-causes-abtibiotic-resistance)
- [**Проект №2**](#проект-2-why-did-i-get-the-flu-deep-sequencing-error-control-p-value-viral-evolution)

Создание окружения:

```sh
conda create -n bioINF
conda activate bioINF
```

## Проект №1. What causes abtibiotic resistance?

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

### 1. Скачиваем файлы секвенирования (SRA) с лейблом SRR1705851

- линк: https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/001/SRR1705851/

Проверим качество 

### Отчет FastQC

```sh
fastqc -o SRR1705851.fastq 
```

file:///Users/valeriaistuganova/Desktop/BioInf/project2/BioProject2/SRR1705851_fastqc.html


Анализ:

- Качество прочтений хорошее
- Среднее качество хорошее
- Шум от адаптеров - неоднородность состава нуклеотидов
- GC-состав - пик один
- Высокий уровень дупликаций - некотором смещении в сторону обогащения

Необходимо отфильтровать - 10 первых нуклеотидов обрежем

Обрезаем прочтения с помощью Trimmomatic через conda:bioconductor

```sh
trimmomatic PE -phred33 SRR1705851.fastq SRR1705851.results HEADCROP:10 | wc -l
```

### FastQC после обрезки 

```sh
fastqc SRR1705851.results
```

Все хорошо!


### 2. Скачивание референсного генома - reference sequence for the influenza hemagglutinin gene.

- линк:

Скачиваем через efetch по индентификатору:

Установка в окружение:

```sh
sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"
```
Комманда: 

```sh
efetch -db nucleotide -id KF848938.1 -format fasta > influenza_hemagglutinin.fa
```

Snakemake file - выравнивание

- Сортировка

```sh
samtools sort influenza_hemagglutinin.SRR1705851.unsorted.bam -o influenza_hemagglutininюSRR1705851.sorted.bam
```
- Индексация

```sh
samtools index influenza_hemagglutinin.SRR1705851юsorted.bam
```

total length:	52717864
average length:	147
Number of reads: 361116

- Статистика по выравниванию

361349 + 0 in total (QC-passed reads + QC-failed reads)
358265 + 0 primary
0 + 0 secondary
3084 + 0 supplementary
0 + 0 duplicates
0 + 0 primary duplicates
361116 + 0 mapped (99.94% : N/A)
358032 + 0 primary mapped (99.93% : N/A)
0 + 0 paired in sequencing
0 + 0 read1
0 + 0 read2
0 + 0 properly paired (N/A : N/A)
0 + 0 with itself and mate mapped
0 + 0 singletons (N/A : N/A)
0 + 0 with mate mapped to a different chr
0 + 0 with mate mapped to a different chr (mapQ>=5))

## Сортировка и индексация 

```sh
samtools sort influenza_hemagglutinin.SRR1705851.unsorted.bam -o influenza_hemagglutinin.SRR1705851.sorted.bam

samtools index influenza_hemagglutinin.SRR1705851.sorted.bam
```

samtools mpileup -d 3 -f influenza_hemagglutinin.fa influenza_hemagglutinin.SRR1705851.sorted.bam > influenza_hemagglutinin.SRR1705851.mpileup

VarScan mpileup2snp influenza_hemagglutinin.SRR1705851.mpileup --min-var-freq 0.95 --output-vcf 1 > VarScan_results.vcf 

cat VarScan_results.vcf | awk 'NR>24 {print $1, $2, $4, $10}'

cat VarScan_results.vcf | awk 'NR>24 {print $1, $2, $4, $10}' | awk -F ':' '{print $NF}' | awk -F ',' '{print $1}'

(How many variants are reported back?) - 5 SNV

Считаем глубину покрытия 

awk '{sum += $3} END {if (NR > 0) print "Average coverage:", sum / NR; else print "No data"}' coverage.txt
Average coverage: 29158,9 - Количество прочтений 


grep -v '^>' influenza_hemagglutinin.fa | tr -d '\n' | wc -c
    1665 - длина рефефренса



awk - awk 'NR%4==2 { total += length($0); count++ } END { print total/count }' SRR1705851.results

137,148 - Средняя длина рида 



samtools depth influenza_hemagglutinin.SRR1705851.sorted.bam | awk '{sum += $3; count++} END {if (count > 0) print sum/count; else print 0}'

29158,9

Выставим d - 29159  - это средняя глубина прочтения


Скачиваем контрольные образцы 

wget -c -O SRR1705858.fastq.gz  ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/008/SRR1705858/SRR1705858.fastq.gz 
wget -c -O SRR1705859.fastq.gz  ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/009/SRR1705859/SRR1705859.fastq.gz
wget -c -O SRR1705860.fastq.gz  ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/000/SRR1705860/SRR1705860.fastq.gz 

SRR1705858: ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/008/SRR1705858/SRR1705858.fastq.gz 
SRR1705859: ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/009/SRR1705859/SRR1705859.fastq.gz 
SRR1705860: ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/000/SRR1705860/SRR1705860.fastq.gz 

gunzip SRR1705858.fastq.gz SRR1705859.fastq.gz SRR1705860.fastq.gz


bwa mem -t 16 influenza_hemagglutinin.fa SRR1705858.fastq 2> log | samtools view -b - | samtools sort -o SRR1705858.influenza_hemagglutinin.sorted.bam - | samtools index SRR1705858.influenza_hemagglutinin.sorted.bam
bwa mem -t 16 influenza_hemagglutinin.fa SRR1705859.fastq 2> log | samtools view -b - | samtools sort  -o SRR1705859.influenza_hemagglutinin.sorted.bam - | samtools index SRR1705859.influenza_hemagglutinin.sorted.bam
bwa mem -t 16 influenza_hemagglutinin.fa SRR1705860.fastq 2> log | samtools view -b - | samtools sort  -o SRR1705860.influenza_hemagglutinin.sorted.bam - | samtools index > SRR1705860.influenza_hemagglutinin.sorted.bam


samtools mpileup  -f influenza_hemagglutinin.fa SRR1705858.influenza_hemagglutinin.sorted.bam > SRR1705858.influenza_hemagglutinin.mpileup
samtools mpileup  -f influenza_hemagglutinin.fa SRR1705859.influenza_hemagglutinin.sorted.bam > SRR1705859.influenza_hemagglutinin.mpileup
samtools mpileup  -f influenza_hemagglutinin.fa SRR1705860.influenza_hemagglutinin.sorted.bam > SRR1705860.influenza_hemagglutinin.mpileup

VarScan mpileup2snp SRR1705858.influenza_hemagglutinin.mpileup --min-var-freq 0.001 --output-vcf 1 > VarScan_resultsSRR1705858.vcf 
VarScan mpileup2snp SRR1705859.influenza_hemagglutinin.mpileup --min-var-freq 0.001 --output-vcf 1 > VarScan_resultsSRR1705859.vcf 
VarScan mpileup2snp SRR1705860.influenza_hemagglutinin.mpileup --min-var-freq 0.001 --output-vcf 1 > VarScan_resultsSRR1705860.vcf 


