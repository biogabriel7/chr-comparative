import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse
import numpy as np

def plot_enhanced_histogram(final_df, output_path):
    label_counts = final_df['label_count'].value_counts().sort_index()
    label_counts = label_counts[label_counts.index != 'TN']

    # Debugging statements
    print("Label Counts:")
    print(label_counts)
    print("Final DataFrame:")
    print(final_df.head())
    print("Output Path:", output_path)

    if label_counts.empty:
        print("No data to plot.")
        return

    plt.figure(figsize=(10, 8))
    bar_positions = np.arange(len(label_counts))
    bar_width = 0.6
    colors = plt.cm.viridis(np.linspace(0, 1, len(label_counts)))

    for i, label in enumerate(label_counts.index):
        if label == 'TP':
            label_text = 'True Positives (TP)'
        elif label == 'FN':
            label_text = 'False Negatives (FN)'
        elif label == 'FP':
            label_text = 'False Positives (FP)'
        else:
            label_text = label

        plt.bar(bar_positions[i], label_counts[label], width=bar_width, color=colors[i], label=label_text)

    plt.xlabel('Labels', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.title('Distribution of TP, FP, and FN', fontsize=16)
    plt.xticks(bar_positions, label_counts.index, fontsize=12)
    plt.yticks(fontsize=12)

    for i, count in enumerate(label_counts):
        plt.text(bar_positions[i], count + 0.005 * max(label_counts), str(count), ha='center', fontsize=12)

    plt.legend(fontsize=12)
    plt.tight_layout()

    # Check if the directory exists
    dir_name = os.path.dirname(output_path)
    if not os.path.exists(dir_name):
        print(f"Creating directory: {dir_name}")
        os.makedirs(dir_name, exist_ok=True)

    # Save the figures
    print(f"Saving PNG to {output_path}")
    plt.savefig(output_path, dpi=300)  # Save as PNG

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate histogram from labeled and scored BED file.')
    parser.add_argument('--input', type=str, required=True, help='Path to the labeled and scored BED file.')
    parser.add_argument('--output', type=str, required=True, help='Path to the output histogram plot.')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    final_df = pd.read_csv(args.input, sep='\t', names=['chr', 'start', 'end', 'peak', 'score', 'label', 'label_count'])

    # Debugging statement
    print("Loaded DataFrame:")
    print(final_df.head())

    plot_enhanced_histogram(final_df, args.output)
