import os
import glob
from pybedtools import BedTool
import pandas as pd
import logging
import sys

def merge_all_bed_files_to_one(input_folder, intermediate_output_file):
    """
    Concatenates all BED files in the input folder into a single intermediate output file.
    """
    bed_files = glob.glob(os.path.join(input_folder, '*.bed'))

    with open(intermediate_output_file, 'w') as outfile:
        for file in bed_files:
            with open(file, 'r') as infile:
                outfile.write(infile.read())
    logging.info(f"All BED files merged into {intermediate_output_file}")

def merge_regions_in_bed_file(intermediate_output_file, final_output_file):
    """
    Sorts and then merges overlapping and directly adjacent intervals in the BED file.
    """
    bed = BedTool(intermediate_output_file).sort()
    merged_bed = bed.merge()
    merged_bed.saveas(final_output_file)
    logging.info(f'Merged regions saved to {final_output_file}')

def merge_bed_file(input_bedfile, output_bedfile):
    """
    Sorts and then merges overlapping intervals in the BED file.
    """
    bed = BedTool(input_bedfile).sort().merge()
    bed.saveas(output_bedfile)
    logging.info(f'Merged and sorted intervals from {input_bedfile} saved to {output_bedfile}')

def process_all_bed_files_in_folder(input_folder, output_folder):
    """
    Processes all BED files in the input folder by sorting, merging intervals,
    and saves each processed BED file in the output folder.
    """
    os.makedirs(output_folder, exist_ok=True)
    bedfiles = glob.glob(os.path.join(input_folder, '*.bed'))

    for bedfile in bedfiles:
        output_bedfile = os.path.join(output_folder, os.path.basename(bedfile))
        merge_bed_file(bedfile, output_bedfile)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    if len(sys.argv) < 2:
        print("Usage: python merge_bed_files.py <command> [<args>]")
        print("Commands:")
        print("  process <input_folder> <output_folder>")
        print("  merge_all <input_folder> <intermediate_output_file>")
        print("  merge_regions <intermediate_output_file> <final_output_file>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "process":
        input_folder = sys.argv[2]
        output_folder = sys.argv[3]
        process_all_bed_files_in_folder(input_folder, output_folder)
    elif command == "merge_all":
        input_folder = sys.argv[2]
        intermediate_output_file = sys.argv[3]
        os.makedirs(os.path.dirname(intermediate_output_file), exist_ok=True)
        merge_all_bed_files_to_one(input_folder, intermediate_output_file)
    elif command == "merge_regions":
        intermediate_output_file = sys.argv[2]
        final_output_file = sys.argv[3]
        os.makedirs(os.path.dirname(final_output_file), exist_ok=True)
        merge_regions_in_bed_file(intermediate_output_file, final_output_file)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
