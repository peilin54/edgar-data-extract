#!/usr/bin/env python



# Example: (create the ./scratch directory or replace with your output directory)
#
# python main.py  -i ./tests/test_1 -o ./scratch
#  


import argparse
from edgar import run_form4


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SEC Edgar Form 4 reader')
    parser.add_argument('-i','--input_path', type=str, help='Enter directory of input files', required=True)
    parser.add_argument('-o','--output_path', type=str, help='Enter output directory ', required=True)
    parser.add_argument('-l','--list_order', type=bool, default=False, help='Read the .txt files in the order specified by a file list_txt. For testing purpose. Default is False', required=False)
    args = parser.parse_args()
    
    
    run_form4(args.input_path, args.output_path, args.list_order)
    
    
