#!/usr/bin/env python


import pandas as pd


class Form4Data:
    """
    Create a class for holding formatted Form-4 data
    
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
        "ownershipNature.natureOfOwnership.value"
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
        "ownershipNature.natureOfOwnership.value"
        ]
   
    footnotes_col_name = ["footnote_"]
    
    
    def __init__(self, table_name, orig_df):
        """
        This function creates a DataFrame, with standardized column names, and dropped redundant entries
        
        table_name: string, name of database to create
        orig_df:    pandas DataFrame, full table contains all the data columns        
        """
        if table_name == "nonDerivative":
            column_list = self.issuer_col_name + self.reporting_col_name + self.nonderivative_col_name
        elif table_name == "derivative":
            column_list = self.issuer_col_name + self.reporting_col_name + self.derivative_col_name
        elif table_name == "footnotes":
            column_list = self.issuer_col_name + self.reporting_col_name + self.footnotes_col_name
        else:
            raise ValueError("Unknown table name!")
            
        # could do some more checking with column_names after concat         
        empty_df = pd.DataFrame(columns=column_list)
        self.df  = pd.concat([empty_df,orig_df])[list(column_list)]

        self._check_col_name(empty_df, orig_df)


    def _check_col_name(self, empty_df, orig_df):
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


