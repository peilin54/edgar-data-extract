#!/usr/bin/env python
# coding: utf-8

import argparse
from edgar.edgar_form4 import run_form4


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SEC Edgar Form 4 reader')
    parser.add_argument('-inpath','--inpath', type=str, help='Enter directory of input files, MUST include trailing "/"', required=True)
    parser.add_argument('-outpath','--outpath', type=str, help='Enter output directory (optional), MUST include trailing "/". Default is same as input directory', required=False)
    parser.add_argument('-readlist','--readlist', type=bool, default=False, help='Read the .txt files in the order specified by a file list_txt. For testing purpose. Default is False', required=False)
    args = parser.parse_args()
    
    inpath = args.inpath
    if args.outpath:
        outpath = args.outpath
    else:
        outpath = inpath
    
    run_form4(inpath, outpath, args.readlist)
    
    