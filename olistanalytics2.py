# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:50:57 2025

@author: sadhyar
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set the working directory
os.chdir('C:/Users/sadhyar/Desktop/Ecommerce Orders Project')

# Check the current working directory
os.getcwd()
print(os.getcwd())

# =============================================================================
# Loading Files
# =============================================================================

# Load the orders data
orders_data = pd.read_excel('orders.xlsx')

# Load the payments data
# If it was a CSV file, then you would have used pd.read_csv('filename.csv')

payments_data = pd.read_excel('order_payment.xlsx')

# Load the customers data
customers_data = pd.read_excel('customers.xlsx')

# =============================================================================
# Describing the data
# =============================================================================
orders_data.describe()
payments_data.describe()
customers_data.describe()
orders_data.info()
payments_data.info()
customers_data.info()

# =============================================================================
# Handling Missing data
# =============================================================================

# Check for missing data in the orders data

orders_data.isnull().sum()
payments_data.isnull().sum()
customers_data.isnull().sum()

# Filling in the missing values in the orders data with a default value

orders_data2 = orders_data.fillna('N/A')

# Check if there are null values in the orders_data2

orders_data2.isnull().sum()

# Drop rows with missing values in payments data

payments_data2 = payments_data.dropna()

# Check if there are null values in the payments data

payments_data2.isnull().sum()

# =============================================================================
# Removing Duplicate data
# =============================================================================

# Check for Duplicates in our orders data

orders_data.duplicated().sum()

# Check for Duplicates in our payments data

payments_data.duplicated().sum()

# Check for Duplicates in our customers data

customers_data.duplicated().sum()

#Remove duplicates from orders data

orders_data = orders_data.drop_duplicates()
orders_data.duplicated().sum()

#Remove duplicates from payments data

payments_data = payments_data.drop_duplicates()
payments_data.duplicated().sum()

# =============================================================================
# Filtering the data
# =============================================================================

# Select a subset of the order data based on the order status
invoiced_orders_data = orders_data[orders_data['order_status'] == 'invoiced']

#Reset the index
invoiced_orders_data = invoiced_orders_data.reset_index(drop=True) 

#Select a subset of the payments_data where payment type = Credit Card and payment value > 1000
credit_card_payments_data = payments_data[(payments_data['payment_type'] == 'credit_card') & (payments_data['payment_value'] > 1000)]

#Reset the index
credit_card_payments_data = credit_card_payments_data.reset_index(drop=True)

# Select a subset of customers based on customer state = SP
customer_data_state = customers_data[customers_data['customer_state'] == 'SP']

#Reset the index

customer_data_state = customer_data_state.reset_index(drop=True)


# =============================================================================
# Merging and Joining different Data Frames
# =============================================================================

# Merge orders_data with payments_data on order_id column

merged_data = pd.merge(orders_data, payments_data, on='order_id')

#Join the merged data with customers_data on customer_id column
joined_data = pd.merge(merged_data, customers_data, on='customer_id')

# =============================================================================
# Data Visualization
# =============================================================================

# Create a field called month_year from order_purchase_timestamp

joined_data['month_year'] = joined_data['order_purchase_timestamp'].dt.to_period('M')
joined_data['week_year'] = joined_data['order_purchase_timestamp'].dt.to_period('W')
joined_data['year'] = joined_data['order_purchase_timestamp'].dt.to_period('Y')

grouped_data = joined_data.groupby(['month_year'], as_index=False)['payment_value'].sum()

#Convert month_year from period to string
grouped_data['month_year'] = grouped_data['month_year'].astype(str)

#Creating a plot
plt.plot(grouped_data['month_year'], grouped_data['payment_value'], color='red', marker = 'o')
plt.ticklabel_format(useOffset=False, style='plain', axis = 'y')
plt.xlabel('Month and Year')
plt.ylabel('Payment Value')
plt.title('Payment value by month and year')
plt.xticks(rotation = 90, fontsize=8)
plt.yticks(fontsize=8)
plt.show()

#Scatter Plot

# Create the DataFrame

scatter_df = joined_data.groupby('customer_unique_id', as_index=False).agg({'payment_value': 'sum', 'payment_installments' : 'sum'})

plt.scatter(scatter_df['payment_value'], scatter_df['payment_installments'])
plt.xlabel('Payment Values')
plt.ylabel('Payment Installments')
plt.title('Payment Values vs Installments by Customer')
plt.show()

# Using seaborn to create a scatter plot

sns.set_theme(style = 'darkgrid') #whitegrid, darkgrid, dark, white

sns.scatterplot(scatter_df, x='payment_value', y='payment_installments')
plt.xlabel('Payment Values')
plt.ylabel('Payment Installments')
plt.title('Payment Values vs Installments by Customer')
plt.show()

# Creating a bar chart
bar_chart_df = joined_data.groupby(['payment_type','month_year'], as_index=False)['payment_value'].sum()

pivot_data = bar_chart_df.pivot(index='month_year', columns='payment_type',values='payment_value')
#pivot_data = pivot_data.reset_index(drop=True)

pivot_data.plot(kind='bar',stacked='True')
plt.ticklabel_format(useOffset=False, style='plain', axis='y')
plt.xlabel('Month of Payment')
plt.ylabel('Payment value')
plt.title('Payment per Payment Type by Month')
plt.show()


# Creating a Box Plot

payment_values = joined_data['payment_value']
payment_types = joined_data['payment_type']

#Creating a separate box plot per payment type

plt.boxplot([ payment_values[payment_types=='credit_card'],
             payment_values[payment_types=='boleto'],
             payment_values[payment_types=='voucher'],
             payment_values[payment_types=='debit_card']],
            labels = ['Credit Card', 'Boleto', 'Voucher', 'Debit Card']
            )
plt.xlabel('Payment Type')
plt.ylabel('Payment Value')
plt.title('Box Plot showing Payment Value ranges by Payment Type')
plt.show()

#Creating a sub plot (3 plots in one)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize = (10,10))


#ax1 is boxplot

ax1.boxplot([ payment_values[payment_types=='credit_card'],
             payment_values[payment_types=='boleto'],
             payment_values[payment_types=='voucher'],
             payment_values[payment_types=='debit_card']],
            labels = ['Credit Card', 'Boleto', 'Voucher', 'Debit Card']
            )
ax1.set_xlabel('Payment Type')
ax1.set_ylabel('Payment Value')
ax1.set_title('Box Plot showing Payment Value ranges by Payment Type')

#ax2 is the stacked barchart

pivot_data.plot(kind='bar',stacked='True', ax=ax2)
ax2.ticklabel_format(useOffset=False, style='plain', axis='y')
ax2.set_xlabel('Month of Payment')
ax2.set_ylabel('Payment value')
ax2.set_title('Payment per Payment Type by Month')


#ax3 is a scatterplot

ax3.scatter(scatter_df['payment_value'], scatter_df['payment_installments'])
ax3.set_xlabel('Payment Values')
ax3.set_ylabel('Payment Installments')
ax3.set_title('Payment Values vs Installments by Customer')

fig.tight_layout()

plt.savefig('myplot.png')
plt.show()


orders_df = pd.DataFrame({
    'OrderID': [1, 2, 3, 4, 5],
    'Product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Mouse'],
    'Quantity': [1, 2, 1, 1, 3],
    'Price': [1000, 20, 100, 200, 25]
})

# Task 1: Calculate and print total revenue for each product

product_revenue = orders_df.groupby('Product').apply(lambda x: (x.Quantity * x.Price).sum())
print(product_revenue)
 
# Task 2: Create a bar chart of total revenue for each product

product_revenue.plot(kind='bar')
plt.xlabel('Product')
plt.ylabel('Total Revenue')
plt.title('Total Revenue for Each Product')
plt.show()






















































































































































