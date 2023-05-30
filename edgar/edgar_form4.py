#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import argparse
import os
import sys
from pathlib import Path
import flatdict
from edgar.proc_form4 import proc_form4txt, form4xml_toflatdict, flatdict_toDF, form4df_tocsv, concat_abtoC, save_dftocsv


def form4_tocsv(inpath, outpath, filename):
    """
    This is the main function that reads form 4 file and process it and save it to .csv database
    
    inpath:   Path obj, directory for input files
    outpath:  Path obj, directory for output files
    filename: string, full filename of Form-4.txt file
    """
    
    # pre-processing .txt file, so that xml can be formatted properly with flatdict
    outfilename = filename + '.mod'
    proc_form4txt(inpath, outpath, filename, outfilename)
    
    # extract xml information to flatdict object
    full_dict = form4xml_toflatdict(outpath, outfilename)

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


def run_form4(inpath, outpath, readlist):
    """
    This function calls the main function form4_tocsv
    
    inpath:   string, directory for input files
    outpath:  string, directory for output files
    readlist: boolean, read the .txt files in the order specified by a file "list_txt"
    """
    
    if not readlist:
        directory = os.fsencode(inpath)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".txt"): 
                print(filename)
                form4_tocsv(Path(inpath), Path(outpath), filename)
    else:
        fileloc = Path(inpath) / "list_txt"
        infile  = open(fileloc, 'r')
        lines   = infile.readlines()

        for line in lines:
            filename = line.strip()
            print(filename)
            form4_tocsv(Path(inpath), Path(outpath), filename)

        infile.close()

    return
