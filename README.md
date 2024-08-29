# ChIP-seq / Chromatin Profilling Techniques Data Analysis Workflow

This repository contains a Snakemake-based workflow for analyzing ChIP-seq data. The workflow processes bed files, generates a gold standard, and performs comparative analysis between the gold standard and a desired sample.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Workflow Overview](#workflow-overview)
5. [Configuration](#configuration)
6. [Output](#output)
7. [Scripts](#scripts)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction

The developed workflow provide an automated and reproducible approach for the comparative analysis of ChIP-Seq samples. The modular design of the pipeline enables eficient data processing, gold standard generation, and comparative analysis tasks, facilitating the identification of significant regions and the evaluation of analysis performance. The precision-recall curves and F1 scores show how well the peak calling works and what the best threshold is for determining peak presence. It can be used to analyze various types of high-throughput sequencing data beyond ChIP-Seq. This workflows helps understand how TFs and HMs affect different conditions or cell types. This helps them make important discoveries in epigenetics and gene regulation.

## Installation

To use this workflow, you need to have Snakemake installed. You can install Snakemake and other dependencies using conda:

```bash
conda create -n chipseq-workflow python=3.10
conda activate chipseq-workflow
conda install -c bioconda snakemake
pip install pandas numpy matplotlib seaborn pybedtools scikit-learn
```

## Usage

To run the workflow:

```bash
snakemake analysis.snakefile --cores all
```

## Workflow Overview

The workflow consists of three main modules:

- Gold Standard Generation: Processes input bed files and generates gold standard regions.
- Input Processing: Sorts and processes input a bed file for comparative analysis.
- Comparative Analysis: Compares processed input files against gold standards.

## Configuration

Edit the config.yaml file to set parameters for your analysis:

note: I do not recommend editing any path since it would require additional modifications to other files!

- samples_folder: "path/to/input/samples"
- gold_standard_folder: "path/to/gold/standard/output"
- comparison_input_folder: "path/to/comparison/input"
- comparison_output_folder: "path/to/comparison/output"
- plot_folder: "path/to/plot/output"
- top_n: 20000 (Number of peaks to consider from each sample to establish the gold standard)
- top_n_comparison: 100000
- max_sample_count: 10 (Number of samples used to create the gold standard)

## Output

Processed and sorted bed files
Gold standard
Comparative analysis results
Various plots (heatmaps, histograms, precision-recall curves)

## Scripts

- process_bed_files.py: Processes and sorts bed files
- merge_bed_files.py: Merges bed files
- find_regions_sample.py: Finds regions present in samples
- split_regions_by_sample_count.py: Splits regions by sample count
- generate_heatmap.py: Generates heatmaps
- sort_input_comparative.py: Sorts input files for comparative analysis
- precision_recall.py: Calculates precision and recall
- plot_histogram.py: Plots histograms
- calculate_precision_recall.py: Calculates and plots precision-recall curves

## Contributing

Contributions to improve the workflow are welcome. Please submit a pull request or open an issue to discuss proposed changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
