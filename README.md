# Data Extraction from EDGAR Form 4 Files

## Overview 
Form 4 filings are publicly available through the [SEC EDGAR website](https://www.sec.gov/edgar/search/). Information in Form 4 can be used to analyze insider trading activity.  
This code extracts information from Form 4 filings and store the information in two databases in CSV format:
- **nonDerivative.csv**:  database that contains issuer, reporting owners, "Table I - Non-Derivative Securities Acquired, Disposed of, or Beneficially Owned" and footnotes inoformation in Form 4.
- **derivative.csv**:  database that contains issuer, reporting owners, "Table II - Derivative Securities Acquired, Disposed of, or Beneficially Owned" and footnotes information in Form 4.

Each entry has exactly one transaction/holding record along with the corresponding issuer, reporting owner and footnotes information.


## How to use
The source code is in the `edgar` directory and the tests are in the `tests` directory.  
### Requirement 
The following packages were used for developing this code.
>Python 3.10.6  
flatdict==4.0.1  
pandas==2.0.1  
xmltodict==0.13.0  
pytest==7.3.1  
>

### Command line interface
Command line execution requires providing an `input directory`, which contains Form 4 .txt files, and an `output directory`.  

```
edgar-data-extract$ python main.py -h
usage: main.py [-h] -i INPUT_PATH -o OUTPUT_PATH [-l LIST_ORDER]

SEC Edgar Form 4 reader

options:
  -h, --help            show this help message and exit
  -i INPUT_PATH, --input_path INPUT_PATH
                        Enter directory of input files
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Enter output directory
  -l LIST_ORDER, --list_order LIST_ORDER
                        Read the .txt files in the order specified by a file list_txt. For testing purpose. Default is False
  
  
# Use the ./scratch directory or replace with your output directory
edgar-data-extract$ python main.py  -i ./tests/test_1 -o ./scratch
```

The code finds **all** the `.txt` files in the input directory and generates two .csv output files: `nonDerivative.csv` and `derivative.csv`.  
**`Note:`** if the .csv files already `exist` in the directory, running the code will **`append`** entries to the existing .csv files.  
  
### Example/test cases
Examples and tests are in the `tests` folder. This folder contains a testing script, two test folders and a Jupyter Notebook.  
1. To test if code is running correctly on your machine, use the `pytest` tool. It runs tests in the `test_form4csv.py` script.
```
# execute at the edgar-data-extract directory
edgar-data-extract$ pytest 
======================================================================================== test session starts ========================================================================================
platform linux -- Python 3.10.6, pytest-7.3.1, pluggy-1.0.0
rootdir: 
collected 2 items                                                                                                                                                                                   

tests/test_form4csv.py ..                                                                                                                                                                     [100%]

========================================================================================= 2 passed in 4.38s =========================================================================================

```
  
2. There is one .txt file in the `test_1` folder and 100 .txt files in the `test_100` folder. Outputs files are available in those two folders for comparison. 
You can run individual test by executing the command line:
```
edgar-data-extract$ python main.py  -i ./tests/test_1 -o ./scratch

# The "-l" tag requests to read .txt files following the order in the list_txt file. Only needed for testing.
edgar-data-extract$ python main.py  -i ./tests/test_100 -o ./scratch -l True
```
  
3. The Jupyter Notebook `edgar_form4.ipynb` can be used for interactive exploration. Test cases for the notebook are in the `test_jup` folder.  

The generated .csv files can be loaded into Pandas DataFrames. Examples can be found at the end of the Jupyter notebook.

## Code structure

The downloaded .txt files from SEC Edgar website are text files, in a hybrid HTML/XML format (there is an HTML header, and an XML body). 
We use the *xmltodict* and *flatdict* library for processing the text documents and then use *Pandas DataFrame* for storing the data before saving them to .csv files.
- `main.py`: get command line arguments and start the program
- `edgar/edgar_form4.py`: contains the main `form4_to_csv` function that calls various functions to complete the current project
- `edgar/proc_form4.py`: functions for various specific tasks
- `edgar/form4data.py`: define the class `Form4Data`

```
def form4_to_csv
    # pre-processing txt file for loading into flatdict object
    def proc_form4txt

    # extract xml information and loaded into flatdict object
    def form4txt_to_flatdict

    # load flatdict object into Pandas DataFrames
    def flatdict_to_df

    # process Pandas DataFrames to save as .csv format    
    def form4df_to_csv
        # concatenate Pandas DataFrame, add issuer and reporting owners information to Tables
        def concat_abtoC
        # function for writing.csv file
        def save_df_to_csv
        # convert footnote information to dictionary
        def footnotes_to_dict
        # add footnote column to DataFrame
        def get_footnote_info


# Class that holds standard Form 4 column names and DataFrames
class Form4Data:
    self.df
    def __init__(self, df):
    # create dataframe during txt file reading
    def from_txt(cls, table_name, orig_df):
    # create dataframe from .csv file
    def from_csv(cls, input_path, filename):
    def check_10b5(self, text):
    # add a column of True/False regarding if footnotes contain 10b5 information
    def add_has_10b5(self):
    # check if read new unknown column names
    def _check_col_name(empty_df, orig_df):

```
