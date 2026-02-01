"""
Dispensary Data Exploratory Analysis
This script performs comprehensive business analysis including KPIs, customer churn,
regional performance, and product insights.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("DISPENSARY DATA EXPLORATORY ANALYSIS")
print("="*70)

# Load cleaned data
print("\nLoading cleaned data...")
df = pd.read_csv('../data/cleaned/dispensary_data_cleaned.csv')
df['transaction_date'] = pd.to_datetime(df['transaction_date'])
df['customer_first_purchase_date'] = pd.to_datetime(df['customer_first_purchase_date'])

print(f"Dataset loaded: {len(df)} transactions")
print(f"Date range: {df['transaction_date'].min().date()} to {df['transaction_date'].max().date()}")

# ============================================================================
# 1. KEY PERFORMANCE INDICATORS (KPIs)
# ============================================================================

print("\n" + "="*70)
print("1. KEY PERFORMANCE INDICATORS")
print("="*70)

total_revenue = df['total_amount'].sum()
total_transactions = len(df)
unique_customers = df['customer_id'].nunique()
avg_transaction_value = df['total_amount'].mean()
avg_items_per_transaction = df.groupby('transaction_id')['quantity'].sum().mean()

print(f"\nOverall Business Metrics:")
print(f"  Total Revenue: ${total_revenue:,.2f}")
print(f"  Total Transactions: {total_transactions:,}")
print(f"  Unique Customers: {unique_customers:,}")
print(f"  Average Transaction Value: ${avg_transaction_value:.2f}")
print(f"  Average Items per Transaction: {avg_items_per_transaction:.2f}")

# Customer metrics
transactions_per_customer = df.groupby('customer_id').size()
avg_transactions_per_customer = transactions_per_customer.mean()
repeat_customers = (transactions_per_customer > 1).sum()
repeat_customer_rate = (repeat_customers / unique_customers) * 100

print(f"\nCustomer Engagement:")
print(f"  Average Transactions per Customer: {avg_transactions_per_customer:.2f}")
print(f"  Repeat Customers: {repeat_customers:,} ({repeat_customer_rate:.1f}%)")
print(f"  One-time Customers: {unique_customers - repeat_customers:,}")

# ============================================================================
# 2. CUSTOMER CHURN ANALYSIS
# ============================================================================

print("\n" + "="*70)
print("2. CUSTOMER CHURN ANALYSIS")
print("="*70)

# Define churn: customers who haven't purchased in the last 90 days
latest_date = df['transaction_date'].max()
churn_threshold_days = 90
churn_date = latest_date - timedelta(days=churn_threshold_days)

customer_last_purchase = df.groupby('customer_id')['transaction_date'].max()
churned_customers = (customer_last_purchase < churn_date).sum()
active_customers = unique_customers - churned_customers
churn_rate = (churned_customers / unique_customers) * 100
retention_rate = 100 - churn_rate

print(f"\nChurn Metrics (90-day threshold):")
print(f"  Total Customers: {unique_customers:,}")
print(f"  Active Customers: {active_customers:,}")
print(f"  Churned Customers: {churned_customers:,}")
print(f"  Churn Rate: {churn_rate:.2f}%")
print(f"  Retention Rate: {retention_rate:.2f}%")

# Churn by customer segment
print(f"\nChurn Analysis by Segment:")

# By age group
churn_by_age = df.groupby('customer_id').agg({
    'customer_age_group': 'first',
    'transaction_date': 'max'
})
churn_by_age['churned'] = churn_by_age['transaction_date'] < churn_date
age_churn_summary = churn_by_age.groupby('customer_age_group')['churned'].agg(['sum', 'count'])
age_churn_summary['churn_rate'] = (age_churn_summary['sum'] / age_churn_summary['count'] * 100).round(2)
age_churn_summary.columns = ['Churned', 'Total', 'Churn_Rate_%']
print(f"\n  By Age Group:")
print(age_churn_summary)

# By membership tier
churn_by_membership = df.groupby('customer_id').agg({
    'membership_tier': 'first',
    'transaction_date': 'max'
})
churn_by_membership['churned'] = churn_by_membership['transaction_date'] < churn_date
membership_churn_summary = churn_by_membership.groupby('membership_tier')['churned'].agg(['sum', 'count'])
membership_churn_summary['churn_rate'] = (membership_churn_summary['sum'] / membership_churn_summary['count'] * 100).round(2)
membership_churn_summary.columns = ['Churned', 'Total', 'Churn_Rate_%']
print(f"\n  By Membership Tier:")
print(membership_churn_summary)

# Customer lifetime value
customer_ltv = df.groupby('customer_id')['total_amount'].sum().describe()
print(f"\nCustomer Lifetime Value (LTV) Statistics:")
print(f"  Mean LTV: ${customer_ltv['mean']:.2f}")
print(f"  Median LTV: ${customer_ltv['50%']:.2f}")
print(f"  Max LTV: ${customer_ltv['max']:.2f}")

# ============================================================================
# 3. REGIONAL DEMAND ANALYSIS
# ============================================================================

print("\n" + "="*70)
print("3. REGIONAL DEMAND ANALYSIS")
print("="*70)

# Revenue by state
revenue_by_state = df.groupby('customer_location_state').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'customer_id': 'nunique'
}).round(2)
revenue_by_state.columns = ['Total_Revenue', 'Transactions', 'Unique_Customers']
revenue_by_state['Avg_Transaction_Value'] = (revenue_by_state['Total_Revenue'] / revenue_by_state['Transactions']).round(2)
revenue_by_state = revenue_by_state.sort_values('Total_Revenue', ascending=False)

print("\nPerformance by State:")
print(revenue_by_state)

# Revenue by city (top 10)
revenue_by_city = df.groupby('customer_location_city').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'customer_id': 'nunique'
}).round(2)
revenue_by_city.columns = ['Total_Revenue', 'Transactions', 'Unique_Customers']
revenue_by_city['Avg_Transaction_Value'] = (revenue_by_city['Total_Revenue'] / revenue_by_city['Transactions']).round(2)
revenue_by_city = revenue_by_city.sort_values('Total_Revenue', ascending=False)

print("\nTop 10 Cities by Revenue:")
print(revenue_by_city.head(10))

# Product category preference by region (top 3 states)
print("\nProduct Category Preferences by Top States:")
top_3_states = revenue_by_state.head(3).index

for state in top_3_states:
    state_data = df[df['customer_location_state'] == state]
    category_revenue = state_data.groupby('product_category')['total_amount'].sum().sort_values(ascending=False)
    print(f"\n  {state}:")
    for category, revenue in category_revenue.items():
        percentage = (revenue / category_revenue.sum() * 100)
        print(f"    {category}: ${revenue:,.2f} ({percentage:.1f}%)")

# ============================================================================
# 4. PRODUCT PERFORMANCE ANALYSIS
# ============================================================================

print("\n" + "="*70)
print("4. PRODUCT PERFORMANCE ANALYSIS")
print("="*70)

# Revenue by category
category_performance = df.groupby('product_category').agg({
    'total_amount': 'sum',
    'quantity': 'sum',
    'transaction_id': 'count'
}).round(2)
category_performance.columns = ['Total_Revenue', 'Units_Sold', 'Transactions']
category_performance['Avg_Price'] = (category_performance['Total_Revenue'] / category_performance['Units_Sold']).round(2)
category_performance['Revenue_Pct'] = (category_performance['Total_Revenue'] / category_performance['Total_Revenue'].sum() * 100).round(2)
category_performance = category_performance.sort_values('Total_Revenue', ascending=False)

print("\nProduct Category Performance:")
print(category_performance)

# Top 10 products by revenue
product_performance = df.groupby('product_name').agg({
    'total_amount': 'sum',
    'quantity': 'sum',
    'transaction_id': 'count',
    'product_category': 'first'
}).round(2)
product_performance.columns = ['Total_Revenue', 'Units_Sold', 'Transactions', 'Category']
product_performance = product_performance.sort_values('Total_Revenue', ascending=False)

print("\nTop 10 Products by Revenue:")
print(product_performance.head(10))

# Top 10 products by quantity
print("\nTop 10 Products by Units Sold:")
print(product_performance.sort_values('Units_Sold', ascending=False).head(10)[['Category', 'Units_Sold', 'Total_Revenue']])

# ============================================================================
# 5. REVENUE TRENDS & SEASONALITY
# ============================================================================

print("\n" + "="*70)
print("5. REVENUE TRENDS & SEASONALITY")
print("="*70)

# Monthly revenue trend
monthly_revenue = df.groupby('month_year').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'customer_id': 'nunique'
}).round(2)
monthly_revenue.columns = ['Revenue', 'Transactions', 'Customers']

print("\nMonthly Revenue Trend:")
print(monthly_revenue)

# Calculate growth rates
monthly_revenue['Revenue_Growth_%'] = monthly_revenue['Revenue'].pct_change() * 100
print(f"\nAverage Monthly Revenue Growth: {monthly_revenue['Revenue_Growth_%'].mean():.2f}%")

# Quarterly performance
quarterly_revenue = df.groupby(['transaction_year', 'transaction_quarter']).agg({
    'total_amount': 'sum',
    'transaction_id': 'count'
}).round(2)
quarterly_revenue.columns = ['Revenue', 'Transactions']

print("\nQuarterly Revenue:")
print(quarterly_revenue)

# Day of week analysis
dow_performance = df.groupby('day_of_week').agg({
    'total_amount': 'sum',
    'transaction_id': 'count'
}).round(2)
dow_performance.columns = ['Revenue', 'Transactions']
dow_performance['Avg_Transaction_Value'] = (dow_performance['Revenue'] / dow_performance['Transactions']).round(2)

# Reorder by weekday
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dow_performance = dow_performance.reindex([d for d in day_order if d in dow_performance.index])

print("\nPerformance by Day of Week:")
print(dow_performance)

# ============================================================================
# 6. CUSTOMER SEGMENTATION
# ============================================================================

print("\n" + "="*70)
print("6. CUSTOMER SEGMENTATION")
print("="*70)

# Segment customers by purchase frequency
customer_summary = df.groupby('customer_id').agg({
    'transaction_id': 'count',
    'total_amount': 'sum',
    'transaction_date': ['min', 'max']
}).round(2)
customer_summary.columns = ['Purchase_Count', 'Total_Spent', 'First_Purchase', 'Last_Purchase']
customer_summary['Customer_Lifetime_Days'] = (
    pd.to_datetime(customer_summary['Last_Purchase']) - 
    pd.to_datetime(customer_summary['First_Purchase'])
).dt.days

# Segment customers
def segment_customer(row):
    if row['Purchase_Count'] == 1:
        return 'One-time'
    elif row['Purchase_Count'] <= 3:
        return 'Occasional'
    elif row['Purchase_Count'] <= 10:
        return 'Regular'
    else:
        return 'VIP'

customer_summary['Segment'] = customer_summary.apply(segment_customer, axis=1)

segment_analysis = customer_summary.groupby('Segment').agg({
    'Purchase_Count': ['count', 'mean'],
    'Total_Spent': ['sum', 'mean']
}).round(2)

print("\nCustomer Segmentation Analysis:")
print(segment_analysis)

# Age group analysis
age_performance = df.groupby('customer_age_group').agg({
    'total_amount': 'sum',
    'customer_id': 'nunique',
    'transaction_id': 'count'
}).round(2)
age_performance.columns = ['Total_Revenue', 'Customers', 'Transactions']
age_performance['Avg_Revenue_per_Customer'] = (age_performance['Total_Revenue'] / age_performance['Customers']).round(2)
age_performance = age_performance.sort_values('Total_Revenue', ascending=False)

print("\nPerformance by Age Group:")
print(age_performance)

# Membership tier performance
membership_performance = df.groupby('membership_tier').agg({
    'total_amount': 'sum',
    'customer_id': 'nunique',
    'transaction_id': 'count'
}).round(2)
membership_performance.columns = ['Total_Revenue', 'Customers', 'Transactions']
membership_performance['Avg_Revenue_per_Customer'] = (membership_performance['Total_Revenue'] / membership_performance['Customers']).round(2)

tier_order = ['Standard', 'Silver', 'Gold', 'Platinum']
membership_performance = membership_performance.reindex([t for t in tier_order if t in membership_performance.index])

print("\nPerformance by Membership Tier:")
print(membership_performance)

# ============================================================================
# 7. PAYMENT METHOD ANALYSIS
# ============================================================================

print("\n" + "="*70)
print("7. PAYMENT METHOD ANALYSIS")
print("="*70)

payment_analysis = df.groupby('payment_method').agg({
    'total_amount': 'sum',
    'transaction_id': 'count'
}).round(2)
payment_analysis.columns = ['Total_Revenue', 'Transactions']
payment_analysis['Avg_Transaction_Value'] = (payment_analysis['Total_Revenue'] / payment_analysis['Transactions']).round(2)
payment_analysis['Percentage_of_Transactions'] = (payment_analysis['Transactions'] / payment_analysis['Transactions'].sum() * 100).round(2)
payment_analysis = payment_analysis.sort_values('Total_Revenue', ascending=False)

print("\nPayment Method Analysis:")
print(payment_analysis)

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*70)
print("KEY INSIGHTS SUMMARY")
print("="*70)

print(f"""
Business Overview:
- Generated ${total_revenue:,.2f} in revenue across {total_transactions:,} transactions
- Served {unique_customers:,} unique customers with an average transaction value of ${avg_transaction_value:.2f}
- {repeat_customer_rate:.1f}% repeat customer rate indicates strong customer loyalty

Customer Health:
- Current churn rate: {churn_rate:.2f}%
- Retention rate: {retention_rate:.2f}%
- Average customer lifetime value: ${customer_ltv['mean']:.2f}

Top Performing Regions:
- Best state: {revenue_by_state.index[0]} (${revenue_by_state.iloc[0]['Total_Revenue']:,.2f})
- Best city: {revenue_by_city.index[0]} (${revenue_by_city.iloc[0]['Total_Revenue']:,.2f})

Product Insights:
- Top category: {category_performance.index[0]} ({category_performance.iloc[0]['Revenue_Pct']:.1f}% of revenue)
- Best selling product: {product_performance.index[0]}

Growth Metrics:
- Average monthly revenue growth: {monthly_revenue['Revenue_Growth_%'].mean():.2f}%
""")

print("="*70)
print("Analysis Complete!")
print("="*70)
