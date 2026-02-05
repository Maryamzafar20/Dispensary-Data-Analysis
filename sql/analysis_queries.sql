/*
================================================================================
DISPENSARY DATA ANALYSIS - SQL QUERIES
================================================================================
This file contains SQL queries for analyzing dispensary transaction data.
These queries can be used in any SQL database (PostgreSQL, MySQL, SQLite, etc.)
after importing the cleaned CSV data.

Dataset: dispensary_data_cleaned.csv
Table Name: dispensary_transactions (or dispensary_data_cleaned depending on import)
================================================================================
*/

-- ============================================================================
-- 1. OVERALL BUSINESS METRICS
-- ============================================================================

-- Total revenue, transactions, and unique customers
SELECT 
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_transaction_value,
    ROUND(SUM(quantity), 0) AS total_items_sold
FROM dispensary_transactions;


-- Customer purchase frequency distribution
SELECT 
    purchase_frequency,
    COUNT(*) AS customer_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM (
    SELECT 
        customer_id,
        COUNT(*) AS purchase_frequency
    FROM dispensary_transactions
    GROUP BY customer_id
) AS customer_purchases
GROUP BY purchase_frequency
ORDER BY purchase_frequency;


-- ============================================================================
-- 2. CUSTOMER RETENTION & CHURN ANALYSIS
-- ============================================================================

-- Customer retention rate (customers with last purchase in last 90 days)
SELECT 
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT CASE 
        WHEN JULIANDAY('2026-01-31') - JULIANDAY(last_purchase_date) <= 90 
        THEN customer_id 
    END) AS active_customers,
    COUNT(DISTINCT CASE 
        WHEN JULIANDAY('2026-01-31') - JULIANDAY(last_purchase_date) > 90 
        THEN customer_id 
    END) AS churned_customers,
    ROUND(COUNT(DISTINCT CASE 
        WHEN JULIANDAY('2026-01-31') - JULIANDAY(last_purchase_date) <= 90 
        THEN customer_id 
    END) * 100.0 / COUNT(DISTINCT customer_id), 2) AS retention_rate_pct,
    ROUND(COUNT(DISTINCT CASE 
        WHEN JULIANDAY('2026-01-31') - JULIANDAY(last_purchase_date) > 90 
        THEN customer_id 
    END) * 100.0 / COUNT(DISTINCT customer_id), 2) AS churn_rate_pct
FROM (
    SELECT 
        customer_id,
        MAX(transaction_date) AS last_purchase_date
    FROM dispensary_transactions
    GROUP BY customer_id
) AS customer_last_purchase;


-- Churn rate by customer segment
SELECT 
    membership_tier,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT CASE 
        WHEN JULIANDAY('2026-01-31') - JULIANDAY(last_purchase_date) > 90 
        THEN customer_id 
    END) AS churned_customers,
    ROUND(COUNT(DISTINCT CASE 
        WHEN JULIANDAY('2026-01-31') - JULIANDAY(last_purchase_date) > 90 
        THEN customer_id 
    END) * 100.0 / COUNT(DISTINCT customer_id), 2) AS churn_rate_pct
FROM (
    SELECT 
        t.customer_id,
        t.membership_tier,
        MAX(t.transaction_date) AS last_purchase_date
    FROM dispensary_transactions t
    GROUP BY t.customer_id, t.membership_tier
) AS customer_data
GROUP BY membership_tier
ORDER BY churn_rate_pct DESC;


-- Customer lifetime value (LTV) analysis
SELECT 
    customer_id,
    COUNT(*) AS total_purchases,
    ROUND(SUM(total_amount), 2) AS lifetime_value,
    ROUND(AVG(total_amount), 2) AS avg_transaction_value,
    MIN(transaction_date) AS first_purchase_date,
    MAX(transaction_date) AS last_purchase_date,
    JULIANDAY(MAX(transaction_date)) - JULIANDAY(MIN(transaction_date)) AS customer_lifetime_days
FROM dispensary_transactions
GROUP BY customer_id
ORDER BY lifetime_value DESC
LIMIT 20;


-- ============================================================================
-- 3. REGIONAL DEMAND ANALYSIS
-- ============================================================================

-- Revenue and performance by state
SELECT 
    customer_location_state,
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_transaction_value,
    ROUND(SUM(quantity), 0) AS total_items_sold
FROM dispensary_transactions
GROUP BY customer_location_state
ORDER BY total_revenue DESC;


-- Top 10 cities by revenue
SELECT 
    customer_location_city,
    customer_location_state,
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_transaction_value
FROM dispensary_transactions
GROUP BY customer_location_city, customer_location_state
ORDER BY total_revenue DESC
LIMIT 10;


-- Product category preference by top 3 states
SELECT 
    customer_location_state,
    product_category,
    COUNT(*) AS transactions,
    ROUND(SUM(total_amount), 2) AS revenue,
    ROUND(SUM(total_amount) * 100.0 / SUM(SUM(total_amount)) OVER (PARTITION BY customer_location_state), 2) AS revenue_pct
FROM dispensary_transactions
WHERE customer_location_state IN ('CA', 'AZ', 'CO')
GROUP BY customer_location_state, product_category
ORDER BY customer_location_state, revenue DESC;


-- ============================================================================
-- 4. PRODUCT PERFORMANCE ANALYSIS
-- ============================================================================

-- Product category performance
SELECT 
    product_category,
    COUNT(*) AS total_transactions,
    ROUND(SUM(quantity), 0) AS units_sold,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(unit_price), 2) AS avg_unit_price,
    ROUND(SUM(total_amount) * 100.0 / SUM(SUM(total_amount)) OVER (), 2) AS revenue_pct
FROM dispensary_transactions
GROUP BY product_category
ORDER BY total_revenue DESC;


-- Top 10 products by revenue
SELECT 
    product_name,
    product_category,
    COUNT(*) AS transactions,
    ROUND(SUM(quantity), 0) AS units_sold,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(unit_price), 2) AS avg_unit_price
FROM dispensary_transactions
GROUP BY product_name, product_category
ORDER BY total_revenue DESC
LIMIT 10;


-- Top 10 products by quantity sold
SELECT 
    product_name,
    product_category,
    ROUND(SUM(quantity), 0) AS units_sold,
    COUNT(*) AS transactions,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(unit_price), 2) AS avg_unit_price
FROM dispensary_transactions
GROUP BY product_name, product_category
ORDER BY units_sold DESC
LIMIT 10;


-- Product performance by category over time (monthly)
SELECT 
    month_year,
    product_category,
    COUNT(*) AS transactions,
    ROUND(SUM(total_amount), 2) AS revenue
FROM dispensary_transactions
GROUP BY month_year, product_category
ORDER BY month_year, revenue DESC;


-- ============================================================================
-- 5. REVENUE TRENDS & SEASONALITY
-- ============================================================================

-- Monthly revenue trend
SELECT 
    month_year,
    COUNT(*) AS transactions,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(total_amount), 2) AS revenue,
    ROUND(AVG(total_amount), 2) AS avg_transaction_value
FROM dispensary_transactions
GROUP BY month_year
ORDER BY month_year;


-- Monthly revenue growth rate
WITH monthly_revenue AS (
    SELECT 
        month_year,
        ROUND(SUM(total_amount), 2) AS revenue
    FROM dispensary_transactions
    GROUP BY month_year
)
SELECT 
    month_year,
    revenue,
    LAG(revenue) OVER (ORDER BY month_year) AS previous_month_revenue,
    ROUND((revenue - LAG(revenue) OVER (ORDER BY month_year)) * 100.0 / 
          LAG(revenue) OVER (ORDER BY month_year), 2) AS revenue_growth_pct
FROM monthly_revenue
ORDER BY month_year;


-- Quarterly revenue performance
SELECT 
    transaction_year,
    transaction_quarter,
    COUNT(*) AS transactions,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(total_amount), 2) AS revenue,
    ROUND(AVG(total_amount), 2) AS avg_transaction_value
FROM dispensary_transactions
GROUP BY transaction_year, transaction_quarter
ORDER BY transaction_year, transaction_quarter;


-- Performance by day of week
SELECT 
    day_of_week,
    COUNT(*) AS transactions,
    ROUND(SUM(total_amount), 2) AS revenue,
    ROUND(AVG(total_amount), 2) AS avg_transaction_value
FROM dispensary_transactions
GROUP BY day_of_week
ORDER BY 
    CASE day_of_week
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END;


-- Best performing months by revenue
SELECT 
    month_year,
    ROUND(SUM(total_amount), 2) AS revenue,
    COUNT(*) AS transactions,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM dispensary_transactions
GROUP BY month_year
ORDER BY revenue DESC
LIMIT 5;


-- ============================================================================
-- 6. CUSTOMER SEGMENTATION ANALYSIS
-- ============================================================================

-- Customer segmentation by purchase frequency
SELECT 
    CASE 
        WHEN purchase_count = 1 THEN 'One-time'
        WHEN purchase_count BETWEEN 2 AND 3 THEN 'Occasional'
        WHEN purchase_count BETWEEN 4 AND 10 THEN 'Regular'
        ELSE 'VIP'
    END AS customer_segment,
    COUNT(*) AS customers,
    ROUND(AVG(purchase_count), 2) AS avg_purchases,
    ROUND(SUM(total_spent), 2) AS total_revenue,
    ROUND(AVG(total_spent), 2) AS avg_lifetime_value
FROM (
    SELECT 
        customer_id,
        COUNT(*) AS purchase_count,
        SUM(total_amount) AS total_spent
    FROM dispensary_transactions
    GROUP BY customer_id
) AS customer_summary
GROUP BY customer_segment
ORDER BY 
    CASE customer_segment
        WHEN 'One-time' THEN 1
        WHEN 'Occasional' THEN 2
        WHEN 'Regular' THEN 3
        WHEN 'VIP' THEN 4
    END;


-- Performance by age group
SELECT 
    customer_age_group,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(*) AS total_transactions,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_transaction_value,
    ROUND(SUM(total_amount) / COUNT(DISTINCT customer_id), 2) AS avg_revenue_per_customer
FROM dispensary_transactions
GROUP BY customer_age_group
ORDER BY total_revenue DESC;


-- Performance by membership tier
SELECT 
    membership_tier,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(*) AS total_transactions,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_transaction_value,
    ROUND(SUM(total_amount) / COUNT(DISTINCT customer_id), 2) AS avg_revenue_per_customer
FROM dispensary_transactions
GROUP BY membership_tier
ORDER BY 
    CASE membership_tier
        WHEN 'Standard' THEN 1
        WHEN 'Silver' THEN 2
        WHEN 'Gold' THEN 3
        WHEN 'Platinum' THEN 4
    END;


-- High-value customers (top 10% by lifetime value)
WITH customer_ltv AS (
    SELECT 
        customer_id,
        membership_tier,
        customer_age_group,
        COUNT(*) AS purchase_count,
        ROUND(SUM(total_amount), 2) AS lifetime_value
    FROM dispensary_transactions
    GROUP BY customer_id, membership_tier, customer_age_group
)
SELECT 
    customer_id,
    membership_tier,
    customer_age_group,
    purchase_count,
    lifetime_value
FROM customer_ltv
WHERE lifetime_value >= (SELECT PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY lifetime_value) FROM customer_ltv)
ORDER BY lifetime_value DESC;


-- ============================================================================
-- 7. PAYMENT METHOD ANALYSIS
-- ============================================================================

-- Revenue and transactions by payment method
SELECT 
    payment_method,
    COUNT(*) AS total_transactions,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS transaction_pct,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(SUM(total_amount) * 100.0 / SUM(SUM(total_amount)) OVER (), 2) AS revenue_pct,
    ROUND(AVG(total_amount), 2) AS avg_transaction_value
FROM dispensary_transactions
GROUP BY payment_method
ORDER BY total_revenue DESC;


-- ============================================================================
-- 8. COHORT ANALYSIS
-- ============================================================================

-- Monthly cohort retention analysis
WITH customer_cohorts AS (
    SELECT 
        customer_id,
        DATE(customer_first_purchase_date, 'start of month') AS cohort_month,
        DATE(transaction_date, 'start of month') AS transaction_month
    FROM dispensary_transactions
),
cohort_size AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_customers
    FROM customer_cohorts
    GROUP BY cohort_month
),
cohort_activity AS (
    SELECT 
        cohort_month,
        transaction_month,
        COUNT(DISTINCT customer_id) AS active_customers
    FROM customer_cohorts
    GROUP BY cohort_month, transaction_month
)
SELECT 
    ca.cohort_month,
    ca.transaction_month,
    CAST((JULIANDAY(ca.transaction_month) - JULIANDAY(ca.cohort_month)) / 30 AS INTEGER) AS months_since_cohort,
    ca.active_customers,
    cs.cohort_customers,
    ROUND(ca.active_customers * 100.0 / cs.cohort_customers, 2) AS retention_rate_pct
FROM cohort_activity ca
JOIN cohort_size cs ON ca.cohort_month = cs.cohort_month
ORDER BY ca.cohort_month, ca.transaction_month;


-- ============================================================================
-- 9. ADVANCED BUSINESS INSIGHTS
-- ============================================================================

-- Customer purchase patterns: Average days between purchases
WITH customer_purchase_gaps AS (
    SELECT 
        customer_id,
        transaction_date,
        LAG(transaction_date) OVER (PARTITION BY customer_id ORDER BY transaction_date) AS previous_purchase_date,
        JULIANDAY(transaction_date) - JULIANDAY(LAG(transaction_date) OVER (PARTITION BY customer_id ORDER BY transaction_date)) AS days_between_purchases
    FROM dispensary_transactions
)
SELECT 
    customer_id,
    COUNT(*) AS total_purchases,
    ROUND(AVG(days_between_purchases), 1) AS avg_days_between_purchases,
    ROUND(MIN(days_between_purchases), 0) AS min_days_between_purchases,
    ROUND(MAX(days_between_purchases), 0) AS max_days_between_purchases
FROM customer_purchase_gaps
WHERE days_between_purchases IS NOT NULL
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY total_purchases DESC
LIMIT 20;


-- Product cross-sell analysis: Products frequently purchased together
SELECT 
    t1.product_name AS product_1,
    t2.product_name AS product_2,
    COUNT(DISTINCT t1.transaction_id) AS times_purchased_together,
    ROUND(AVG(t1.total_amount + t2.total_amount), 2) AS avg_combined_value
FROM dispensary_transactions t1
JOIN dispensary_transactions t2 
    ON t1.transaction_id = t2.transaction_id 
    AND t1.product_name < t2.product_name
GROUP BY t1.product_name, t2.product_name
HAVING times_purchased_together >= 10
ORDER BY times_purchased_together DESC
LIMIT 20;


-- RFM Analysis (Recency, Frequency, Monetary)
WITH customer_rfm AS (
    SELECT 
        customer_id,
        JULIANDAY('2026-01-31') - JULIANDAY(MAX(transaction_date)) AS recency_days,
        COUNT(*) AS frequency,
        ROUND(SUM(total_amount), 2) AS monetary_value
    FROM dispensary_transactions
    GROUP BY customer_id
)
SELECT 
    customer_id,
    recency_days,
    frequency,
    monetary_value,
    CASE 
        WHEN recency_days <= 30 AND frequency >= 10 AND monetary_value >= 500 THEN 'Champions'
        WHEN recency_days <= 60 AND frequency >= 5 AND monetary_value >= 300 THEN 'Loyal Customers'
        WHEN recency_days <= 90 AND frequency >= 3 THEN 'Potential Loyalists'
        WHEN recency_days <= 30 AND frequency <= 2 THEN 'New Customers'
        WHEN recency_days > 90 AND frequency >= 5 THEN 'At Risk'
        WHEN recency_days > 180 THEN 'Lost'
        ELSE 'Need Attention'
    END AS customer_segment
FROM customer_rfm
ORDER BY monetary_value DESC;


-- ============================================================================
-- END OF SQL QUERIES
-- ============================================================================
