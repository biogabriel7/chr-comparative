import os
import pybedtools
import pandas as pd
import numpy as np
from multiprocessing import Pool, freeze_support
import argparse
import logging

def load_bed_files(sorted_samples_folder):
    sample_beds = {}
    for sample_file in os.listdir(sorted_samples_folder):
        if sample_file.endswith('.bed'):
            sample_name = os.path.splitext(sample_file)[0]
            sample_beds[sample_name] = pybedtools.BedTool(os.path.join(sorted_samples_folder, sample_file))
    return sample_beds

def process_region(args):
    region, sample_beds = args
    region_str = f"{region.chrom}:{region.start}-{region.end}"
    region_data = {'region': region_str, 'samples': [], 'scores': []}
    for sample_name, sample_bed in sample_beds.items():
        intersections = sample_bed.intersect(pybedtools.BedTool(str(region), from_string=True), wa=True, wb=True)
        scores = [float(intersect[4]) for intersect in intersections]
        if scores:
            region_data['samples'].append(sample_name)
            region_data['scores'].extend(scores)
    return region_data

def find_samples_with_regions(merged_bedfile, sorted_samples_folder, output_file):
    merged_bed = pybedtools.BedTool(merged_bedfile)
    logging.info(f"Processing {len(merged_bed)} regions in merged BED file.")
    sample_beds = load_bed_files(sorted_samples_folder)
    with Pool(processes=12) as pool:
        results = pool.map(process_region, [(region, sample_beds) for region in merged_bed])
    df = pd.DataFrame({
        'Region': [result['region'] for result in results],
        'Samples': [','.join(result['samples']) for result in results],
        'Count': [len(result['samples']) for result in results],
        'Mean Score': [np.mean(result['scores']) if result['scores'] else 0 for result in results]
    })
    df.to_csv(output_file, sep='\t', header=None, index=False)
    logging.info(f"Output file {output_file} has been successfully created.")

if __name__ == '__main__':
    freeze_support()  # for Windows compatibility

    parser = argparse.ArgumentParser(description='Find samples with regions in a merged BED file.')
    parser.add_argument('merged_bedfile', type=str, help='Path to the merged BED file.')
    parser.add_argument('sorted_samples_folder', type=str, help='Path to the directory containing sorted sample BED files.')
    parser.add_argument('output_file', type=str, help='Output file to save the results.')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    find_samples_with_regions(args.merged_bedfile, args.sorted_samples_folder, args.output_file)
