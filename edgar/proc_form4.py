#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import re
import xmltodict
import flatdict
from pathlib import Path
import os
import sys
from .form4data import Form4Data


def proc_form4txt(input_path, output_path, filename, output_filename):
    """
    This function processes the xml text for correct reading later using flatdict:
    1. Add empty xml elements to xml, so that flatdict can process items consistently
    2. Merge "Holding" to "Transaction", so that no separate form is needed
    3. Edit <footnotes> for flatdict to read properly
    
    input_path:      Path obj, input directory
    output_path:     Path obj, outnput directory
    filename:    string, full filename of Form-4.txt for pre-processing
    output_filename: string, full filename of file written: Form-4.txt.mod 
    """
    
    input_file_loc  = input_path / filename
    output_file_loc = output_path / output_filename

    with open(input_file_loc, 'r') as lines:
    
        with open(output_file_loc,'w') as output_file:
            for line in lines:
                # add empty xml elements so that flatdic can process all as a list
                if r'</nonDerivativeTable>' in line and r'<nonDerivativeTable></nonDerivativeTable>' not in line:
                    output_file.write(r'<nonDerivativeTransaction></nonDerivativeTransaction>' + "\n") 
                if r'</derivativeTable>' in line and r'<derivativeTable></derivativeTable>' not in line:
                    output_file.write(r'<derivativeTransaction></derivativeTransaction>' + "\n") 
                if r'</footnotes>' in line and r'<footnotes></footnotes>' not in line:
                    output_file.write(line.replace(r'</footnotes>', r'<footnote><footnote_>  </footnote_></footnote></footnotes>'))
                    continue
                    
                # "Holding" and "Transaction" are slight variation of same table
                if 'nonDerivativeHolding' in line:
                    output_file.write(line.replace('nonDerivativeHolding', 'nonDerivativeTransaction'))
                    continue
                if 'derivativeHolding' in line:
                    output_file.write(line.replace('derivativeHolding', 'derivativeTransaction'))
                    continue
                
                # add additional nesting in footnote, so that flatdic process and separate the notes
                if r'<footnote ' in line:
                    output_file.write(line.replace(' id', '><footnote_>id').replace(r'</footnote>', r'</footnote_></footnote>'))
                    continue
                if r'</footnote>' in line:
                    output_file.write(line.replace(r'</footnote>', r'</footnote_></footnote>'))
                    continue
                      
                output_file.write(line)
    
    return


def form4xml_to_flatdict(filepath, filename):
    """
    This function reads the processed form4.txt.mod, extract xml information and convert to a flatdict object.
    
    filepath: Path obj, file directory
    filename: string, full filename of file written: Form-4.txt.mod 
    return:   flatdict obj
    """
    
    input_file_loc  = filepath / filename
    with open(input_file_loc) as f:
        data = f.read()
    
    # delete the temporary .txt.mod file
    input_file_loc.unlink()

    # extract file around ownershipDocument 
    matcher = re.compile(r'<\?xml.*ownershipDocument>', flags=re.MULTILINE|re.DOTALL)
    matches = matcher.search(data)
    xml     = matches.group(0)

    # load entire xml to dict object
    xmldict = xmltodict.parse(xml)

    # use flatdict tool to flatten levels of dictionary for easy indexing
    return flatdict.FlatDict(xmldict["ownershipDocument"], delimiter='.')


def flatdict_to_df(table_d):
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


def form4df_to_csv(filepath, full_dict, issuer_df, reportingOwner_df):
    """
    This function takes read-in information and save it to .csv database
    
    filepath:          Path obj, directory for file
    full_dict:         flatdict, contains full flatdic read from xml 
    issuer_df:         pandas DataFrame, contains issuer info
    reportingOwner_df: pandas DataFrame, contains reporting owner info
    """

    # work on footnotes
    if "footnotes.footnote" in full_dict.keys():
        footnotes_df  = flatdict_to_df(full_dict["footnotes.footnote"])
        footnotes_dict = footnotes_to_dict(footnotes_df["footnote_"])
    
    # work on nonDerivativeTable
    if "nonDerivativeTable.nonDerivativeTransaction" in full_dict.keys():
        nonDerivativeTable_df = flatdict_to_df(full_dict["nonDerivativeTable.nonDerivativeTransaction"])
        
        # check if there is footnote information to add
        col_has_footnote = [col for col in nonDerivativeTable_df.columns if 'footnote' in col]
        if col_has_footnote:
            nonDerivativeTable_df = get_footnote_info(nonDerivativeTable_df, footnotes_dict, col_has_footnote)
        
        # add information about issuer and owner to the tables
        nonDerivative_cDF = concat_abtoC(issuer_df, reportingOwner_df, nonDerivativeTable_df)
        # remove the last row that was added for flatdict reading
        f4_nonDerivative  = Form4Data.from_txt("nonDerivative", nonDerivative_cDF.iloc[:-1])
        save_df_to_csv(filepath, "nonDerivative.csv", f4_nonDerivative.df)
        
    # work on derivativeTable
    if "derivativeTable.derivativeTransaction" in full_dict.keys():
        derivativeTable_df= flatdict_to_df(full_dict["derivativeTable.derivativeTransaction"])
        
        # check if there is footnote information to add
        col_has_footnote = [col for col in derivativeTable_df.columns if 'footnote' in col]
        if col_has_footnote:
            derivativeTable_df = get_footnote_info(derivativeTable_df, footnotes_dict, col_has_footnote)
                
        derivative_cDF    = concat_abtoC(issuer_df, reportingOwner_df, derivativeTable_df)
        f4_derivative     = Form4Data.from_txt("derivative", derivative_cDF.iloc[:-1])
        save_df_to_csv(filepath, "derivative.csv", f4_derivative.df)
    
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


def save_df_to_csv(filepath, filename, df):
    """
    This function takes a pandas DF and save to specific filename in filepath.
    Append if file already exists.
    
    filepath: Path obj, directory for file
    filename: string, full filename for csv output   
    df:       pandas DataFrame
    """
    
    fileloc = filepath / filename
    file_present = os.path.isfile(fileloc) 
    if file_present:
        df.to_csv(fileloc, index=False, mode='a', header=False)    
    else:
        df.to_csv(fileloc, index=False)
        
    return
                                           

def footnotes_to_dict(footnotes_df):
    """
    This function converts footnote column to a dictionary
    footnotes_df:  pandas Series
    return:        dict obj
    """
    
    footnote_dict = {}
    
    for i, value in footnotes_df.iloc[:-1].items():
        s_tmp, s_text = value.split(r'>')
        s_id = s_tmp.split(r'"')[1]
           
        footnote_dict[s_id] = s_id + r': ' + s_text

    return footnote_dict
    
    
def get_footnote_info(df, footnotes_dict, col_has_footnote):
    """
    This function 
    1. Read the index location and id value from the footnoteat column.
    2. Create a footnote column, append footnote entry to the correct location.

    df:               pandas DataFrame, target dataframe to append footnote column
    footnotes_dict:   dictonary obj, contains id -> string details
    col_has_footnote: list of column names with footnote
    return:           pandas DataFrame
    """
           
    # for each footnote column, save index and footnote key
    f_index = []
    f_value= []
    
    for i in col_has_footnote:
        # iterate over values inside footnote column
        for idx, value in df[i].items():
            # more than one footnotes in this tag
            if isinstance(value, list):
                for j in value:
                    f_index.append(idx)
                    f_value.append(footnotes_dict[j["@id"]])
            else:
                if "F" in str(value):
                    f_index.append(idx)
                    f_value.append(footnotes_dict[value])

    tmp_df = pd.Series(f_value, index = f_index, name='footnote')
    footnote_col = tmp_df.groupby(level=0).transform(lambda x: ' '.join(x)).drop_duplicates()
    
    return pd.concat([df,footnote_col], axis=1)


