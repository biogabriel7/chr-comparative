import os
import glob

configfile: "config.yaml"

def get_sample_names():
    sample_names = []
    for f in glob.glob(os.path.join(config["comparison_input_folder"], '*.bed')):
        sample_name = os.path.basename(f).split(".")[0]
        sample_names.append(sample_name)
    print(f"Sample Names: {sample_names}")
    return sample_names

sample_names = get_sample_names()

rule all:
    input:
        expand("{output_folder}/{sample}.bed", output_folder=config["comparison_output_folder"], sample=sample_names),
        expand("{plot_folder}/{sample}_score_distribution.png", plot_folder=config["plot_folder"], sample=sample_names),
        expand("{plot_folder}/{sample}_high_score_distribution.png", plot_folder=config["plot_folder"], sample=sample_names)

rule sort_input_comparative:
    input:
        folder=config["comparison_input_folder"]
    output:
        bed=expand("{output_folder}/{sample}.bed", output_folder=config["comparison_output_folder"], sample=sample_names),
        score_plot=expand("{plot_folder}/{sample}_score_distribution.png", plot_folder=config["plot_folder"], sample=sample_names),
        high_score_plot=expand("{plot_folder}/{sample}_high_score_distribution.png", plot_folder=config["plot_folder"], sample=sample_names)
    params:
        top_n=config["top_n_comparison"],
        output_folder=config["comparison_output_folder"],
        plot_folder=config["plot_folder"]
    shell:
        """
        python modules/scripts/sort_input_comparative.py {input.folder} {params.output_folder} {params.plot_folder} {params.top_n}
        """
