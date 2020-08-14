# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 19:23:17 2020

@author: Kostya Zektser
"""

'''
Given a randomly populated dataset of funds, cashflows and dates, this script aims to group the cashflows per date, per fund, into a table
and output the results into a .csv file.
'''

import os
import pandas as pd
import getpass
import datetime as dt
from functools import reduce

user_name = getpass.getuser()
main_directory = f'C:\\Users\\{user_name}\\Desktop'
os.chdir(main_directory) # change working directory to the above directory
file_name = 'transaction_data.xlsx' # this file should be saved on your desktop

def balance_effect(text):
    ''' 
    if the transaction type is 'Deposit', multiply the amount by 1;
    if the transaction type is 'Withdrawal', multiply the amount by -1;
    '''
    balance_effect_dict = {'Deposit': 1, 'Withdrawal': -1}
    return balance_effect_dict[text]

def date_to_string(date):
    '''
    convert date to string format
    '''
    return dt.datetime.strftime(date, "%Y-%m-%d")

df2 = None

for file in os.listdir('.'):
    if file == file_name: # check if file exists in the current working directory
        df = pd.read_excel(main_directory + '\\' + file_name)
        df['ActualAmount'] = [balance_effect(x)*y for x, y in zip(list(df.Type), list(df.Amount))] # balance effect is either 1 or -1.
        df2 = df.groupby(['Fund', 'Date'], as_index = False)['ActualAmount'].sum()
        unique_dates = list(set(list(df2.Date)))
        
        # dictionary of dataframes
        df_dict = {date: df2.loc[ df2.Date == date , ['Fund', 'ActualAmount'] ].reset_index(drop = True) for date in unique_dates}
        df_dict2 = {date: dataframe.rename(columns = {'ActualAmount': f'Cashflow {date_to_string(date)}'}, inplace = True) for date, dataframe in df_dict.items()}
        
        # merge data frames
        df3 = reduce(lambda  df_left , df_right: pd.merge(df_left , df_right, on = ['Fund'] , how = 'outer'), df_dict.values())
# output csv file with Cashflow projections for each fund        
df3.to_csv("Cashflows.csv", index = False)
    
    

