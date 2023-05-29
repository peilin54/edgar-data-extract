# Information Extraction from EDGAR Form 4 files

## Overview 
Form 4 filings are publicly available through the [SEC EDGAR website](https://www.sec.gov/edgar/search/). Information in Form 4 can be used to analyze insider trading activity.  
This code extracts information from Form 4 filings and store the information in three databases in CSV format:
- ***nonDerivative.csv***:  database that contains issuer, reporting owners and information for "Table I - Non-Derivative Securities Acquired, Disposed of, or Beneficially Owned" in Form 4.
- ***derivative.csv***:  database that contains issuer, reporting owners and informatoin for "Table II - Derivative Securities Acquired, Disposed of, or Beneficially Owned" in Form 4.
- ***footnotes.csv***:  database that contains issuer, reporting owners and footnotes in Form 4.

## How to use this code
The source code is in the `edgar` directory and the test code is in the `tests` directory.  
Command line execution takes a directory as input, which contains Form 4 txt files.  


```
$ python3 edgar_form4.py -h
usage: edgar_form4.py [-h] -inpath INPATH [-outpath OUTPATH]

SEC Edgar Form 4 reader

options:
  -h, --help            show this help message and exit
  -inpath INPATH, --inpath INPATH
                        Enter directory of input files, include trailing "/"
  -outpath OUTPATH, --outpath OUTPATH
                        Enter output directory (optional), include trailing "/". Default is same as input directory
  -readlist READLIST, --readlist READLIST
                        Read file from a list. For testing purpose. Default is False

$ python3 edgar_form4.py -inpath /home/user/data/
# /home/user/data/ should be modified to be your local dictectory containing those .txt files.
```

The code generates three .csv output files: `nonDerivative.csv`, `derivative.csv`, and `footnotes.csv`.  
**`Note:`** if the .csv files already `exist` in the directory, running the code will **`append`** entries to the existing .csv files.  
These files can be loaded into Pandas DataFrames as:
```
import pandas as pd

# /home/user/data/ should be modified to be your local dictectory containing those .csv files.
load_nd_data = pd.read_csv("/home/user/data/nonDerivative.csv")
```
  
## Example and test cases
Examples are in the `tests` folder. This folder contains 2 test.
```
# Clean folder before running new test.
cd tests
clean_testfolder.sh

# Run tests with scripts
run_testfolder.sh
```
You may also run each test manually.
1. Run code with one .txt in the ./test-1/ folder. Then use shell `diff` to compare output .csv files with those in ./test-1/test_data folder.
```
cd tests
clean_testfolder.sh
python ../edgar/edgar_form4.py -inpath ./test-1/test_data/ -outpath ./test-1/ 

cd test-1
diff nonDerivative.csv test_data/
diff derivative.csv  test_data/
diff footnotes.csv  test_data/
cd ..
```
2. Run code with 100 .txt files in ./test-100/ folder. Compare output .csv files with those in ./test-100/test_data.  
This will read from a list_txt file to get file reading order, to minimize difference caused by system reading the 100 files in different order.
```
cd tests
clean_testfolder.sh
python ../edgar/edgar_form4.py -inpath ./test-100/test_data/ -outpath ./test-100/ -readlist True

cd test-100
diff nonDerivative.csv test_data/
diff derivative.csv  test_data/
diff footnotes.csv  test_data/
cd ..
```

## How the code is structured

The downloaded txt files from SEC Edgar website are text files, in a hybrid HTML/XML format (there is an HTML header, and an XML body). 
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
