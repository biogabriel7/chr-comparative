import pybedtools
import pandas as pd
import numpy as np
import os
import argparse

def read_bed_file(file_path):
    return pybedtools.BedTool(file_path)

def generate_candidate_regions(genome_size, num_candidates=800000, length_range=(200, 400)):
    regions = []
    for chrom, size in genome_size.items():
        for _ in range(num_candidates // len(genome_size)):
            start = np.random.randint(0, size - max(length_range))
            end = start + np.random.randint(*length_range)
            score = np.random.uniform(0, 1)
            regions.append((chrom, start, end, score))

            if len(regions) % 10000 == 0:
                print(f"Generated {len(regions)} candidate regions...")

    df = pd.DataFrame(regions, columns=['chr', 'start', 'end', 'score'])
    return pybedtools.BedTool.from_dataframe(df)

def process_bed_files(gold_standard, sample_bed, genome_size):
    true_positives = sample_bed.intersect(gold_standard, wa=True, u=True)
    false_positives = sample_bed.intersect(gold_standard, wa=True, v=True)
    false_negatives = gold_standard.intersect(sample_bed, wa=True, v=True)

    tp_df = true_positives.to_dataframe(names=['chr', 'start', 'end', 'peak', 'score'], dtype=str)
    fp_df = false_positives.to_dataframe(names=['chr', 'start', 'end', 'peak', 'score'], dtype=str)
    fn_df = false_negatives.to_dataframe(names=['chr', 'start', 'end', 'peak', 'score'], dtype=str)

    tp_df['score'] = tp_df['score'].astype(float)
    fp_df['score'] = fp_df['score'].astype(float)
    fn_df['score'] = np.random.uniform(0, 1, size=len(fn_df))

    tp_df['label'] = 1; tp_df['label_count'] = 'TP'
    fp_df['label'] = 0; fp_df['label_count'] = 'FP'
    fn_df['label'] = 1; fn_df['label_count'] = 'FN'

    candidate_regions = generate_candidate_regions(genome_size)
    existing_regions = pybedtools.BedTool.from_dataframe(pd.concat([tp_df, fp_df, fn_df]))
    true_negatives = candidate_regions.subtract(existing_regions, A=True).to_dataframe(names=['chr', 'start', 'end', 'score'])
    true_negatives['score'] = np.random.uniform(0, 1, size=len(true_negatives))
    true_negatives['label'] = 0; true_negatives['label_count'] = 'TN'

    final_df = pd.concat([tp_df, fp_df, fn_df, true_negatives])
    return final_df

def output_with_labels_and_scores(final_df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_df = final_df.sort_values(by=['chr', 'start', 'end'])
    final_df.to_csv(output_path, sep='\t', index=False, header=False)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process BED files and generate labeled and scored peaks.')
    parser.add_argument('--gold-standard', type=str, required=True, help='Path to the gold standard BED file.')
    parser.add_argument('--peaks', type=str, required=True, help='Path to the peaks BED file.')
    parser.add_argument('--output', type=str, required=True, help='Path to the output labeled and scored BED file.')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    genome_size = {
        'chr1': 248956422,
        'chr2': 242193529,
        'chr3': 198295559,
        'chr4': 190214555,
        'chr5': 181538259,
        'chr6': 170805979,
        'chr7': 159345973,
        'chr8': 145138636,
        'chr9': 138394717,
        'chr10': 133797422,
        'chr11': 135086622,
        'chr12': 133275309,
        'chr13': 114364328,
        'chr14': 107043718,
        'chr15': 101991189,
        'chr16': 90338345,
        'chr17': 83257441,
        'chr18': 80373285,
        'chr19': 58617616,
        'chr20': 64444167,
        'chr21': 46709983,
        'chr22': 50818468
    }

    gold_standard = read_bed_file(args.gold_standard)
    peaks = read_bed_file(args.peaks)

    final_df = process_bed_files(gold_standard, peaks, genome_size)
    output_with_labels_and_scores(final_df, args.output)
