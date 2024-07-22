import os
import glob
import yaml

configfile: "config.yaml"

def get_chipseq_names():
    chipseq_sample_names = []
    for f in glob.glob(os.path.join(config["samples_folder"], '*.bed')):
        chipseq_sample_name = os.path.basename(f).split(".")[0]
        chipseq_sample_names.append(chipseq_sample_name)  # Fix variable name
    print(f"ChipSeq Sample Names: {chipseq_sample_names}")
    return chipseq_sample_names  # Fix return value

chipseq_names = get_chipseq_names()

rule all:
    input:
        "analysis/final_file_{top_n}.bed".format(top_n=config["top_n"]),
        expand(config["gold_standard_folder"] + "/regions_present_in_{count}_samples_or_more.bed", count=range(1, config["max_sample_count"])),
        "analysis/heatmap/heatmap_{top_n}.png".format(top_n=config["top_n"])


rule process_bed_files:
    input:
        folder=config["samples_folder"]
    output:
        directory(config["sorted_samples_folder"])
    params:
        top_n=config["top_n"]
    shell:
        "python modules/scripts/process_bed_files.py {input.folder} {output} {params.top_n}"

rule merge_bed_files:
    input:
        folder=config["sorted_samples_folder"]
    output:
        directory(config["merged_samples_folder"])
    shell:
        "python modules/scripts/merge_bed_files.py process {input.folder} {output}"

rule merge_all_bed_files:
    input:
        folder=config["merged_samples_folder"]
    output:
        intermediate=config["intermediate_output_file"],
        final=config["final_output_file"]
    shell:
        """
        mkdir -p $(dirname {output.intermediate}) $(dirname {output.final})
        python modules/scripts/merge_bed_files.py merge_all {input.folder} {output.intermediate}
        python modules/scripts/merge_bed_files.py merge_regions {output.intermediate} {output.final}
        """

rule find_samples_with_regions:
    input:
        merged_bedfile=config["final_output_file"],
        sorted_samples_folder=rules.process_bed_files.output
    output:
        "analysis/final_file_{top_n}.bed".format(top_n=config["top_n"])
    shell:
        "python modules/scripts/find_regions_sample.py {input.merged_bedfile} {input.sorted_samples_folder} {output}"

rule split_regions_by_sample_count:
    input:
        rules.find_samples_with_regions.output
    output:
        expand(config["gold_standard_folder"] + "/regions_present_in_{count}_samples_or_more.bed", count=range(1, config["max_sample_count"]))
    params:
        output_folder=config["gold_standard_folder"],
        max_sample_count=config["max_sample_count"]
    shell:
        "python modules/scripts/split_regions_by_sample_count.py {input} {params.output_folder} {params.max_sample_count}"

rule generate_heatmap:
    input:
        rules.split_regions_by_sample_count.output[0]  # Use the first output file from split_regions_by_sample_count
    output:
        "analysis/heatmap/heatmap_{top_n}.png".format(top_n=config["top_n"])
    shell:
        "python modules/scripts/generate_heatmap.py {input} {output}"
