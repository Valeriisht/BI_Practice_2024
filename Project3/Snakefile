URL = {
    'forward_PE': "https://d28rh4a8wq0iu5.cloudfront.net/bioinfo/SRR292678sub_S1_L001_R1_001.fastq.gz",
    'reverse_PE': "https://d28rh4a8wq0iu5.cloudfront.net/bioinfo/SRR292678sub_S1_L001_R2_001.fastq.gz",
    'forward_MP_2': "https://d28rh4a8wq0iu5.cloudfront.net/bioinfo/SRR292862_S2_L001_R1_001.fastq.gz",
    'reverse_MP_2': "https://d28rh4a8wq0iu5.cloudfront.net/bioinfo/SRR292862_S2_L001_R2_001.fastq.gz",
    'forward_MP_6': "https://d28rh4a8wq0iu5.cloudfront.net/bioinfo/SRR292770_S1_L001_R1_001.fastq.gz",
    'reverse_MP_6': "https://d28rh4a8wq0iu5.cloudfront.net/bioinfo/SRR292770_S1_L001_R2_001.fastq.gz"
}

rule all:
	input:
		expand('{sample}', sample = URL.keys()) #чтобы по словарю проходится

rule sample_download:
    output:
        sample = 'libraries/{sample}.fastq.gz'
    params:
        link = lambda x: URL[x.sample] #вытаскиваем конкретную ссылку
    shell:
        """
        wget -O {output.sample} {params.link}
        """

rule fastqc:
    input:
        "libraries/{sample}.fastq.gz"
    output:
        "qc/fastqc/{sample}_fastqc.html",
        "qc/fastqc/{sample}_fastqc.zip"
    shell:
        "fastqc -o qc/fastqc/ --noextract {input}" # не распаковываем архив

rule multiqc:
    input:
        "qc/fastqc/"
    output:
        "qc/multiqc/multiqc_report.html"
    shell:
        "multiqc {input} -o qc/multiqc/"

rule kkmer_count:
    input:
        forward ="libraries/forward_{sample_s}.fastq.gz",
        reverse ="libraries/reverse_{sample_s}.fastq.gz"
    output:
        "results/jellyfish/{sample_s}_31.jf"
    params:
        m='31', # длина к-меров
        s='10M' # размер для хранения данных > больше размера генома (5.2M)
    shell:
        """
        jellyfish count -m {params.m} -s {params.s} <(gzcat {input.forward}) <(gzcat {input.reverse}) -o {output}
        """

rule kkmer_histo:
    input:
        "results/jellyfish/{name}_31.jf"
    output:
        "results/jellyfish/{name}_histo.txt"
    shell:
        """
        jellyfish histo {input} > {output} 
        """
