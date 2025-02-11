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
 
#### 2) Для определение по Y хромосоме воспользуемся тулом [Y-DNA_tool]([https://isogg.org/wiki/Y-DNA_tools](https://mitoydna.org/))


