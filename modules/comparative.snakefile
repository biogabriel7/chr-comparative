import os
import glob

configfile: "config.yaml"

# Define functions to extract sample names and gold standard files
def get_sample_names():
    sample_names = []
    for f in glob.glob(os.path.join(config["comparison_output_folder"], '*.bed')):
        sample_name = os.path.basename(f).split(".")[0]
        sample_names.append(sample_name)
    print(f"Sample Names: {sample_names}")
    return sample_names

def get_gold_standard_names():
    gold_standard_names = []
    for f in glob.glob(os.path.join(config["gold_standard_folder"], 'regions_present_in_*_samples_or_more.bed')):
        N = os.path.basename(f).split("_")[3]
        gold_standard_names.append(N)
    print(f"Gold Standard Names: {gold_standard_names}")
    return gold_standard_names

# Rule to expand all combinations of samples and gold standards
rule all:
    input:
        expand(os.path.join(config["output_folder"], "peaks_with_labels_and_scores_{sample_name}_regions_present_in_{gold_standard}_samples_or_more.bed"),
              sample_name=get_sample_names(), gold_standard=get_gold_standard_names()),
        expand(os.path.join(config["histogram_folder"], "{sample_name}_regions_present_in_{gold_standard}_samples_or_more_histogram.png"),
              sample_name=get_sample_names(), gold_standard=get_gold_standard_names()),
        expand(os.path.join(config["precision_recall_folder"], "{sample_name}_regions_present_in_{gold_standard}_samples_or_more_precision_recall.png"),
              sample_name=get_sample_names(), gold_standard=get_gold_standard_names())

# Define the rule to process BED files
rule process_bed_files:
    input:
        gold_standard = lambda wildcards: os.path.join(config["gold_standard_folder"], f"regions_present_in_{wildcards.gold_standard}_samples_or_more.bed"),
        peaks = lambda wildcards: os.path.join(config["comparison_output_folder"], f"{wildcards.sample_name}.bed")
    output:
        bed = os.path.join(config["output_folder"], "peaks_with_labels_and_scores_{sample_name}_regions_present_in_{gold_standard}_samples_or_more.bed")
    shell:
        """
        python modules/scripts/precision_recall.py \
            --gold-standard {input.gold_standard} \
            --peaks {input.peaks} \
            --output {output.bed}
        """

rule generate_histogram:
    input:
        bed = lambda wildcards: os.path.join(config["output_folder"], f"peaks_with_labels_and_scores_{wildcards.sample_name}_regions_present_in_{wildcards.gold_standard}_samples_or_more.bed")
    output:
        histogram = os.path.join(config["histogram_folder"], "{sample_name}_regions_present_in_{gold_standard}_samples_or_more_histogram.png")
    shell:
        """
        python modules/scripts/plot_histogram.py \
            --input {input.bed} \
            --output {output.histogram}
        """

rule calculate_precision_recall:
    input:
        bed = lambda wildcards: os.path.join(config["output_folder"], f"peaks_with_labels_and_scores_{wildcards.sample_name}_regions_present_in_{wildcards.gold_standard}_samples_or_more.bed")
    output:
        precision_recall = os.path.join(config["precision_recall_folder"], "{sample_name}_regions_present_in_{gold_standard}_samples_or_more_precision_recall.png")
    shell:
        """
        python modules/scripts/calculate_precision_recall.py \
            --input {input.bed} \
            --output {output.precision_recall}
        """
