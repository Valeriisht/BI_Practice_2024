# Project 5: Perfect Human 

- Данные для реализации проекта были взяты в [репозитории](https://github.com/msporny/dna)

У нас имеются данные SNPs, для каждой замены прописаны ее позиция, номер хромосомы и  идентификатор

## 1. Конвертируем формат 23andMe's raw data в стандартный vcf формат с помошью утилиты plink (можно также воспользоваться bcftools convert)

Справка: Формат 23andMe представляет собой текстовый формат хранения данных генотипирования и содержит 4 поля, разделенных табуляцией

Команда:
  
- ``sh plink --23file SNP_raw_v4_Full_20170514175358.txt  --recode vcf --out snps_clean --output-chr MT --snps-only just-acgt ``

- --snps-only исключает все варианты с одной или несколькими многосимвольными кодами аллелей
существуют, из-за низкой вероятности двойного изменения пары оснований в одной и той же паре оснований)

Inferred sex: male.

## 2. Какое значения имеют SNPs в наших данных?

- Обрабатываем в базе данных ClinVar

## 3. Определение гаплогруппы 

#### 1) Для определение по митохондриальной ДНК воспользуемся тулом [mthap](https://dna.jameslick.com/mthap/)

На вход программа принимает исходный файл в формате 23andMe's

Результат: Found 2708394 markers at 2137144 positions covering 100.0% of mtDNA. ([полный отчет](https://github.com/Valeriisht/BI_Practice_2024/blob/main/Project%205%3A%20Perfect%20Human/ManuSporny-genome%E2%80%94mtDNA%20Haplogroup%20Analysis%20Report.pdf))

Best mtDNA Haplogroup Matches: H2a2a1
 
#### 2) Для определение по Y хромосоме воспользуемся тулом [Y-DNA_tool](https://ytree.morleydna.com/extractFromAutosomal) и [cladefinder](https://cladefinder.yseq.net/)

Результаты: 
- 63 Y-DNA position(s) lacking mutations recognised by the genetic genealogy community. These Y-DNA positions may not be very useful.
- 166 recognised mutation(s) with positive calls.
- 733 recognised mutation(s) with negative calls.
- 1086 recognised mutation(s) with no-calls.
(отчет)

Most specific position on the YFull YTree is R-M417 

### 4. Аннотация пола и цвета глаз 

- По [статье](https://pmc.ncbi.nlm.nih.gov/articles/PMC3694299/) определяем, какие именно варианты SNPs имеются, которые отвечают за цвет гласс

- VCF-файл открываем в IGV, определяем, в каких генах находятся

SNPs, отвечающие за цвет глаз: 
- rs12913832 /AG/01  в *OCA2* - linked to blue or brown eye color
- rs154537 G./00 *OCA2*
- rs16891982 CG/01  в *SLC45A2* - G allele homozygosity is associated with light skin, hair, and eye color
- rs1426654 AG/01 в *SLC24A5* 
- rs885479 G./00 в *MC1R*
- rs6119471 в *ASIP*
- rs12203592 CT/01 в *DUSP22*

### 5. Аннотация всех SNP, отбор клинически значимых вариантов 

- С помощью snpEff находим всю информацию об обнаруженных SNPs
  
  1) Скачиваем сборку
     - ```   java -jar snpEff.jar download -v GRCh37.75 ```
  2) Аннотируем
     - ``` java -jar snpEff.jar -v GRCh37.75 ../snps_clean.vcf  > ../snps_snpeff.vcf ```
- Связываем с фенотипом по базе ClinVar:
  - ``` sh java -jar SnpSift.jar annotate clinvar.vcf  snps_clean.vcf > snps_clean_snpsift_clinvar.vcf ```
- Отбираем клинически значимые варианты
  - 

### 6. Для идентификации роли обнаруженных SNV используем базу данных OMIM и также tool openCRAVAT, gnomAD и Franklin

