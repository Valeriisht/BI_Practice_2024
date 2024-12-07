from humanfriendly.terminal import output

URL1="https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR170/001/SRR1705851/SRR1705851.fastq.gz"

rule sample_download:
    output:
        "{sample}.fastq.gz"
    shell:
        "wget -c -O {output} {URL1}"

rule sample_unzip:
    input:
        "{sample}.fastq.gz"
    output:
        "{sample}.fastq",
    shell:
        "gunzip -c {input} > {output}"

rule fastqc_report:
    input:
        "{sample}.fastq"
    output:
        "{sample}.results"
    shell:
        "trimmomatic SE -phred33 {input} {output} HEADCROP:10 | wc -l"

rule reference_download:
    output:
        "influenza_hemagglutinin.fa"
    shell:
        "efetch -db nucleotide -id KF848938.1 -format fasta > {output}"

rule bwa_index:
    input:
        "{reference}.fa"
    output:
        "{reference}.fa.amb",
        "{reference}.fa.ann",
        "{reference}.fa.bwt",
        "{reference}.fa.pac",
        "{reference}.fa.sa",
    shell:
        "bwa index {input}"

rule bwa_map:
    input:
        "{reference}.fa.amb",
        "{reference}.fa.ann",
        "{reference}.fa.bwt",
        "{reference}.fa.pac",
        "{reference}.fa.sa",
        ref="{reference}.fa",
        sample="{sample}.results"
    threads: 16
    log: "{reference}.{sample}.bwa.log"
    output:
        "{reference}.{sample}.sorted.bam",
        "{reference}.{sample}.sorted.bam.bai"
    shell:
        "bwa mem -t {threads} {input.ref} {input.sample} 2>{log} | samtools view -S -b | samtools sort -o {output[0]} - && samtools index {output[0]}"

rule mpileup:
    input:
        ref="influenza_hemagglutinin.fa",
        sample="influenza_hemagglutinin.SRR1705851.sorted.bam"
    output:
        "influenza_hemagglutinin.SRR1705851.mpileup"
    shell:
        "samtools mpileup -d 360000 -f {input.ref} {input.sample} > {output}"

rule VarScan_up:
    input:
        "influenza_hemagglutinin.SRR1705851.mpileup"
    output:
        "VarScan_up_results.vcf"
    shell:
        "VarScan mpileup2snp {input} --min-var-freq 0.95 --output-vcf 1 > {output}"

rule VarScan_low:
    input:
        "influenza_hemagglutinin.SRR1705851.mpileup"
    output:
        "VarScan_low_results.vcf"
    shell:
        "VarScan mpileup2snp {input} --min-var-freq  0.001 --output-vcf 1 > {output}"
