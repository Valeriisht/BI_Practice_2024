#  Лабный журнал 

###  Записаны основые команды, которые были использованы для реализации проектов.

## Проекты

- [**Проект №1**](#проект-1-what-causes-abtibiotic-resistance)
- [**Проект №2**](#проект-2-why-did-i-get-the-flu-deep-sequencing-error-control-p-value-viral-evolution)
- [**Проект №3**](#проект-3-ecoli-outbreak-investigation)
- [**Проект №4**](#проект-4-tardigrades-from-genestealers-to-space-marines)

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

## Поиск SNV в исследуемом образце

### 1. Скачиваем файлы секвенирования (SRA) с лейблом SRR1705851

**Проект сделан с помощью утилиты SnakeMaske, в репозитории приложен файл**

Ниже продублированы основные шаги

- линк: https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/001/SRR1705851/

```sh
wget -c -O SRR1705851.fastq.gz {URL1}
```

Проверим качество 

### Отчет FastQC

```sh
fastqc  SRR1705851.fastq 
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

*Краткая статистика*

total length:	52717864
average length:	147
Number of reads: 361116


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

### 3. Выравнивание на референсный ген геммагглютинина (проведена индексация прежде), сортировка и индексация 

```sh
bwa mem -t 16 influenza_hemagglutinin.fa SRR1705851.fastq 2> log | samtools view -b - | samtools sort -o influenza_hemagglutinin.SRR1705851.sorted.bam - | samtools index influenza_hemagglutinin.SRR1705851.sorted.bam
```
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

### 4. mpileup -  генерации текстового формата pileup из данных по выравниванию 

Важно указать флаг -d, который который задает максимальную  глубину покрытия, которую следует учитывать при генерации выходных данных.

Для того, захватить и учесть все возможные варианты, мы должны посчитать среднее покрытие и выбрать -d не меньше, чем покрытие в нашем образце

Средняя глубина покрытия считается: количество ридов * средняя длина проччтений / длина эталлонного генома 

- С помощью команды ```samtools depth``` вытащим информацию о покрытие при выравнивании.  После с помощью awk посчитаем среднее покрытие. 

```sh
awk '{sum += $3} END {if (NR > 0) print "Average coverage:", sum / NR; else print "No data"}' coverage.txt

``` 
Получили Average coverage: 29158,9 

#### Перепроверка 

- Количество ридов из fastqc-report

Number of reads: 361116

- Посчитаем  длину рефефренса

```sh
grep -v '^>' influenza_hemagglutinin.fa | tr -d '\n' | wc -c
```

1665 - длина рефефренса

- Посчитаем среднюю длину ридов

```sh
 awk 'NR%4==2 { total += length($0); count++ } END { print total/count }' SRR1705851.results
```

137,148 - Средняя длина рида 

- Покрытие

361116*137,148/1665 = 29 745,548  

То есть, флаг d должен быть не меньше  29 745,548 
Выставим d - 360 000 - по количесству ридов в целом, таким образом,  мы точно сохраним все возможные варианты 

```sh
samtools mpileup -d 360 000 -f influenza_hemagglutinin.fa influenza_hemagglutinin.SRR1705851.sorted.bam > influenza_hemagglutinin.SRR1705851.mpileup
```

### 5. Variant calling

Вывявление SNV с высокой частотой встречаемости:

```sh
VarScan mpileup2snp influenza_hemagglutinin.SRR1705851.mpileup --min-var-freq 0.95 --output-vcf 1 > VarScan_up_results.vcf
```
Получили 5 вариантов  

Вывявление SNV с частотой встречаемоти не ниже 0,1% (+редкие варианты):

```sh
VarScan mpileup2snp influenza_hemagglutinin.SRR1705851.mpileup --min-var-freq 0.001 --output-vcf 1 > VarScan_low_results.vcf
```
Получили 21 вариант 

### 6. Парсинг VCF файла 

cat VarScan_results.vcf | awk 'NR>24 {print $1, $2, $4, $10}'

## Обнаружение ошибок амплификации и секвенирования

- Скачиваем контрольные образцы 

```sh
wget -c -O SRR1705858.fastq.gz  ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/008/SRR1705858/SRR1705858.fastq.gz 
wget -c -O SRR1705859.fastq.gz  ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/009/SRR1705859/SRR1705859.fastq.gz
wget -c -O SRR1705860.fastq.gz  ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/000/SRR1705860/SRR1705860.fastq.gz 
```
- Распаковка

 ```sh
gunzip SRR1705858.fastq.gz SRR1705859.fastq.gz SRR1705860.fastq.gz
```
- Выравнивание, сортировка и  индексация

 ```sh
bwa mem -t 16 influenza_hemagglutinin.fa SRR1705858.fastq 2> log | samtools view -b - | samtools sort -o SRR1705858.influenza_hemagglutinin.sorted.bam - | samtools index SRR1705858.influenza_hemagglutinin.sorted.bam
bwa mem -t 16 influenza_hemagglutinin.fa SRR1705859.fastq 2> log | samtools view -b - | samtools sort  -o SRR1705859.influenza_hemagglutinin.sorted.bam - | samtools index SRR1705859.influenza_hemagglutinin.sorted.bam
bwa mem -t 16 influenza_hemagglutinin.fa SRR1705860.fastq 2> log | samtools view -b - | samtools sort  -o SRR1705860.influenza_hemagglutinin.sorted.bam - | samtools index > SRR1705860.influenza_hemagglutinin.sorted.bam
```

- Генерация pileup

```sh
samtools mpileup  -f influenza_hemagglutinin.fa SRR1705858.influenza_hemagglutinin.sorted.bam > SRR1705858.influenza_hemagglutinin.mpileup
samtools mpileup  -f influenza_hemagglutinin.fa SRR1705859.influenza_hemagglutinin.sorted.bam > SRR1705859.influenza_hemagglutinin.mpileup
samtools mpileup  -f influenza_hemagglutinin.fa SRR1705860.influenza_hemagglutinin.sorted.bam > SRR1705860.influenza_hemagglutinin.mpileup
```
### 7. Variant calling

```sh
VarScan mpileup2snp SRR1705858.influenza_hemagglutinin.mpileup --min-var-freq 0.001 --output-vcf 1 > VarScan_resultsSRR1705858.vcf 
VarScan mpileup2snp SRR1705859.influenza_hemagglutinin.mpileup --min-var-freq 0.001 --output-vcf 1 > VarScan_resultsSRR1705859.vcf 
VarScan mpileup2snp SRR1705860.influenza_hemagglutinin.mpileup --min-var-freq 0.001 --output-vcf 1 > VarScan_resultsSRR1705860.vcf 
```

### 8. IGC

Подгружаем в геномный браузер и фильтруем. Встречающиеся SNV и в контрольных образцах, и в исследуемом образце указывают на ошибки секвыенирования - были отсеяны. Уникальными оказались SNV в позиции 307 и 1458

### 9. Парсинг vcf-файла 

Парсинг vcf-файла осуществлялся в питоне с помощью библиотеки pandas - файл приложен в репозитории 

Посчитаны средние частоты SNV и стандартные отклонения в контрольных образцах. Пороговое значение для фильтрации оказалось равным ~ 0,4%. Частоты SNV, ниже порогового значения, рассматривались, как ошибки секвенирования.  

## Проект №3. E.coli outbreak investigation 

#### В данном проекте мы занимаемся сбором генома патогенной кишечной палочки, бактерии, вызвавшей вспышку заболевания. Для этого мы используем ассемблер SPAdes и проводим анализ факторов, которые могли способствовать возникновению патогенного штамма.

Реализация пунктов 1-4 приведена в файле Snakefile3 (Папка Project3/Snakefile)

### 1) Скачаем данные секвенирования TY2482 образца

   - SRR292678 - paired end, insert size 470 bp (forward reads, reverse reads, 400 Mb each)
   - SRR292862 – mate pair, insert size 2 kb, (forward reads, reverse reads, 200 Mb each)
   - SRR292770 – mate pair, insert size 6 kb, (forward reads, reverse reads, 200 Mb each)

### 2) Анализируем данные с помощью fastqc

   Число ридов в каждом образце:
   paired end: 5.5 M (1,5 дибликаты)
   mate pair 2kb: 5.1 M
   mate pair 6kb: 5.1 M

All samples have sequences of a single length (49bp, 90bp)

*Ремарка: Insert sizes refer to the length of the DNA fragments that are sequenced between the adapter sequences in a sequencing library*

#### Дополнителоьно запускаем multiqc для того, чтобы анализировать данные со всех прочтений

- в целом данные очень хорошие (ничего не обрезаем)

### 3) Определимся с длиной к-меров.

Для подсчета к-меров используем  программу Jellyfish - производит быстрый подсчет кмеров (подсчитает частоту всех возможных кмеров заданной длины в наших данных)

Подгружаем эту программу в окружение:

```sh
conda config --add channels conda-forge #удостоверимся, что доступен канал
conda install jellyfish #установка
jellyfish --version #проверка установки 
```

Опции программы:

-m или «mer» задает длину.
-C - игнорировать направленность (каждое чтение рассматривается как его обратное дополнение).
-s - начальная оценка размера хэш-таблицы, которую использует jellyfish, set > genome size
-o задает имя выходного файла

Запускаем программу подсчета к-меров:

```sh
jellyfish count -m 31 -s 10000000 <(zcat {input.sample1}) <(zcat {input.sample2}) -o {output}
```

Визуализация по гистограмме - график приложен "jellyfish histo"

Cлева находится список бинов (количество повторений к-мера или его «глубина»)
Cправа - подсчет количества к-меров в данных, которые соответствуют данной категории

Оценим размер генома по формуле: 


N = (M*L)/(L-K+1)
Размер генома = T/N

- N - глубина покрытия
- M - пик Kmer,
- K - размер Kmer
- L - средняя длина чтения
- T - общее количество оснований

N = (65*90)/(90-31+1) = 97.5

T = 5499346 * 90

Размер генома =  5499346 * 90 / 97.5 = 5.076.319

Визуализируем с помощью библиотеку matplotlib (файлы в папке "Histo_jellyfish") или онлайн приложения http://genomescope.org
Пик приходится на 65 (покрытие)



### 5) Запуск SPAdes

Соберем геном кишечной палки 

Запускаем только на парно-концевых прочтениях

```sh
spades.py -t 16 --pe1-1 libraries/forward_PE.fastq.gz --pe1-2 libraries/reverse_PE.fastq.gz -o results/spades/pair_end
```

Запускаем на трех библиотеках для разрешения длинных/коротких повторов

```sh
spades.py -t 16 \
--pe1-1 libraries/forward_PE.fastq.gz --pe1-2 libraries/reverse_PE.fastq.gz \
--mp1-1 libraries/forward_MP_2.fastq.gz --mp1-2 libraries/reverse_MP_2.fastq.gz \
--mp2-1 libraries/forward_MP_6.fastq.gz --mp2-2 libraries/reverse_MP_6.fastq.gz \
-o results/spades/three_libs_spades_out
```
### 6) Оценка качества полученной сборки

- pair_end
  
```sh
python quast-5.3.0/quast.py results/spades/pair_end/contigs.fasta -o results/quast/pair_end/contigs
python quast-5.3.0/quast.py results/spades/pair_end/scaffolds.fasta -o results/quast/pair_end/scaffolds 
```

- all

```sh
python quast-5.3.0/quast.py results/spades/three_libs_spades_out/contigs.fasta -o results/quast/all/contigs
python quast-5.3.0/quast.py results/spades/three_libs_spades_out/scaffolds.fasta -o results/quast/all/scaffolds 
```

### 7) Prokka - аннотация генома

**Этот инструмент определяет координаты предполагаемых генов в контигах, а затем использует BLAST для аннотации на основе сходства, используя все белки из секвенированных бактериальных геномов в базе данных RefSeq**

```sh
prokka results/three_libs_spades/scaffolds.fasta -o results/prokka
```

### 8) Поиск ближайшего родственника *E. coli X*

По эволюционно консервативному гену 16S ribosomal RNA

Сначала вытащим этот ген из нашей патогенной бактерии с помощью  Barrnap

```sh
barrnap results/three_libs_spades_out/scaffolds.fasta --outseq results/barrnap/barr.fna
```
### 9) Идем в бласт и ищем макисмально похожий организм с таким же 16S RNA геном, как и наша бактерия

Последовательность 16S RNA выровнялась на 

Name and GenBank accession number of the reference *E.coli* strain: Escherichia coli 55989, NC_011748

Скачиваем референсный геном:

```sh
efetch -db nucleotide -id NC_011748.1 -format fasta > 55989.fasta
```

### 10) Какова генетическая причина HUS?

Проведем полногеномное сравнение с эталонным геномом и проанализируем регионы, в которых эти штаммы отличаются друг от друга

 Используем Mauve программу для визуализации Locally Collinear Blocks (LCBs)
 
 - Открываем программу и запускам выравнивание собранного генома и референса
 - Визуализируем
   
 Locally Collinear Blocks (LCBs)
 
Геном E. coli X кодирует гены токсинов, похожих на шига-токсин - StxA и StxB
Происхождение этих генов токсинов у *E.coli* X - горизонтальный перенос и встравиание фага (рядом расположены гены интеграз) 


### 11) Детекция генов устойчивости к антибиотикам

use ResFinder (http://genepi.food.dtu.dk/resfinder) - специальный поиск в базе данных генов, связанных с устойчивостью к антибиотикам

Выявление устойчивости к streptomycin - aminoglycoside - рядом располагаются гены рекомбиназ - перенос горизонтальный 

# Проект 4. Tardigrades: from genestealers to space marines 

- **Проводим функциональную анатацию генома тихоходки**

- Сборщики генома прокариот:SOAPdenovo, Platanus or DISCOVAR, также основаны на графе де Брюйна

1. Скачиваем референсный геном

```sh
ftp.ncbi.nlm.nih.gov/genomes/all/GCA/001/949/185/GCA_001949185.1_Rvar_4.0/GCA_001949185.1_Rvar_4.0_genomic.fna.gz
```

2. AUGUSTUS

**Это программа для предсказания генов в геномных последовательностях эукариот**

Принцип работы:
- Метод ab initio: Augustus использует статистические модели для предсказания генов на основе известных последовательностей
- Augustus применяет скрытые марковские модели для анализа последовательностей ДНК и определения вероятных мест расположения генов

Скачиваем результаты работы прорраммы (энергозатратный процесс предсказания)

3. Извлечение белковых последовательностей

- С помощью программ the getAnnoFasta.pl script

  С помошью команды запускаем скрипт и сохраняем только CDS:
  
  ```sh
  perl getAnnoFasta.pl augustus.whole.gff
  ```
  Посчитаем количесвто предсказанных элементов

  ```sh
  grep ">" augustus.whole.aa | wc -l     
  ```
  Результат:  16435
  

4. Выравнивание по базе данных

   - У нас есть фацл (piptides.txt), который был получен по результатам масс-спектрометрии. В файле содержиться информация, какие белки ассоциированые с участками ДНК (иммуно-преципитация хроматина)
   - С помощью blast мы выбираем только ассоциированные с ДНК белки -> для этого по базе данных на основе результатов предсказателя Augustus выравниваем пептиды, полученные с помощью масс-спектрометрии
   
   1) Создаем базу данных
   
   ```sh
   makeblastdb -in augustus.whole.aa -dbtype prot  -out targidrata_db
   ```

   2) Выравниваем
      
   ```sh
   blastp -query nucl_proteins -db swissprot -out protein_name -evalue 0.001 -outfmt "6 qseqid sacc evalue pident qcovs stitle"
   ```
   Итог: обнаружено 36 белков 
5.  Сохраняем только нужные последовательности

- Воспользуемся утилитой seqkt, что сохранить только название пептидов
- Сначала из файла protein_name сохраним только id выравненых последовательностей

  ```sh
  awk '{print $2}' protein_name | sort | uniq > protein_id.txt
  ```
- Далее получаем аминокислотные последовательности белков 
```sh
seqtk subseq augustus.whole.aa protein_id.txt > protein_seq.fasta
```
6.  Предсказание с помощью TargetP Server и Wolf PSORT
   
- PSORT предсказывает клеточную локализацию белков на основе наличия сигнального пептида на их N-конце.  

Результаты: queryProtein WoLFPSORT prediction extr: 20, cyto: 8, cyto_nucl: 7, nucl: 4 

- Для предсказания субклеточной локализации бьелка воспользуемся утилитой TargetP Server
- Определение локализации белка основано на предсказании присутствия любой из N-концевой последовательности:  cTP хлоропластов, mTP митохондриального, или сигнального пептида секреторного пути (SP)
  
- Загружаем последовательность белков и анализируем результаты работиы программы

Нам не интересны белки, для какторых правдаподобии выше 0.8, так как это означает, что белок скорее всего экспортируется из клетки и не работает в ядре.

Отфильтруем: 

```sh
awk '$4 < 0.01 {print $1}' output_protein_type.txt > filter_protein_seq
```
Или с помощью python script

7. Выравниваем обнаруженные белки на базу данных UniProtKB/Swiss-Prot

8. Предсказание Pfam

- Так как не для всех белков мы нашли ортологи, мы воспользуемся HMMER для поиска наших белковых последовательностей по базе  HMM для различных белковых доменов и мотивов.

9. Создаем таблицу
- По результатам делаем таблицу с информацией об обнаруженных белках 



   















