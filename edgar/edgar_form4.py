#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import argparse
import os
import sys
from pathlib import Path
import flatdict
from .proc_form4 import proc_form4txt, form4xml_to_flatdict, flatdict_to_df, form4df_to_csv, concat_abtoC, save_df_to_csv


def form4_to_csv(input_path, output_path, filename):
    """
    This is the main function that reads form 4 file and process it and save it to .csv database
    
    input_path:   Path obj, directory for input files
    output_path:  Path obj, directory for output files
    filename: string, full filename of Form-4.txt file
    """
    
    # pre-processing .txt file, so that xml can be formatted properly with flatdict
    output_filename = filename + '.mod'
    proc_form4txt(input_path, output_path, filename, output_filename)
    
    # extract xml information to flatdict object
    full_dict = form4xml_to_flatdict(output_path, output_filename)

    # create subsections from the full dictionary
    # issuer and reportingOwner first; hopefully these fields are populated
    issuer_df = flatdict_to_df(full_dict["issuer"])
          
    if isinstance(full_dict["reportingOwner"], list):
        for item in full_dict["reportingOwner"]:
            tmp = flatdict.FlatDict(item, delimiter='.')
            reportingOwner_df = flatdict_to_df(tmp)
            form4df_to_csv(output_path, full_dict, issuer_df, reportingOwner_df)
        
        # # DEBUG only: use only one reporting Owner for multiple owner cases
        # item=full_dict["reportingOwner"][0]
        # tmp = flatdict.FlatDict(item, delimiter='.')
        # reportingOwner_df = flatdict_to_df(tmp)
        # form4df_to_csv(output_path, full_dict, issuer_df, reportingOwner_df)
        # # DEBUG only

    else:
        reportingOwner_df = flatdict_to_df(full_dict["reportingOwner"])
        form4df_to_csv(output_path, full_dict, issuer_df, reportingOwner_df)
        
    return


def run_form4(input_path, output_path, list_order):
    """
    This function calls the main function form4_to_csv
    
    input_path:   string, directory for input files
    output_path:  string, directory for output files
    list_order: boolean, read the .txt files in the order specified by a file "list_txt"
    """
    
    if not list_order:
        directory = os.fsencode(input_path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".txt"): 
                print("Processing: " + filename)
                form4_to_csv(Path(input_path), Path(output_path), filename)
    else:
        fileloc = Path(input_path) / "list_txt"
        with open(fileloc, 'r') as f:
            for line in f:
                filename = line.strip()
                print("Processing: " + filename)
                form4_to_csv(Path(input_path), Path(output_path), filename)

    return
