import os
import pandas as pd
import glob
import logging
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

def custom_chr_sort(chrom):
    """Custom sort function for chromosomes, handling both numeric and 'chrX', 'chrY'."""
    if chrom.startswith("chr"):
        chrom = chrom[3:]
    return chrom.zfill(2) if chrom.isdigit() else chrom

def select_and_sort_peaks(input_bedfile, output_bedfile, plot_folder, c_top_n):
    # Read the BED file into a pandas DataFrame
    df = pd.read_csv(input_bedfile, sep='\t', header=None)

    # Filter out rows from chromosomes X and Y
    df = df[~df[0].isin(['chrX', 'chrY'])]

    # Filter out rows where the chromosome name does not match the pattern "chr" followed by one or more digits
    df = df[df[0].str.match(r'chr\d+$')]

    # Ensure the DataFrame has at least 5 columns
    if df.shape[1] < 5:
        raise ValueError(f"The file {input_bedfile} does not have the expected 5 columns (chromosome, start, end, name, score).")

    # Sort the DataFrame by the 5th column (score) in descending order and select the top N
    df_sorted = df.sort_values(by=4, ascending=False).head(c_top_n)

    # Additional sorting: first by chromosome, then by feature size (end - start) in descending order
    df_sorted['chr_sorted'] = df_sorted[0].apply(custom_chr_sort)  # Apply custom chromosome sort
    df_sorted['feature_size'] = df_sorted[2] - df_sorted[1]  # Calculate feature size
    df_final_sorted = df_sorted.sort_values(by=['chr_sorted', 'feature_size'], ascending=[True, False])

    # Drop the auxiliary columns used for sorting
    df_final_sorted = df_final_sorted.drop(columns=['chr_sorted', 'feature_size'])

    # Save the sorted DataFrame to a new BED file
    df_final_sorted.to_csv(output_bedfile, sep='\t', index=False, header=False)
    logging.info(f'Processed and sorted {input_bedfile} saved to {output_bedfile}')

    # Filter scores between 1 and 10000
    valid_scores = df_final_sorted[4][(df_final_sorted[4] >= 1) & (df_final_sorted[4] <= 10000)]

    # Plot histogram with adjusted bin edges
    plt.figure(figsize=(10, 6))
    sns.histplot(valid_scores, bins=50, kde=True, edgecolor='black')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.title(f'Score Distribution for {os.path.basename(input_bedfile)}')
    plt.yscale('log')  # Use a logarithmic scale for the y-axis
    plt.grid(True, axis='y')  # Add horizontal grid lines

    # Save the plot as a PNG file in the plot folder
    plot_filename = f"{os.path.splitext(os.path.basename(input_bedfile))[0]}_score_distribution.png"
    plot_path = os.path.join(plot_folder, plot_filename)
    plt.savefig(plot_path)
    plt.close()

    # Plot a separate histogram for high score values
    high_scores = valid_scores[valid_scores > valid_scores.quantile(0.95)]
    if not high_scores.empty:
        plt.figure(figsize=(10, 6))
        sns.histplot(high_scores, bins=20, kde=True, edgecolor='black')
        plt.xlabel('Score')
        plt.ylabel('Frequency')
        plt.title(f'Distribution of High Scores for {os.path.basename(input_bedfile)}')
        plt.yscale('log')  # Use a logarithmic scale for the y-axis
        plt.grid(True, axis='y')  # Add horizontal grid lines

        # Save the high score plot as a PNG file in the plot folder
        high_score_plot_filename = f"{os.path.splitext(os.path.basename(input_bedfile))[0]}_high_score_distribution.png"
        high_score_plot_path = os.path.join(plot_folder, high_score_plot_filename)
        plt.savefig(high_score_plot_path)
        plt.close()

def process_all_bed_files_in_folder(input_folder, output_folder, plot_folder, top_n):
    # Ensure the output folder and plot folder exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(plot_folder, exist_ok=True)

    # Get a list of all the .bed files in the folder
    bedfiles = glob.glob(os.path.join(input_folder, '*.bed'))

    # Process and sort each bed file
    for bedfile in bedfiles:
        try:
            # Construct the output file path
            output_bedfile = os.path.join(output_folder, os.path.basename(bedfile))

            # Select the top N peaks based on score, then sort by chromosome and feature size
            select_and_sort_peaks(bedfile, output_bedfile, plot_folder, top_n)
        except Exception as e:
            logging.error(f"Error processing {bedfile}: {str(e)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process and plot BED files for comparison.')
    parser.add_argument('input_folder', type=str, help='Input folder containing BED files for comparison.')
    parser.add_argument('output_folder', type=str, help='Output folder for processed BED files.')
    parser.add_argument('plot_folder', type=str, help='Output folder for score distribution plots.')
    parser.add_argument('top_n', type=int, help='Number of top peaks to select.')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    process_all_bed_files_in_folder(args.input_folder, args.output_folder, args.plot_folder, args.top_n)
