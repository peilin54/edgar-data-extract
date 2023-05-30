#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import re
import xmltodict
import flatdict
from pathlib import Path
import os
import sys
from .f4data import f4data


def proc_form4txt(inpath, outpath, filename, outfilename):
    """
    This function processes the xml text for correct reading later using flatdict:
    1. Add a few lines to xml, so that flatdict can process things correctly
    2. Merge "Holding" to "Transaction", so that no separate form is needed
    3. Edit <footnotes> for flatdict to read
    
    inpath:      Path obj, input directory
    outpath:     Path obj, outnput directory
    filename:    string, full filename of Form-4.txt for pre-processing
    outfilename: string, full filename of file written: Form-4.txt.mod 
    """
    
    inloc  = inpath / filename
    outloc = outpath / outfilename

    infile  = open(inloc, 'r')
    lines   = infile.readlines()
    
    outfile = open(outloc,'w')
    for line in lines:
        # add line so that flatdic can process all as a list
        if r'</nonDerivativeTable>' in line and r'<nonDerivativeTable></nonDerivativeTable>' not in line:
            outfile.write(r'<nonDerivativeTransaction></nonDerivativeTransaction>' + "\n") 
        if r'</derivativeTable>' in line and r'<derivativeTable></derivativeTable>' not in line:
            outfile.write(r'<derivativeTransaction></derivativeTransaction>' + "\n") 
        if r'</footnotes>' in line and r'<footnotes></footnotes>' not in line:
            outfile.write(line.replace('</footnotes>', '<footnote><footnote_>  </footnote_></footnote></footnotes>'))
            continue
            
        # "Holding" and "Transaction" are slight variation of same table
        if 'nonDerivativeHolding' in line:
            outfile.write(line.replace('nonDerivativeHolding', 'nonDerivativeTransaction'))
            continue
        if 'derivativeHolding' in line:
            outfile.write(line.replace('derivativeHolding', 'derivativeTransaction'))
            continue
        
        # add additional nesting in footnote, so that flatdic process and separate the notes
        if r'<footnote ' in line:
            outfile.write(line.replace(' id', '><footnote_>id').replace('</footnote>', '</footnote_></footnote>'))
            continue
        if r'</footnote>' in line:
            outfile.write(line.replace('</footnote>', '</footnote_></footnote>'))
            continue
              
        outfile.write(line)
        
    outfile.close()
    infile.close()
    
    return


def form4xml_toflatdict(filepath, filename):
    """
    This function reads the processed form4.txt.mod, extract xml information and convert to a flatdict object.
    
    filepath: Path obj, file directory
    filename: string, full filename of file written: Form-4.txt.mod 
    """
    
    with open(filepath / filename) as f:
        data = f.read()

    # extract file around ownershipDocument 
    matcher = re.compile(r'<\?xml.*ownershipDocument>', flags=re.MULTILINE|re.DOTALL)
    matches = matcher.search(data)
    xml     = matches.group(0)

    # load entire xml to dict object
    xmldict = xmltodict.parse(xml)

    # use flatdict tool to flatten levels of dictionary for easy indexing
    return flatdict.FlatDict(xmldict["ownershipDocument"], delimiter='.')


def flatdict_toDF(table_d):
    """
    This function takes a flat dictionary object and process it as follows: 
    If there is only 1 item, it is a dictionary. Convert it to a pandas DF object
    If there are more than 1 item, it will be a list. We flat it further and convert it to a pandas DF object
    
    table_d: could be list or a pandas DataFrame that has two rows (one of them contains column names)
    return:  pandas DataFrame with column names
    """
    
    if isinstance(table_d, list):
        d_list = []
        for i in table_d:
            d_list.append(flatdict.FlatDict(i, delimiter='.'))
        
        return pd.DataFrame(d_list)
    
    else:
        tmp_df   = pd.DataFrame(table_d.items()).T
        col_name = tmp_df.iloc[0] 
    
        return tmp_df.drop([0]).reset_index(drop=True).rename(col_name, axis=1)


def form4df_tocsv(filepath, full_dict, issuer_df, reportingOwner_df):
    """
    This function takes read-in information and save it to .csv database
    
    filepath:          Path obj, directory for file
    full_dict:         flatdict, contains full flatdic read from xml 
    issuer_df:         pandas DataFrame, contains issuer info
    reportingOwner_df: pandas DataFrame, contains reporting owner info
    """

    exist_nonDer = False
    exist_der = False

    # work on nonDerivativeTable
    if "nonDerivativeTable.nonDerivativeTransaction" in full_dict.keys():
        nonDerivativeTable_df = flatdict_toDF(full_dict["nonDerivativeTable.nonDerivativeTransaction"])
        # add information about issuer and owner to the tables
        nonDerivative_cDF = concat_abtoC(issuer_df, reportingOwner_df, nonDerivativeTable_df)
        # remove the last row that was added for flatdict reading
        f4_nonDerivative  = f4data("nonDerivative", nonDerivative_cDF.iloc[:-1])
        save_dftocsv(filepath, "nonDerivative.csv", f4_nonDerivative.df)
        exist_nonDer = True
        
    # work on derivativeTable
    if "derivativeTable.derivativeTransaction" in full_dict.keys():
        derivativeTable_df= flatdict_toDF(full_dict["derivativeTable.derivativeTransaction"])
        derivative_cDF    = concat_abtoC(issuer_df, reportingOwner_df, derivativeTable_df)
        f4_derivative     = f4data("derivative", derivative_cDF.iloc[:-1])
        save_dftocsv(filepath, "derivative.csv", f4_derivative.df)
        exist_der = True
    
    # work on footnotes
    if "footnotes.footnote" in full_dict.keys():
        footnotes_df  = flatdict_toDF(full_dict["footnotes.footnote"])
        footnotes_cDF = concat_abtoC(issuer_df, reportingOwner_df, footnotes_df)
        f4_footnotes  = f4data("footnotes", footnotes_cDF.iloc[:-1])
        # add transaction date to footnotes table
        row = len(f4_footnotes.df.index)
        if exist_nonDer:
            transactionDate = [f4_nonDerivative.df["transactionDate.value"].iloc[0]]*row
        elif exist_der:
            transactionDate = [f4_derivative.df["transactionDate.value"].iloc[0]]*row
        else:
            raise Exception("Try to find transaction date for footnotes. Empty entries for nonDerivative and derivative tables.")
        footnotes_withdate = f4_footnotes.df
        footnotes_withdate["transactionDate"] = transactionDate
        save_dftocsv(filepath, "footnotes.csv", footnotes_withdate)
    
    return


def concat_abtoC(a, b, c):
    """
    This function takes three pandas DF objects a b and c (a and b has one row and c may have multiple rows) to:
    1. Duplicate lines of a and b to the same number of rows in c
    2. Merge a b and c to a large DF along axis=1
    
    a:      pandas DataFrame, one row only
    b:      pandas DataFrame, one row only
    c:      pandas DataFrame, may have multiple rows
    return: pandas DataFrame
    """
    
    n   = len(c.index)
    t1  = pd.concat([a]*n,ignore_index=True)
    t2  = pd.concat([b]*n,ignore_index=True)
    t12 = pd.concat([t1.reset_index(drop=True),t2.reset_index(drop=True)], axis=1)
    
    return pd.concat([t12.reset_index(drop=True),c.reset_index(drop=True)], axis=1)


def save_dftocsv(filepath, filename, df):
    """
    This function takes a pandas DF and save to specific filename in filepath.
    Append if file already exists.
    
    filepath: Path obj, directory for file
    filename: string, full filename for csv output   
    """
    
    fileloc = filepath / filename
    file_present = os.path.isfile(fileloc) 
    if file_present:
        df.to_csv(fileloc, index=False, mode='a', header=False)    
    else:
        df.to_csv(fileloc, index=False)
        
    return

