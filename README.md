# Information Extraction from EDGAR files

## Overview: 
Forms 3, 4, and 5 filings are reports submitted to the SEC by investors who may buy or sell shares in companies where they are deemed insiders. The SEC defines an insider as any officer, director or more than 10% shareholder of a publicly traded company.

* https://www.sec.gov/files/forms-3-4-5.pdf
* https://www.sec.gov/Archives/edgar/data/1326190/000101297517000759/xslF345X03/edgar.xml
* https://whalewisdomalpha.com/form-4-insider-trading-analysis/
* https://www.sec.gov/Archives/edgar/data/1318605/000149473018000006/xslF345X03/edgardoc.xml

These filings are publicly available through the [SEC EDGAR website](https://www.sec.gov/edgar/search/)

For example, here is a [Form 4](https://www.sec.gov/Archives/edgar/data/1326190/000101297517000759/)

The SEC describes Form 4 as [follows](https://www.sec.gov/files/forms-3-4-5.pdf):

>"In most cases, when an insider executes a transaction,
he or she must file a Form 4. With this form filing, the
public is made aware of the insider’s various transactions
in company securities, including the amount purchased
or sold and the price per share. Form 4 must be filed
within two business days following the transaction date.
Transactions in a company’s common stock as well as
derivative securities, such as options, warrants, and
convertible securities, are reported on the form. Each
transaction is coded to indicate the nature of the
transaction."
> 

## Objective:
The objective of this task is to extract information from Form 4 filings and store the information in a database. The database will be used to analyze insider trading activity. For our purposes, a database can consist of one or more flat files (e.g., in CSV format) that can be loaded into one or more Pandas dataframes.

The task template repository provides 100 Form 4 examples in the `data` directory. These files are text files, in a hybrid HTML/XML format (there is an HTML header, and an XML body) In real life, there are many thousands of these files and they are updated daily. We therefore need to automate the process of extracting information from these files and storing the information in a database. We would like for you to prototype a solution. Extract as much structured information as you can from the reports.

Our preference is for you to use Python code for this task. You may use Jupyter notebooks for exploration and to illustrate your solution. You may use any Python libraries you wish. You may also use any other tools you wish, but please be prepared to explain your choices.

## Deliverables:
We would like a command line interface that accepts a directory as input containing Form 4 files. Output should be one or more flat files (e.g. in CSV format) that extracts the relevant information from the Form 4 files. The output should be suitable for loading into a database, or into one or more Pandas dataframes.

Please use this git repository as a template for your solution. You may fork this repository and submit a pull request, or you may create a new repository and send us a link. Please include a README.md file that describes your solution and how to run it. Source code may go in the `edgar` directory. Test code should go in the `test` directory. You may add additional files and directories as needed. 

You will be asked to present and explain your prototype to the research support team (you will be given approximately 45 minutes to an hour, including questions). Some members of the team understand Python and some do not. Please be prepared to explain your solution to a mixed audience.