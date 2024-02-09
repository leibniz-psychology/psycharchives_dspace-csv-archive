#!/usr/bin/python3

import os, sys

from dspacearchive import DspaceArchive

if len(sys.argv) != 2:
	print("Usage: ./dspace-csv-archive [/path/to/input/file.csv]")
	sys.exit()

input_file = sys.argv[1]
input_base_path = os.path.dirname(input_file)
output_path = input_base_path + "_saf"

print("input_file = ", input_file)
print("input_base_path = ", input_base_path)
print("output_path = ", output_path)

archive = DspaceArchive(input_file)

archive.write(output_path)
archive.zip(output_path, output_path)
