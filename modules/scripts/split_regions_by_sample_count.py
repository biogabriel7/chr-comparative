import os
import pandas as pd
from collections import defaultdict
import sys

def split_regions_by_sample_count(input_file, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read the file into a DataFrame
    df = pd.read_csv(input_file, sep='\t', header=None, names=['region', 'samples', 'count', 'score'])

    # Create a dictionary to hold data for each count level
    data_by_count = defaultdict(list)

    # Populate the dictionary with regions grouped by their sample count
    for _, row in df.iterrows():
        data_by_count[row['count']].append(row)

    # Determine the maximum count of samples that any region has
    max_count = int(df['count'].max())  # Convert max count to integer

    # Output files for each level from 1 up to max_count
    for count in range(1, max_count + 1):
        output_filename = f'regions_present_in_{count}_samples_or_more.bed'
        output_path = os.path.join(output_dir, output_filename)

        # Filter regions that meet or exceed the current count threshold
        with open(output_path, 'w') as f:
            # Optionally, you can remove the next line if comments are not desired
            # f.write("#region\tsamples\tcount\n") # Comment line (remove if not needed)

            for c in range(count, max_count + 1):
                for row in data_by_count[c]:
                    region_parts = row['region'].split(':')  # Split 'chr1:629731-630156' into parts
                    chrom = region_parts[0]
                    start, end = region_parts[1].split('-')

                    # Writing BED format: chrom, start, end, optionally followed by sample details in comments
                    # f.write(f"{chrom}\t{start}\t{end}\n") # Uncomment next line to remove sample details
                    f.write(f"{chrom}\t{start}\t{end}\t{row['samples']}\t{row['score']}\n")  # Include sample details

    print(f"Files created for each sample count up to {max_count} in the '{output_dir}' directory.")

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_dir = sys.argv[2]  # This will be ignored, as output_dir is set to config["gold_standard_folder"]
    split_regions_by_sample_count(input_file, output_dir)
