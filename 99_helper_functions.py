# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.3
#   kernelspec:
#     display_name: myenvpy3.9
#     language: python
#     name: python3
# ---

# %%
import pandas as pd 
from sec_api import XbrlApi


# %%
# convert XBRL-JSON of income statement to pandas dataframe
def get_income_statement(xbrl_json):
    income_statement_store = {}

    # iterate over each US GAAP item in the income statement
    for usGaapItem in xbrl_json['StatementsOfIncome']:
        values = []
        indicies = []

        for fact in xbrl_json['StatementsOfIncome'][usGaapItem]:
            # only consider items without segment. not required for our analysis.
            if 'segment' not in fact:
                index = fact['period']['startDate'] + '_' + fact['period']['endDate']
                # ensure no index duplicates are created
                if index not in indicies:
                    values.append(fact['value'])
                    indicies.append(index)                    

        income_statement_store[usGaapItem] = pd.Series(values, index=indicies) 

    income_statement = pd.DataFrame(income_statement_store)
    # switch columns and rows so that US GAAP items are rows and each column header represents a date range
    return income_statement.T 


# %%
# convert XBRL-JSON of Balance sheets to pandas dataframe
def get_balance_sheets(xbrl_json):
    balance_sheets_store = {}

    # iterate over each US GAAP item in the balance sheet statement
    for usGaapItem in xbrl_json['BalanceSheets']:
        values = []
        indicies = []

        for fact in xbrl_json['BalanceSheets'][usGaapItem]:
            # only consider items without segment. not required for our analysis.
            if 'segment' not in fact and 'value' in fact:
                period = fact['period']
                
                # Handle duration vs instant periods
                if 'startDate' in period and 'endDate' in period:
                    index = f"{period['startDate']}-{period['endDate']}"
                elif 'instant' in period:
                    index = period['instant']
                else:
                    continue  # skip if period structure is unexpected
                # index = fact['period']['startDate'] + '-' + fact['period']['endDate']

                # ensure no index duplicates are created
                if index not in indicies:
                    values.append(fact['value'])
                    indicies.append(index)
                        

        balance_sheets_store[usGaapItem] = pd.Series(values, index=indicies) 

    balance_sheets = pd.DataFrame(balance_sheets_store)
    # switch columns and rows so that US GAAP items are rows and each column header represents a date range
    return balance_sheets.T 


# %%
def get_cashflow(xbrl_json):
    cashflow_store = {}

    # iterate over each US GAAP item in the income statement
    for usGaapItem in xbrl_json['StatementsOfCashFlows']:
        values = []
        indicies = []

        for fact in xbrl_json['StatementsOfCashFlows'][usGaapItem]:
            # only consider items without segment. not required for our analysis.
            if 'segment' not in fact and 'value' in fact:
                # ensure no index duplicates are created
                period = fact['period'] 
                
                # Handle duration vs instant periods
                if 'startDate' in period and 'endDate' in period:
                    index = f"{period['startDate']}-{period['endDate']}"
                elif 'instant' in period:
                    index = period['instant']
                else:
                    continue  # skip if period structure is unexpected

                if index not in indicies:
                    values.append(fact['value'])
                    indicies.append(index)                    

        cashflow_store[usGaapItem] = pd.Series(values, index=indicies) 

    cashflow = pd.DataFrame(cashflow_store)
    # switch columns and rows so that US GAAP items are rows and each column header represents a date range
    return cashflow.T 
