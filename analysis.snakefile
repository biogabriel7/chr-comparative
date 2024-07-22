# Main Snakefile

configfile: "config.yaml"

# Define the desired order of Snakefiles
SNAKEFILES = [
    "modules/goldstandard.snakefile",
    "modules/input.snakefile",
    "modules/comparative.snakefile"
]

# Define the main rule
rule all:
    input:
        expand("{snakefile}_done", snakefile=SNAKEFILES)

# Rule to execute each Snakefile
rule run_snakefile:
    output:
        touch("{snakefile}_done")
    shell:
        """
        snakemake --snakefile {wildcards.snakefile} --cores {threads}
        """
