# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np

df = pd.read_csv(r"M:\Kemsley Paper Mill\Technical\Technical\PM4\Furnish Data\NSP Furnish CSV.csv", encoding='mac_roman') #imports excel file

df.reset_index(drop=True, inplace=True)

df_t = df.transpose()

new_header = df_t.iloc[0] #grab the first row for the header
df_t = df_t[1:] #take the data less the header row
df_t.columns = new_header #set the header row as the df heade

df_t.reset_index(inplace=True)
df_t = df_t.rename(columns={'index': 'Date'}) # renames the column name Index to Date


df_t.loc[df_t['Date'].str.contains("Unnamed:"), 'Date'] = np.nan # Replaces all the "Unnamed" cells with NaN object value for ffill to work later
df_t['Date'] = pd.to_datetime(df_t['Date'], format='%d/%m/%Y') #convert to Datetime, ffill doesnt work on object types

u = df_t.select_dtypes(include=['datetime']) # Selects Datetime column for ffill and saves as U series
df_t[u.columns] = u.fillna(method='ffill', inplace=True) # forward fills the column replacing nan values

df_t['Date'] = u # brings the new ffill column u to the dataframm
df_t['Date'] = df_t['Date'].dt.strftime('%d/%m/%Y') # changes format to 01/01/2021 - removes time element

#------------------Rename Columns---------------------#
df_t.drop(columns=["ALine"], inplace=True)

df_t.rename(columns={ df_t.columns[3]: "Aline OKLS" }, inplace = True)
df_t.rename(columns={ df_t.columns[4]: "Aline NKLS" }, inplace = True)
df_t.rename(columns={ df_t.columns[5]: "Aline MWP" }, inplace = True)
df_t.rename(columns={ df_t.columns[6]: "Aline Loose" }, inplace = True)
df_t.rename(columns={ df_t.columns[7]: "Aline ToPlan" }, inplace = True)
df_t.rename(columns={ df_t.columns[8]: "Aline De-wires" }, inplace = True)

df_t.drop(columns=["Comments"], inplace=True) #drop column not needed 

df_t['Aline OKLS'].astype(str)
df_t.loc[(df_t['Aline OKLS'] == 'shut'), 'Aline OKLS'] = '0' # remove shut values (needs to be int column)

#df_t['Aline OKLS'] = pd.to_numeric(df_t['Aline OKLS'])

df_t[['Aline OKLS','Aline NKLS','Aline MWP']] = df_t[['Aline OKLS','Aline NKLS','Aline MWP']].apply(pd.to_numeric) #change dtype to int

# collection of rules to apply values across columns based on value in another column - to allow forward fill to be used

df_t.loc[(df_t['Aline OKLS'] == 100), ['Aline NKLS','Aline MWP', 'Aline Loose']] = 0
df_t.loc[(df_t['Aline OKLS'] == 0), ['Aline NKLS','Aline MWP', 'Aline Loose']] = 0
df_t.loc[(df_t['Aline OKLS'] + df_t['Aline MWP']) ==100, ['Aline NKLS', 'Aline Loose']] = 0
df_t.loc[(df_t['Aline OKLS'] + df_t['Aline NKLS']) ==100, ['Aline MWP', 'Aline Loose']] = 0
df_t.loc[(df_t['Aline OKLS'] + df_t['Aline NKLS']+df_t['Aline MWP']) ==100, ['Aline Loose']] = 0

df_t.loc[(df_t['Aline NKLS'] == 100), ['Aline OKLS','Aline MWP', 'Aline Loose']] = 0
df_t.loc[(df_t['Aline NKLS'] + df_t['Aline MWP']) ==100, ['Aline OKLS', 'Aline Loose']] = 0

df_t[['Aline OKLS','Aline NKLS','Aline MWP']]=df_t[['Aline OKLS','Aline NKLS','Aline MWP']].ffill() # forward fill the columns

df_ABline = df_t[['Date', 'Time', 'Aline OKLS','Aline NKLS','Aline MWP', 'Aline ToPlan']]


#df_Aline.to_csv(r"M:\Kemsley Paper Mill\Technical\Technical\PM4\Furnish Data\Aline Furnish (Complete).csv", index = False)


#--------------------B LINE ------------------------------------#
df_t.drop(columns=["B-Line"], inplace=True)

df_t.rename(columns={ df_t.columns[8]: "Bline OKLS" }, inplace = True)
df_t.rename(columns={ df_t.columns[9]: "Bline NKLS" }, inplace = True)
df_t.rename(columns={ df_t.columns[10]: "Bline MWP" }, inplace = True)
df_t.rename(columns={ df_t.columns[11]: "Bline Loose" }, inplace = True)
df_t.rename(columns={ df_t.columns[12]: "Bline ToPlan" }, inplace = True)
df_t.rename(columns={ df_t.columns[13]: "Bline De-wires" }, inplace = True)

df_t[['Bline OKLS','Bline NKLS','Bline MWP']] = df_t[['Bline OKLS','Bline NKLS','Bline MWP']].apply(pd.to_numeric) #change dtype to int

df_t.loc[(df_t['Bline OKLS'] == 100), ['Bline NKLS','Bline MWP', 'Bline Loose']] = 0
df_t.loc[(df_t['Bline OKLS'] == 0), ['Bline NKLS','Bline MWP', 'Bline Loose']] = 0
df_t.loc[(df_t['Bline OKLS'] + df_t['Bline MWP']) ==100, ['Bline NKLS', 'Bline Loose']] = 0
df_t.loc[(df_t['Bline OKLS'] + df_t['Bline NKLS']) ==100, ['Bline MWP', 'Bline Loose']] = 0
df_t.loc[(df_t['Bline OKLS'] + df_t['Bline NKLS']+df_t['Bline MWP']) ==100, ['Bline Loose']] = 0

df_t.loc[(df_t['Bline NKLS'] == 100), ['Bline OKLS','Bline MWP', 'Bline Loose']] = 0
df_t.loc[(df_t['Bline NKLS'] + df_t['Bline MWP']) ==100, ['Bline OKLS', 'Bline Loose']] = 0

df_t[['Bline OKLS','Bline NKLS','Bline MWP']]=df_t[['Bline OKLS','Bline NKLS','Bline MWP']].ffill() # forward fill the columns


df_ABline = df_t[['Date', 'Time', 'Aline OKLS','Aline NKLS','Aline MWP', 'Aline ToPlan','Bline OKLS','Bline NKLS','Bline MWP', 'Bline ToPlan', 'C-Line Running (y/n)']]

df_ABline.to_csv(r"M:\Kemsley Paper Mill\Technical\Technical\PM4\Furnish Data\ABline Furnish (Complete).csv", index = False)

