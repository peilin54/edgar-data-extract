#!/usr/bin/env python


import pandas as pd


class f4data:
    """
    Create a class for holding formatted Form-4 data
    
    """
       
    issuer_list = ["issuerCik", "issuerName", "issuerTradingSymbol"]
    
    reporting_list = [
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

    nonDerivative_list = [
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
        
    derivative_list = [
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
   
    footnotes_list = ["footnote_"]
    
    
    def __init__(self, table_name, orig_df):
        """
        This function creates a DataFrame, with standardized column names, and dropped redundant entries
        
        table_name: string, name of database to create
        orig_df:    pandas DataFrame, full table contains all the data columns        
        """
        if table_name == "nonDerivative":
            column_list = self.issuer_list + self.reporting_list + self.nonDerivative_list
        elif table_name == "derivative":
            column_list = self.issuer_list + self.reporting_list + self.derivative_list
        elif table_name == "footnotes":
            column_list = self.issuer_list + self.reporting_list + self.footnotes_list
        else:
            raise ValueError("Unknown table name!")
            
        # could do some more checking with column_names after concat         
        empty_df = pd.DataFrame(columns=column_list)
        self.df  = pd.concat([empty_df,orig_df])[column_list]

        self.check_colname(empty_df, orig_df)


    def check_colname(self, empty_df, orig_df):
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
                print("Unmatched column name: "+coln)
        
        return


