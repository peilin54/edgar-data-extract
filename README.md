# Data Extraction from EDGAR Form 4 Files

## Overview 
Form 4 filings are publicly available through the [SEC EDGAR website](https://www.sec.gov/edgar/search/). Information in Form 4 can be used to analyze insider trading activity.  
This code extracts information from Form 4 filings and store the information in three databases in CSV format:
- **nonDerivative.csv**:  database that contains issuer, reporting owners and information for "Table I - Non-Derivative Securities Acquired, Disposed of, or Beneficially Owned" in Form 4.
- **derivative.csv**:  database that contains issuer, reporting owners and informatoin for "Table II - Derivative Securities Acquired, Disposed of, or Beneficially Owned" in Form 4.
- **footnotes.csv**:  database that contains issuer, reporting owners, footnotes and transaction date in Form 4.  

Each entry has exactly one transaction/holding record along with the corresponding issuer and reporting owner information.


## How to use
The source code is in the `edgar` directory and the tests are in the `tests` directory.  
### Requirement 
Python 3.10.6  
Specific packages used for devloping this code.
>flatdict==4.0.1  
pandas==2.0.1  
xmltodict==0.13.0  
pytest==7.3.1  
>

### Command line interface
Command line execution requires providing an `input directory`, which contains Form 4 .txt files, and an `output directory`.  


```
$ python main.py -h
usage: main.py [-h] -inpath INPATH -outpath OUTPATH [-readlist READLIST]

SEC Edgar Form 4 reader

options:
  -h, --help            show this help message and exit
  -inpath INPATH, --inpath INPATH
                        Enter directory of input files
  -outpath OUTPATH, --outpath OUTPATH
                        Enter output directory
  -readlist READLIST, --readlist READLIST
                        Read the .txt files in the order specified by a file list_txt. For testing purpose. Default is False


# Create the ./scratch directory or replace with your output directory
$ python main.py  -inpath ./tests/test_1 -outpath ./scratch
```

The code generates three .csv output files: `nonDerivative.csv`, `derivative.csv`, and `footnotes.csv`.  
**`Note:`** if the .csv files already `exist` in the directory, running the code will **`append`** entries to the existing .csv files.  
The generated .csv files can be loaded into Pandas DataFrames in a Python shell or Jupyter Notebook as:
```
import pandas as pd

# ./scratch/ should be modified to be your local dictectory containing those .csv files.
load_nd_data = pd.read_csv("./scratch/nonDerivative.csv")
```
  
### Example/test cases
Examples are in the `tests` folder. This folder contains two test folders and a Jupiter Notebook.
1. There is one .txt file int the `test_1` folder and 100 .txt files in the `test_100` folder. Outputs files are available in those two folders for comparison. 
You can run individual test by executing the command line:
```
$ python main.py  -inpath ./tests/test_1 -outpath ./scratch

# The "-readlist" tag requests to read .txt files following the order in the list_txt file
$ python main.py  -inpath ./tests/test_100 -outpath ./scratch -readlist True
```
To test if code is running correctly on your machine, use the `pytest` tool.
```
# execute outside tests folder at the edgar-data-extract directory
$ pytest 
=========================================================================================== test session starts ===========================================================================================
platform linux -- Python 3.10.6, pytest-7.3.1, pluggy-1.0.0
rootdir: 
collected 2 items                                                                                                                                                                                         

tests/test_outcsv.py ..                                                                                                                                                                             [100%]

============================================================================================ 2 passed in 3.85s ============================================================================================

```
  
2. The Jupyter Notebook `edgar_form4.ipynb` can be used for interactive exploration. Test cases for the notebook are in the `test_jup` folder.

## Code structure

The downloaded .txt files from SEC Edgar website are text files, in a hybrid HTML/XML format (there is an HTML header, and an XML body). 
We use the *xmltodict* and *flatdict* library for processing the text documents and then use Pandas DataFrame for storing the data before saving them to .csv files.

```
def form4_tocsv
    # pre-processing txt file for loading into flatdict object
    def proc_form4txt

    # extract xml information and loaded into flatdict object
    def form4xml_toflatdict

    # load flatdict object into Pandas DataFrames
    def flatdict_toDF

    # process Pandas DataFrames to save as .csv format    
    def form4df_tocsv
        # concatenate Pandas DataFrame, add issuer and reporting owners information to Tables
        def concat_abtoC
        # function for writing.csv file
        def save_dftocsv

# Class that holds standard Form 4 column names and DataFrames
class f4data:
    # check if read new unknown column names
    def check_colname
```
