#!/usr/bin/env python


import pandas as pd


class Form4Data:
    """
    Create a class for holding formatted Form-4 data
    
    self.df: pandas DataFrame
    
    """
       
    issuer_col_name = ["issuerCik", "issuerName", "issuerTradingSymbol"]
    
    reporting_col_name = [
        "reportingOwnerId.rptOwnerCik",
        "reportingOwnerId.rptOwnerName",
        "reportingOwnerAddress.rptOwnerStreet1",
        "reportingOwnerAddress.rptOwnerStreet2",
        "reportingOwnerAddress.rptOwnerCity",
        "reportingOwnerAddress.rptOwnerState",
        "reportingOwnerAddress.rptOwnerZipCode",
        "reportingOwnerAddress.rptOwnerStateDescription",
        "reportingOwnerRelationship.isDirector",
        "reportingOwnerRelationship.isOfficer",
        "reportingOwnerRelationship.isTenPercentOwner",
        "reportingOwnerRelationship.isOther",
        "reportingOwnerRelationship.officerTitle",
        "reportingOwnerRelationship.otherText"
        ]

    nonderivative_col_name = [
        "securityTitle.value",
        "transactionDate.value",
        "deemedExecutionDate.value",
        "transactionCoding.transactionCode",
        "transactionTimeliness.value",
        "transactionAmounts.transactionShares.value",
        "transactionAmounts.transactionAcquiredDisposedCode.value",
        "transactionAmounts.transactionPricePerShare.value",
        "postTransactionAmounts.sharesOwnedFollowingTransaction.value",
        "ownershipNature.directOrIndirectOwnership.value",
        "ownershipNature.natureOfOwnership.value",
        "footnote"
        ]
        
    derivative_col_name = [
        "securityTitle.value",
        "conversionOrExercisePrice.value",
        "transactionDate.value",
        "deemedExecutionDate.value",
        "transactionCoding.transactionCode",
        "transactionTimeliness.value",
        "transactionAmounts.transactionAcquiredDisposedCode.value",
        "transactionAmounts.transactionShares.value",
        "exerciseDate.value",
        "expirationDate.value",
        "underlyingSecurity.underlyingSecurityTitle.value",
        "underlyingSecurity.underlyingSecurityShares.value",
        "transactionAmounts.transactionPricePerShare.value",
        "postTransactionAmounts.sharesOwnedFollowingTransaction.value",
        "ownershipNature.directOrIndirectOwnership.value",
        "ownershipNature.natureOfOwnership.value",
        "footnote"
        ]
   
    footnotes_col_name = ["footnote_"]
        
    def __init__(self, df):
        self.df =df
    
    
    @classmethod
    def from_txt(cls, table_name, orig_df):
        """
        This function creates a DataFrame, with standardized column names, and dropped redundant entries
        
        table_name: string, name of database to create
        orig_df:    pandas DataFrame, full table contains all the data columns        
        """
        if table_name == "nonDerivative":
            column_list = cls.issuer_col_name + cls.reporting_col_name + cls.nonderivative_col_name
        elif table_name == "derivative":
            column_list = cls.issuer_col_name + cls.reporting_col_name + cls.derivative_col_name
        elif table_name == "footnotes":
            column_list = cls.issuer_col_name + cls.reporting_col_name + cls.footnotes_col_name
        else:
            raise ValueError("Unknown table name!")
            
        # could do some more checking with column_names after concat         
        empty_df = pd.DataFrame(columns=column_list)
        df  = pd.concat([empty_df,orig_df])[column_list]

        cls._check_col_name(empty_df, orig_df)
        
        return cls(df)

    
    @staticmethod
    def _check_col_name(empty_df, orig_df):
        """
        This function checks if the code is reading new unknown column names
        
        empty_df: pandas DataFrame, contains empty DataFrame with columns that have standard names
        orig_df:  pandas DataFrame, full table contains all the data columns 
        """

        # Exclude already known list of outliers:
        #         footnote
        #         transactionCoding.transactionFormType (4 for these forms, not included in database)
        #         transactionCoding.equitySwapInvolved (field not used by form 4)
        #         transactionTimeliness (if it's still here, it's a duplicate)
        #         deemedExecutionDate, empty field, populated field should be deemedExecutionDate.value
        #         transactionTimeliness, empty field, pupulated field should be transactionTimeliness.value

        out_list = list(set(orig_df.columns.values) - set(empty_df.columns.values))
        for coln in out_list:
            i = coln.lower()
            if ("footnote" not in i and "equityswap" not in i
            and "formtype" not in i and "transactiontimeliness" not in i
            and "transactiontimeliness" not in i and "deemedexecutiondate" not in i):
                assert("Warning: unmatched column name: "+coln)
   
        return
    
    
    @classmethod
    def from_csv(cls, input_path, filename):
        """
        This function load data from .csv file

        input_path:  Path obj, input directory
        filename:    string, full filename of .csv file 
        """
        input_file_loc  = input_path / filename
        df = pd.read_csv(input_file_loc)

        return cls(df)
    
    
    def check_10b5(self, text):
        """
        This function checks if 10b5 is mentioned in the footnote text.
        text:   string
        return: boolean
        """
        return "10b5" in text if isinstance(text, str) else False
    
    
    def add_has_10b5(self):
        tmp = self.df['footnote'].apply(self.check_10b5)
        tmp.name = "has_10b5"
        self.df = pd.concat([self.df, tmp], axis=1)
        
        return
        

