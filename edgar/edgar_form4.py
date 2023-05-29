#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import argparse
import os
import sys
import flatdict
from proc_form4 import proc_form4txt, form4xml_toflatdict, flatdict_toDF, form4df_tocsv, concat_abtoC, save_dftocsv


def form4_tocsv(inpath, outpath, filename):
    """
    This is the main function that reads form 4 file and process it and save it to .csv database
    
    inpath:   string, directory for input files
    outpath:  string, directory for output files
    filename: string, full filename of Form-4.txt after pre-processing
    """
    
    # pre-processing .txt file, so that xml can be formatted properly with flatdict
    proc_form4txt(inpath, filename)
    
    # extract xml information to flatdict object
    full_dict = form4xml_toflatdict(inpath, filename+'.mod')

    # create subsections from the full dictionary
    # issuer and reportingOwner first; hopefully these fields are populated
    issuer_df = flatdict_toDF(full_dict["issuer"])
          
    if isinstance(full_dict["reportingOwner"], list):
        for item in full_dict["reportingOwner"]:
            tmp = flatdict.FlatDict(item, delimiter='.')
            reportingOwner_df = flatdict_toDF(tmp)
            form4df_tocsv(outpath, full_dict, issuer_df, reportingOwner_df)
        
        # # DEBUG only: use only one reporting Owner for multiple owner cases
        # item=full_dict["reportingOwner"][0]
        # tmp = flatdict.FlatDict(item, delimiter='.')
        # reportingOwner_df = flatdict_toDF(tmp)
        # form4df_tocsv(outpath, full_dict, issuer_df, reportingOwner_df)
        # # DEBUG only

    else:
        reportingOwner_df = flatdict_toDF(full_dict["reportingOwner"])
        form4df_tocsv(outpath, full_dict, issuer_df, reportingOwner_df)
        
    return


def main():

    parser = argparse.ArgumentParser(description='SEC Edgar Form 4 reader')
    parser.add_argument('-inpath','--inpath', type=str, help='Enter directory of input files, MUST include trailing "/"', required=True)
    parser.add_argument('-outpath','--outpath', type=str, help='Enter output directory (optional), MUST include trailing "/". Default is same as input directory', required=False)
    parser.add_argument('-readlist','--readlist', type=bool, default=False, help='Read file from a list. For testing purpose. Default is False', required=False)
    args = parser.parse_args()

    inpath = args.inpath
    if args.outpath:
        outpath = args.outpath
    else:
        outpath = inpath
    
    if not args.readlist:

        directory = os.fsencode(inpath)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".txt"): 
                print(filename)
                form4_tocsv(inpath, outpath, filename)
    else:
        infile  = open(inpath+"list_txt", 'r')
        lines   = infile.readlines()

        for line in lines:
            filename = line.strip()
            print(filename)
            form4_tocsv(inpath, outpath, filename)

        infile.close()


    # nd = pd.read_csv(outpath+"./nonDerivative.csv")
    # d  = pd.read_csv(outpath+""./derivative.csv")
    # f  = pd.read_csv(outpath+"./footnotes.csv")
    # display(nd)
    # display(d)
    # display(f)


if __name__ == "__main__":
    main()

