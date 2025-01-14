# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 13:38:51 2025

@author: sadhyar
"""

import pandas as pd
import numpy as np

#Load the sales data from an excel file to a pandas dataframe

sales_data = pd.read_excel('C:/Users/sadhyar/Desktop/Amazon Sales Project/sales_data.xlsx')


# =============================================================================
# Exploring the Data
# =============================================================================

#Get a summary of sales data
sales_data.info()   #Can also check data types

sales_data.describe()

#Looking at columns
print(sales_data.columns)

#Having a look at the first few rows of the data
print(sales_data.head())

#Check data types of columns
print(sales_data.dtypes)

# =============================================================================
# Cleaning the data
# =============================================================================

#Checking for missing values in our sales data
sales_data.isnull()
print(sales_data.isnull().sum())

#Drop any rows that has missing / NAN value
sales_data_dropped = sales_data.dropna()
sales_data_dropped.isnull()

#Drop rows with missing amounts based on the amount column
sales_data_clean = sales_data.dropna(subset = ['Amount'])
sales_data_clean.isnull()
print(sales_data_clean.isnull().sum())

#How many sales have they made with the Amount > 1000
sales_greater_than_1000 = sales_data_clean[sales_data_clean['Amount'] > 1000].count()
print(sales_greater_than_1000)

sales_greater_than_1K = sales_data_clean[sales_data_clean['Amount'] > 1000]

#How many sales have they made belong to the category 'Tops' and have a quantity of 3
sales_tops_3 = sales_data_clean[(sales_data_clean['Category'] == 'Tops') & (sales_data_clean['Qty'] == 3)].count()
print(sales_tops_3)

# =============================================================================
# SLICING AND FILTERING DATA
# =============================================================================

#Select a subset of our data based on the category column
category_data = sales_data[sales_data['Category'] == 'Top']
print(category_data)

#Select a subset of the data where amount is greater than 1000
high_amount_data = sales_data[sales_data['Amount']>1000]
print(high_amount_data)

#Select a subset of data based on mulitple conditions
filtered_data = sales_data[(sales_data['Category'] == 'Top') & (sales_data['Qty'] == 3)]
print(filtered_data)

# =============================================================================
# Aggregating data
# =============================================================================

#Total Sales by Category
category_totals = sales_data.groupby('Category', as_index=False)['Amount'].sum()


#Total Sales by Category sorted

category_totals =  category_totals.sort_values('Amount', ascending=False)

#Calculate average amount by category and fulfillment
fulfillment_averages = sales_data.groupby(['Category', 'Fulfilment'], as_index=False)['Amount'].mean()
fulfillment_averages = fulfillment_averages.sort_values('Amount', ascending=False)

#Calculate average amount by category and status
status_averages = sales_data.groupby(['Category', 'Status'], as_index=False)['Amount'].mean()
status_averages = status_averages.sort_values('Amount', ascending=False)

#Total Sales by Fulfilmewnt and shipment type
total_sales_shipandfulfil = sales_data.groupby(['Fulfilment', 'Courier Status'], as_index=False)['Amount'].sum()
total_sales_shipandfulfil = total_sales_shipandfulfil. sort_values('Amount', ascending=False)

#Renaming DataFrames
total_sales_shipandfulfil.rename(columns = {'Courier Status' : 'Shipment'}, inplace=True)

# =============================================================================
# Exporting the Data
# =============================================================================

status_averages.to_excel('average_sales_by_category_and_status.xlsx', index=False) #Exporting data after removing index
total_sales_shipandfulfil.to_excel('total_sales_by_ship_and_fulfil.xlsx', index=False)
