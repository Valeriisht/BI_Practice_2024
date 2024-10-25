#  Лабный журнал 

###  Записаны основые команды, которые были использованы для реализации проекта.

## Проект №1. What causes abtibiotic resistance?

Создание окружения:

- conda create -n hw_1_anib_resis
- conda activate hw_1_anib_resis

Скачивание файла: 

- wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/
- wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.gff.gz
  
Перейти на сайт https://doi.org/10.6084/m9.figshare.10006541.v3 и там скачать два файла amp_res_1.fastq.gz и amp_res_2.fastq.gz

### Смотрим статичтику по файлу 

- conda install -c bioconda seqkit

file                format  type  num_seqs     sum_len  min_len  avg_len  max_len
amp_res_1.fastq.gz  FASTQ   DNA    455,876  46,043,476      101      101      101
