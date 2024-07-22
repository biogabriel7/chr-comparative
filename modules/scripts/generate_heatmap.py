import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import logging

def generate_heatmap(input_file, output_file):
    # Load the dataset
    df = pd.read_csv(input_file, sep='\t', header=None)

    # Assuming the samples are in the 4th column and separated by commas
    # Create a binary matrix for sample presence
    all_samples = sorted(set(','.join(df[3]).split(',')))
    matrix = pd.DataFrame(0, index=df.index, columns=all_samples)

    # Fill the matrix with presence data
    for i, row in df.iterrows():
        samples = row[3].split(',')
        matrix.loc[i, samples] = 1

    # Create the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(matrix.T, cmap='viridis', cbar_kws={'label': 'Presence/Absence'})
    plt.title('Heatmap of Sample Presence in Regions')
    plt.xlabel('Region Index')
    plt.ylabel('Samples')

    # Save the heatmap
    plt.savefig(output_file)
    plt.close()
    logging.info(f"Heatmap saved to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate heatmap for sample presence in regions.')
    parser.add_argument('input_file', type=str, help='Path to the input file.')
    parser.add_argument('output_file', type=str, help='Path to save the output heatmap.')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    generate_heatmap(args.input_file, args.output_file)
