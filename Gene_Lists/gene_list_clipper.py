#!/usr/bin/env python3
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Clip and save a column from a file.")
parser.add_argument("input_file", type=str, help="Path to the input file")
parser.add_argument("output_file", type=str, help="Path to the output file")
parser.add_argument("--rows", type=int, default=7, help="Number of rows to include (default: 7)")
args = parser.parse_args()

df = pd.read_csv(args.input_file, delimiter='\t')
df.columns = df.columns.str.strip()
print("Columns in the file:", df.columns)
df['GeneID'].head(args.rows).to_csv(args.output_file, index=False, header=False)
print(f"File successfully written to {args.output_file}")