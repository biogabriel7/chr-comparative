import pandas as pd
from pybedtools import BedTool
import os
import glob
import re
import logging
import argparse

def custom_chr_sort(chrom):
    """Custom sort function for chromosomes, handling both numeric and 'chrX', 'chrY'."""
    if chrom.startswith("chr"):
        chrom = chrom[3:]
    return chrom.zfill(2) if chrom.isdigit() else chrom

def select_and_sort_peaks(input_bedfile, output_bedfile, top_n):
    df = pd.read_csv(input_bedfile, sep='\t', header=None)
    df = df[~df[0].isin(['chrX', 'chrY'])]
    df = df[df[0].str.match(r'chr\d+$')]

    if df.shape[1] < 5:
        raise ValueError(f"The file {input_bedfile} does not have the expected 5 columns (chromosome, start, end, name, score).")

    df_sorted = df.sort_values(by=4, ascending=False).head(top_n)
    df_sorted['chr_sorted'] = df_sorted[0].apply(custom_chr_sort)
    df_sorted['feature_size'] = df_sorted[2] - df_sorted[1]
    df_final_sorted = df_sorted.sort_values(by=['chr_sorted', 'feature_size'], ascending=[True, False])

    df_final_sorted = df_final_sorted.drop(columns=['chr_sorted', 'feature_size'])
    df_final_sorted.to_csv(output_bedfile, sep='\t', index=False, header=False)
    logging.info(f'Processed and sorted {input_bedfile} saved to {output_bedfile}')

def process_all_bed_files_in_folder(input_folder, output_folder, top_n):
    os.makedirs(output_folder, exist_ok=True)
    bedfiles = glob.glob(os.path.join(input_folder, '*.bed'))

    for bedfile in bedfiles:
        try:
            output_bedfile = os.path.join(output_folder, os.path.basename(bedfile))
            select_and_sort_peaks(bedfile, output_bedfile, top_n)
        except Exception as e:
            logging.error(f"Error processing {bedfile}: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process and sort BED files.')
    parser.add_argument('input_folder', type=str, help='Input folder containing BED files.')
    parser.add_argument('output_folder', type=str, help='Output folder for sorted BED files.')
    parser.add_argument('top_n', type=int, help='Number of top peaks to select.')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    process_all_bed_files_in_folder(args.input_folder, args.output_folder, args.top_n)
