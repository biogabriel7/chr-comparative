import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc, roc_auc_score
import matplotlib.pyplot as plt
import os
import argparse

def calculate_roc_auc_score(df):
    y_true = df['label'].values
    y_score = df['score'].values

    roc_auc = roc_auc_score(y_true, y_score)
    return roc_auc

def plot_roc_curve(df, roc_auc_score, output_path):
    if df['label'].nunique() < 2:
        raise ValueError("The 'label' column must contain both 0s and 1s.")

    if df['score'].isnull().any() or df['label'].isnull().any():
        raise ValueError("NaNs detected in 'score' or 'label' column.")

    fpr, tpr, _ = roc_curve(df['label'], df['score'])
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, linewidth=2)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate', fontsize=14)
    plt.ylabel('True Positive Rate', fontsize=14)
    plt.title('ROC Curve', fontsize=16)
    plt.text(0.7, 0.1, f'ROC AUC Score: {roc_auc_score:.2f}', fontsize=12, transform=plt.gca().transAxes)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True)
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculate ROC AUC from labeled and scored BED file.')
    parser.add_argument('--input', type=str, required=True, help='Path to the labeled and scored BED file.')
    parser.add_argument('--output', type=str, required=True, help='Path to the output ROC curve plot.')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    final_df = pd.read_csv(args.input, sep='\t', names=['chr', 'start', 'end', 'score', 'label', 'label-count'])
    roc_auc = calculate_roc_auc_score(final_df)
    plot_roc_curve(final_df, roc_auc, args.output)
