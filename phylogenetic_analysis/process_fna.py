#!/usr/bin/env python3

import re
import argparse

# Compile regex to match organism name, GeneID, and symbol
organism_regex = re.compile(r"\[organism=(.+?)\]")  # Match organism name
gene_id_regex = re.compile(r"\[GeneID=(\d+)\]")  # Match GeneID
symbol_regex = re.compile(r"(\S+)\s\[")  # Match symbol (assumed to be before "[organism=")

# Function to process the file
def process_fna(input_file, output_file):
    seen_genera = set()  # Keep track of seen genera
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        write_sequence = False
        for line in infile:
            if line.startswith(">"):  # Header line
                # Extract organism name, GeneID, and symbol
                organism_match = organism_regex.search(line)
                gene_id_match = gene_id_regex.search(line)
                symbol_match = symbol_regex.search(line)
                
                if organism_match and gene_id_match and symbol_match:
                    organism = organism_match.group(1)
                    genus = organism.split(" ")[0]  # Extract the genus name (first part)
                    gene_id = gene_id_match.group(1)
                    symbol = symbol_match.group(1)
                    
                    # Check if the genus has already been seen
                    if genus not in seen_genera:
                        seen_genera.add(genus)
                        write_sequence = True
                        # Write the header in the desired order
                        formatted_organism = organism.replace(" ", "_")  # Replace spaces with underscores
                        outfile.write(f">{formatted_organism} {gene_id} {symbol}\n")
                    else:
                        write_sequence = False
                else:
                    write_sequence = False
            else:
                # Write sequence lines if the header was valid and unique
                if write_sequence:
                    outfile.write(line)

# Main function to parse arguments and run the script
def main():
    parser = argparse.ArgumentParser(
        description="Process an FNA file to keep only the first unique genus name and format headers."
    )
    parser.add_argument("input", help="Input .fna file path")
    parser.add_argument("output", help="Output .fna file path")
    args = parser.parse_args()

    # Call the processing function
    process_fna(args.input, args.output)
    print(f"Processed file saved to: {args.output}")

if __name__ == "__main__":
    main()