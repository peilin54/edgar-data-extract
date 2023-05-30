#!/usr/bin/env python



# Example: (create the ./scratch directory or replace with your output directory)
#
# python main.py  -inpath ./tests/test_1 -outpath ./scratch
#  


import argparse
from edgar.edgar_form4 import run_form4


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SEC Edgar Form 4 reader')
    parser.add_argument('-inpath','--inpath', type=str, help='Enter directory of input files', required=True)
    parser.add_argument('-outpath','--outpath', type=str, help='Enter output directory ', required=True)
    parser.add_argument('-readlist','--readlist', type=bool, default=False, help='Read the .txt files in the order specified by a file list_txt. For testing purpose. Default is False', required=False)
    args = parser.parse_args()
    
    
    run_form4(args.inpath, args.outpath, args.readlist)
    
    
