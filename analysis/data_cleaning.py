"""
Dispensary Data Cleaning Script
This script cleans and validates the raw transaction data, handling missing values,
duplicates, and formatting inconsistencies.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

# Load raw data
print("Loading raw data...")
raw_data_path = '../data/raw/dispensary_transactions.csv'
df = pd.read_csv(raw_data_path)

print(f"Initial dataset shape: {df.shape}")
print(f"Initial columns: {list(df.columns)}")
print("\n" + "="*60)

# Data Quality Assessment
print("\nDATA QUALITY ASSESSMENT")
print("="*60)
print("\n1. Missing Values:")
missing_summary = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    'Missing Count': missing_summary,
    'Percentage': missing_pct
})
print(missing_df[missing_df['Missing Count'] > 0])

print(f"\n2. Duplicate Transactions: {df.duplicated().sum()}")

# CLEANING PROCESS

print("\n" + "="*60)
print("STARTING DATA CLEANING PROCESS")
print("="*60)

# 1. Remove duplicate transactions
print("\n1. Removing duplicate transactions...")
initial_count = len(df)
df = df.drop_duplicates(keep='first')
duplicates_removed = initial_count - len(df)
print(f"   Removed {duplicates_removed} duplicate records")
print(f"   New dataset size: {len(df)} records")

# 2. Standardize date formats
print("\n2. Standardizing date formats...")
def parse_date(date_str):
    if pd.isna(date_str):
        return None
    
    date_str = str(date_str).strip()
    
    formats = ['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', '%Y/%m/%d']
    
    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except:
            continue
    
    try:
        return pd.to_datetime(date_str)
    except:
        return None

df['transaction_date'] = df['transaction_date'].apply(parse_date)
print(f"   Dates standardized to YYYY-MM-DD format")

# 3. Standardize city names
print("\n3. Standardizing city names...")
city_mapping = {
    'LA': 'Los Angeles',
    'los angeles': 'Los Angeles',
    'san diego': 'San Diego',
    'san francisco': 'San Francisco',
    'denver': 'Denver',
    'boulder': 'Boulder',
    'portland': 'Portland',
    'seattle': 'Seattle',
    'las vegas': 'Las Vegas',
    'phoenix': 'Phoenix',
    'tucson': 'Tucson'
}

df['customer_location_city'] = df['customer_location_city'].replace(city_mapping)
df['customer_location_city'] = df['customer_location_city'].str.title()
print(f"   City names standardized")

# 4. Standardize state abbreviations
print("\n4. Standardizing state abbreviations...")
state_mapping = {
    'California': 'CA',
    'california': 'CA',
    'ca': 'CA',
    'Colorado': 'CO',
    'colorado': 'CO',
    'co': 'CO',
    'Oregon': 'OR',
    'oregon': 'OR',
    'or': 'OR',
    'Washington': 'WA',
    'washington': 'WA',
    'wa': 'WA',
    'Nevada': 'NV',
    'nevada': 'NV',
    'nv': 'NV',
    'Arizona': 'AZ',
    'arizona': 'AZ',
    'az': 'AZ'
}

df['customer_location_state'] = df['customer_location_state'].replace(state_mapping)
df['customer_location_state'] = df['customer_location_state'].str.upper()
print(f"   State codes standardized")

# 5. Handle missing customer_age_group
print("\n5. Handling missing customer age groups...")
missing_age_before = df['customer_age_group'].isnull().sum()
age_mode = df['customer_age_group'].mode()[0]
df['customer_age_group'] = df['customer_age_group'].fillna(age_mode)
print(f"   Filled {missing_age_before} missing values with mode: {age_mode}")

# 6. Handle missing membership_tier
print("\n6. Handling missing membership tiers...")
missing_membership_before = df['membership_tier'].isnull().sum()
df['membership_tier'] = df['membership_tier'].fillna('Standard')
print(f"   Filled {missing_membership_before} missing values with 'Standard'")

# 7. Handle missing zip codes
print("\n7. Handling missing zip codes...")
missing_zip_before = df['zip_code'].isnull().sum()
for city in df['customer_location_city'].unique():
    city_zips = df[df['customer_location_city'] == city]['zip_code'].dropna()
    if len(city_zips) > 0:
        most_common_zip = city_zips.mode()[0] if len(city_zips.mode()) > 0 else city_zips.iloc[0]
        df.loc[(df['customer_location_city'] == city) & (df['zip_code'].isnull()), 'zip_code'] = most_common_zip

remaining_missing = df['zip_code'].isnull().sum()
if remaining_missing > 0:
    df['zip_code'] = df['zip_code'].fillna('00000')
print(f"   Filled {missing_zip_before} missing zip codes")

# 8. Convert zip_code to string and ensure 5 digits
df['zip_code'] = df['zip_code'].astype(str).str.split('.').str[0].str.zfill(5)

# 9. Create derived fields
print("\n8. Creating derived fields...")

# Extract month, quarter, year
df['transaction_month'] = df['transaction_date'].dt.month
df['transaction_quarter'] = df['transaction_date'].dt.quarter
df['transaction_year'] = df['transaction_date'].dt.year
df['month_year'] = df['transaction_date'].dt.to_period('M').astype(str)
df['day_of_week'] = df['transaction_date'].dt.day_name()

# Calculate days since first purchase per customer
customer_first_purchase = df.groupby('customer_id')['transaction_date'].min().to_dict()
df['customer_first_purchase_date'] = df['customer_id'].map(customer_first_purchase)
df['days_since_first_purchase'] = (df['transaction_date'] - df['customer_first_purchase_date']).dt.days

print(f"   Added: transaction_month, transaction_quarter, transaction_year")
print(f"   Added: month_year, day_of_week")
print(f"   Added: customer_first_purchase_date, days_since_first_purchase")

# 10. Data validation checks
print("\n" + "="*60)
print("DATA VALIDATION CHECKS")
print("="*60)

# Check for negative values
negative_quantity = (df['quantity'] < 0).sum()
negative_price = (df['unit_price'] < 0).sum()
negative_total = (df['total_amount'] < 0).sum()

print(f"\n1. Negative values check:")
print(f"   Negative quantities: {negative_quantity}")
print(f"   Negative unit prices: {negative_price}")
print(f"   Negative total amounts: {negative_total}")

# Check for unrealistic values
print(f"\n2. Price range validation:")
print(f"   Min unit price: ${df['unit_price'].min():.2f}")
print(f"   Max unit price: ${df['unit_price'].max():.2f}")
print(f"   Mean unit price: ${df['unit_price'].mean():.2f}")

# Check transaction total accuracy
df['calculated_total'] = df['quantity'] * df['unit_price']
df['total_difference'] = abs(df['total_amount'] - df['calculated_total'])
accuracy_issues = (df['total_difference'] > 0.01).sum()
print(f"\n3. Transaction total accuracy:")
print(f"   Transactions with calculation discrepancies: {accuracy_issues}")

# Fix any discrepancies
if accuracy_issues > 0:
    df['total_amount'] = df['calculated_total']
    print(f"   Recalculated total_amount for accuracy")

df = df.drop(['calculated_total', 'total_difference'], axis=1)

# Sort by date and transaction_id
df = df.sort_values(['transaction_date', 'transaction_id']).reset_index(drop=True)

# Final data quality report
print("\n" + "="*60)
print("FINAL DATA QUALITY REPORT")
print("="*60)
print(f"\nFinal dataset shape: {df.shape}")
print(f"Date range: {df['transaction_date'].min().date()} to {df['transaction_date'].max().date()}")
print(f"Unique customers: {df['customer_id'].nunique()}")
print(f"Unique products: {df['product_name'].nunique()}")
print(f"Product categories: {df['product_category'].nunique()}")
print(f"Total revenue: ${df['total_amount'].sum():,.2f}")
print(f"\nMissing values after cleaning:")
print(df.isnull().sum()[df.isnull().sum() > 0])

if df.isnull().sum().sum() == 0:
    print("No missing values remaining!")

# Save cleaned data
output_path = '../data/cleaned/dispensary_data_cleaned.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)

print(f"\n" + "="*60)
print(f"Data cleaning complete!")
print(f"Cleaned data saved to: {output_path}")
print("="*60)
