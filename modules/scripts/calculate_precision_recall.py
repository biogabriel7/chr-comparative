import pandas as pd
import numpy as np
from sklearn.metrics import precision_recall_curve, f1_score
import matplotlib.pyplot as plt
import os
import argparse

def calculate_f1_score(df):
    y_true = df['label'].values
    y_score = df['score'].values

    # Find the optimal threshold for all scores
    precision, recall, thresholds = precision_recall_curve(y_true, y_score)
    f1_scores = 2 * precision * recall / (precision + recall + 1e-7)  # Add a small value to avoid division by zero
    optimal_threshold_index = np.argmax(f1_scores)
    optimal_threshold = thresholds[optimal_threshold_index]

    # Convert scores to binary predictions using the optimal threshold
    y_pred = y_score > optimal_threshold

    f1 = f1_score(y_true, y_pred)
    return f1, optimal_threshold, precision[optimal_threshold_index], recall[optimal_threshold_index]

def plot_precision_recall_curve(df, f1_score, optimal_threshold, optimal_precision, optimal_recall, output_path):
    if df['label'].nunique() < 2:
        raise ValueError("The 'label' column must contain both 0s and 1s.")

    if df['score'].isnull().any() or df['label'].isnull().any():
        raise ValueError("NaNs detected in 'score' or 'label' column.")

    precision, recall, _ = precision_recall_curve(df['label'], df['score'])
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, linewidth=2)
    plt.scatter(optimal_recall, optimal_precision, color='red', label=f'Optimal (Precision: {optimal_precision:.2f}, Recall: {optimal_recall:.2f})')
    plt.xlabel('Recall', fontsize=14)
    plt.ylabel('Precision', fontsize=14)
    plt.title('Precision-Recall Curve', fontsize=16)
    plt.text(0.7, 0.9, f'F1 Score: {f1_score:.2f}', fontsize=12, transform=plt.gca().transAxes)
    plt.text(0.7, 0.85, f'Optimal Threshold: {optimal_threshold:.2f}', fontsize=12, transform=plt.gca().transAxes)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True)
    plt.legend(fontsize=12, loc='lower left')
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculate precision-recall from labeled and scored BED file.')
    parser.add_argument('--input', type=str, required=True, help='Path to the labeled and scored BED file.')
    parser.add_argument('--output', type=str, required=True, help='Path to the output precision-recall plot.')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    final_df = pd.read_csv(args.input, sep='\t', names=['chr', 'start', 'end', 'peak', 'score', 'label', 'label_count'])
    f1, optimal_threshold, optimal_precision, optimal_recall = calculate_f1_score(final_df)
    plot_precision_recall_curve(final_df, f1, optimal_threshold, optimal_precision, optimal_recall, args.output)
