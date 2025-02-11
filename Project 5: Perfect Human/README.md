# Project 5: Perfect Human 

- Данные для реализации проекта были взяты в [репозитории](https://github.com/msporny/dna)

У нас имеются данные SNPs, для каждой замены прописаны ее позиция, номер хромосомы и  идентификатор

## 1. Конвертируем формат 23andMe's raw data в стандартный vcf формат с помошью утилиты plink (можно также воспользоваться bcftools convert)

Справка: Формат 23andMe представляет собой текстовый формат хранения данных генотипирования и содержит 4 поля, разделенных табуляцией

Команда:
  
- ``sh plink --23file ManuSporny-genome.txt --recode vcf --out snps_clean --output-chr MT --snps-only just-acgt ``

- --snps-only исключает все варианты с одной или несколькими многосимвольными кодами аллелей
существуют, из-за низкой вероятности двойного изменения пары оснований в одной и той же паре оснований)

## 2. Какое значения имеют SNPs в наших данных?

- Обрабатываем в базе данных ClinVar

## 3. Определение гаплогруппы 

#### 1) Для определение по митохондриальной ДНК воспользуемся тулом [mthap](https://dna.jameslick.com/mthap/)

На вход программа принимает исходный файл в формате 23andMe's

Результат: Found 2708 markers at 2558 positions covering 15.4% of mtDNA. ([полный отчет](https://github.com/Valeriisht/BI_Practice_2024/blob/main/Project%205%3A%20Perfect%20Human/ManuSporny-genome%E2%80%94mtDNA%20Haplogroup%20Analysis%20Report.pdf))

Best mtDNA Haplogroup Matches: M6a

- Гаплогруппа M6  встречается преимущественно в долине Инда и на западных берегах Бенгальского залива, где представлены ее субклады M6a и M6b.
 
#### 2) Для определение по Y хромосоме воспользуемся тулом [Y-DNA_tool](https://ytree.morleydna.com/extractFromAutosomal)

Результаты: Y - 3483 markers (1286 no-calls) (отчет)

Данные имеют:

3480 unrecognised position(s). Are you using data from a source other than AncestryDNA, 23andMe or MyHeritage?
1 recognised mutation(s) with positive calls.
0 recognised mutation(s) with negative calls.
1286 recognised mutation(s) with no-calls.


### 4. Аннотация пола и цвета глаз 

- По [статье](https://pmc.ncbi.nlm.nih.gov/articles/PMC3694299/) определяем, какие именно варианты SNPs имеются, которые отвечают за цвет гласс

- VCF-файл открываем в IGV, определяем, в каких генах находятся

SNPs, отвечающие за цвет глаз: 
- rs12913832 /AG/01  в *HERC2*
- rs154537 G./00 *OCA2*
- rs16891982 CG/01  в *SLC45A2*
- rs1426654 AG/01 в *SLC24A5*
- rs885479 G./00 в *MC1R*
- rs6119471 в *ASIP*
- rs12203592 C./00 в *IRF4*




