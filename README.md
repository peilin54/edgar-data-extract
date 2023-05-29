# Information Extraction from EDGAR files

## Overview: 
Form 4 filings are publicly available through the [SEC EDGAR website](https://www.sec.gov/edgar/search/). Information in Form 4 can be used to analyze insider trading activity.

This code extracts information from Form 4 filings and store the information in three database in CSV format:
>nonDerivative.csv: database that contains issuer, reporting owners and information for "Table I - Non-Derivative Securities Acquired, Disposed of, or Beneficially Owned" in Form 4.
derivative.csv: database that contains issuer, reporting owners and informatoin for "Table II - Derivative Securities Acquired, Disposed of, or Beneficially Owned" in Form 4.
footnotes.csv: database that contains issuer, reporting owners and footnotes in Form 4.
>

They can be loaded into Pandas DataFrames.


## How to use this code

Command line execution takes a directory as input containing Form 4 txt files.  


The code generates three .csv output files. If the .csv files already exist in the directory, running the code will append entries to the existing .csv files.



## Example and test cases


## How the code is structured


def form4_tocsv(filepath, filename)
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

# Class that holds standard column names and DataFrames
class f4data:
    # check if read new unknown column names
    def check_colname


The task template repository provides 100 Form 4 examples in the `data` directory. These files are text files, in a hybrid HTML/XML format (there is an HTML header, and an XML body) In real life, there are many thousands of these files and they are updated daily. We therefore need to automate the process of extracting information from these files and storing the information in a database. We would like for you to prototype a solution. Extract as much structured information as you can from the reports.


We would like a command line interface that accepts a directory as input containing Form 4 files. Output should be one or more flat files (e.g. in CSV format) that extracts the relevant information from the Form 4 files. The output should be suitable for loading into a database, or into one or more Pandas dataframes.

Please use this git repository as a template for your solution. You may fork this repository and submit a pull request, or you may create a new repository and send us a link. Please include a README.md file that describes your solution and how to run it. Source code may go in the `edgar` directory. Test code should go in the `test` directory. You may add additional files and directories as needed. 

You will be asked to present and explain your prototype to the research support team (you will be given approximately 45 minutes to an hour, including questions). Some members of the team understand Python and some do not. Please be prepared to explain your solution to a mixed audience.
