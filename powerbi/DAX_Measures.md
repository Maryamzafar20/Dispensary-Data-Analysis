# Power BI DAX Measures
## Dispensary Analytics Dashboard

This document showcases the DAX measures created for the Dispensary Analytics Dashboard. These measures enable dynamic calculations and advanced analytics across customer behavior, product performance, and business KPIs.

---

## 📊 Basic Business Metrics

### Total Revenue
Calculates the sum of all transaction amounts across the dataset.

```dax
Total Revenue = 
SUM(dispensary_data_cleaned[total_amount])
```

### Total Transactions
Counts the total number of transaction records.

```dax
Total Transactions = 
COUNTROWS(dispensary_data_cleaned)
```

### Unique Customers
Counts distinct customers who have made purchases.

```dax
Unique Customers = 
DISTINCTCOUNT(dispensary_data_cleaned[customer_id])
```

### Average Transaction Value
Calculates the average revenue per transaction.

```dax
Avg Transaction Value = 
DIVIDE([Total Revenue], [Total Transactions], 0)
```

### Total Items Sold
Sums up all product quantities sold.

```dax
Total Items Sold = 
SUM(dispensary_data_cleaned[quantity])
```

### Average Items per Transaction
Calculates the average number of items in each transaction.

```dax
Avg Items per Transaction = 
DIVIDE([Total Items Sold], [Total Transactions], 0)
```

---

## 👥 Customer Metrics

### Active Customers
Counts customers who made purchases within the last 90 days (from November 2025 onwards).

```dax
Active Customers = 
CALCULATE(
    DISTINCTCOUNT(dispensary_data_cleaned[customer_id]),
    FILTER(
        ALL(dispensary_data_cleaned),
        dispensary_data_cleaned[transaction_date] >= DATE(2025, 11, 1)
    )
)
```

### Churned Customers
Calculates the number of customers who have not purchased in the last 90 days.

```dax
Churned Customers = 
[Unique Customers] - [Active Customers]
```

### Churn Rate
Percentage of customers who have stopped purchasing.

```dax
Churn Rate = 
DIVIDE([Churned Customers], [Unique Customers], 0)
```

### Retention Rate
Percentage of customers who remain active.

```dax
Retention Rate = 
1 - [Churn Rate]
```

### Repeat Customer Count
Counts customers who have made more than one purchase.

```dax
Repeat Customer Count = 
CALCULATE(
    DISTINCTCOUNT(dispensary_data_cleaned[customer_id]),
    FILTER(
        ADDCOLUMNS(
            VALUES(dispensary_data_cleaned[customer_id]),
            "TxnCount", CALCULATE(COUNTROWS(dispensary_data_cleaned))
        ),
        [TxnCount] > 1
    )
)
```

### Repeat Customer Rate
Percentage of customers who are repeat purchasers.

```dax
Repeat Customer Rate = 
DIVIDE([Repeat Customer Count], [Unique Customers], 0)
```

### Average Customer Lifetime Value
Average total spend per customer across their entire purchase history.

```dax
Avg Customer LTV = 
DIVIDE([Total Revenue], [Unique Customers], 0)
```

### One-time Customers
Counts customers who have made exactly one purchase.

```dax
One-time Customers = 
[Unique Customers] - [Repeat Customer Count]
```

---

## 📅 Time Intelligence Measures

### Revenue Year-to-Date
Calculates cumulative revenue from the start of the year to the current date.

```dax
Revenue YTD = 
TOTALYTD([Total Revenue], dispensary_data_cleaned[transaction_date])
```

### Revenue Previous Month
Returns revenue from the previous month for comparison.

```dax
Revenue Previous Month = 
CALCULATE(
    [Total Revenue],
    DATEADD(dispensary_data_cleaned[transaction_date], -1, MONTH)
)
```

### Revenue Growth Percentage
Calculates month-over-month revenue growth rate.

```dax
Revenue Growth % = 
DIVIDE(
    [Total Revenue] - [Revenue Previous Month],
    [Revenue Previous Month],
    0
)
```

### Revenue vs Previous Month
Absolute difference in revenue compared to previous month.

```dax
Revenue vs Previous Month = 
[Total Revenue] - [Revenue Previous Month]
```

---

## 🛍️ Product Performance Metrics

### Top Category
Dynamically returns the highest revenue-generating product category.

```dax
Top Category = 
CALCULATE(
    FIRSTNONBLANK(dispensary_data_cleaned[product_category], 1),
    TOPN(1, VALUES(dispensary_data_cleaned[product_category]), [Total Revenue], DESC)
)
```

### Top Product
Identifies the best-selling product by revenue.

```dax
Top Product = 
CALCULATE(
    FIRSTNONBLANK(dispensary_data_cleaned[product_name], 1),
    TOPN(1, VALUES(dispensary_data_cleaned[product_name]), [Total Revenue], DESC)
)
```

### Category Revenue Percentage
Calculates each category's contribution to total revenue.

```dax
Category Revenue % = 
DIVIDE(
    [Total Revenue],
    CALCULATE([Total Revenue], ALL(dispensary_data_cleaned[product_category])),
    0
)
```

---

## 🗺️ Regional Performance Metrics

### Top State
Returns the state with the highest revenue.

```dax
Top State = 
CALCULATE(
    FIRSTNONBLANK(dispensary_data_cleaned[customer_location_state], 1),
    TOPN(1, VALUES(dispensary_data_cleaned[customer_location_state]), [Total Revenue], DESC)
)
```

### Top City
Identifies the city generating the most revenue.

```dax
Top City = 
CALCULATE(
    FIRSTNONBLANK(dispensary_data_cleaned[customer_location_city], 1),
    TOPN(1, VALUES(dispensary_data_cleaned[customer_location_city]), [Total Revenue], DESC)
)
```

---

## 🔍 Advanced Analytics

### Customer Segmentation
Dynamically segments customers based on purchase frequency.

```dax
Customer Count by Segment = 
SWITCH(
    TRUE(),
    CALCULATE(COUNTROWS(dispensary_data_cleaned)) = 1, "One-time",
    CALCULATE(COUNTROWS(dispensary_data_cleaned)) <= 3, "Occasional",
    CALCULATE(COUNTROWS(dispensary_data_cleaned)) <= 10, "Regular",
    "VIP"
)
```

### Average Days Between Purchases
Calculates the average time gap between consecutive customer purchases.

```dax
Avg Days Between Purchases = 
VAR CustomerPurchases = 
    ADDCOLUMNS(
        SUMMARIZE(
            dispensary_data_cleaned,
            dispensary_data_cleaned[customer_id],
            dispensary_data_cleaned[transaction_date]
        ),
        "PrevDate", 
        CALCULATE(
            MAX(dispensary_data_cleaned[transaction_date]),
            FILTER(
                ALL(dispensary_data_cleaned),
                dispensary_data_cleaned[customer_id] = EARLIER(dispensary_data_cleaned[customer_id]) &&
                dispensary_data_cleaned[transaction_date] < EARLIER(dispensary_data_cleaned[transaction_date])
            )
        )
    )
RETURN
    AVERAGEX(
        FILTER(CustomerPurchases, NOT(ISBLANK([PrevDate]))),
        DATEDIFF([PrevDate], [transaction_date], DAY)
    )
```

---

## 📋 Calculated Columns

### Customer Lifetime Value Bucket
Segments customers into LTV tiers for analysis.

```dax
LTV Bucket = 
VAR CustomerLTV = 
    CALCULATE(
        SUM(dispensary_data_cleaned[total_amount]),
        ALLEXCEPT(dispensary_data_cleaned, dispensary_data_cleaned[customer_id])
    )
RETURN
    SWITCH(
        TRUE(),
        CustomerLTV < 100, "$0-$100",
        CustomerLTV < 300, "$100-$300",
        CustomerLTV < 500, "$300-$500",
        CustomerLTV < 1000, "$500-$1000",
        "$1000+"
    )
```

### Customer Segment
Categorizes customers based on their total purchase count.

```dax
Customer Segment = 
VAR PurchaseCount = 
    CALCULATE(
        COUNTROWS(dispensary_data_cleaned),
        ALLEXCEPT(dispensary_data_cleaned, dispensary_data_cleaned[customer_id])
    )
RETURN
    SWITCH(
        TRUE(),
        PurchaseCount = 1, "One-time",
        PurchaseCount <= 3, "Occasional",
        PurchaseCount <= 10, "Regular",
        "VIP"
    )
```

### Revenue Tier
Classifies transactions by revenue range.

```dax
Revenue Tier = 
SWITCH(
    TRUE(),
    dispensary_data_cleaned[total_amount] < 20, "Low (<$20)",
    dispensary_data_cleaned[total_amount] < 40, "Medium ($20-$40)",
    dispensary_data_cleaned[total_amount] < 60, "High ($40-$60)",
    "Premium ($60+)"
)
```

### Transaction Hour Category
Segments transactions by time of day.

```dax
Transaction Hour Category = 
VAR Hour = VALUE(LEFT(dispensary_data_cleaned[transaction_time], 2))
RETURN
    SWITCH(
        TRUE(),
        Hour < 12, "Morning",
        Hour < 17, "Afternoon",
        Hour < 20, "Evening",
        "Night"
    )
```

---

## 📊 Key Insights from DAX Implementation

These DAX measures enable:
- **Real-time KPI tracking** with dynamic calculations
- **Customer segmentation** for targeted marketing strategies
- **Churn analysis** to identify at-risk customers
- **Product performance monitoring** across categories and regions
- **Time-based comparisons** for trend analysis
- **Advanced customer analytics** including LTV and purchase patterns

The measures leverage DAX's context transition, filter manipulation, and time intelligence capabilities to provide actionable business insights from the dispensary transaction data.
