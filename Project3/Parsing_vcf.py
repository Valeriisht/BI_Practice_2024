import io
import pandas as pd


def read_vcf(file_path):
    with open(file_path, "r") as f:
        # Читаем строки, которые не начинаются с '##'
        lines = [line for line in f if not line.startswith("##")]
    # DataFrame
    return pd.read_csv(io.StringIO(''.join(lines)), sep='\t', comment='#', header=0)
