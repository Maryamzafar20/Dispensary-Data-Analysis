# 🌿 Dispensary Data Analysis Project

A comprehensive end-to-end data analysis project examining customer behavior, product performance, and regional demand patterns in the cannabis dispensary industry.

---

## 📊 Project Overview

This project demonstrates advanced data analytics capabilities through a complete analysis workflow: from data collection and cleaning to exploratory analysis, SQL queries, and interactive Power BI dashboards. The analysis provides actionable insights into customer churn, regional sales performance, and product trends.

**Key Business Questions Addressed:**
- What is the customer churn rate and which segments are most at risk?
- Which regions and cities generate the highest revenue?
- What are the top-performing product categories and individual products?
- How do sales trends vary over time and by day of week?
- What is the customer lifetime value and how does it vary by segment?

---

## 🎯 Key Insights & Findings

### Business Performance
- **Total Revenue:** $582,907.96 across 18 months
- **Customer Base:** 1,042 unique customers with 96.8% repeat rate
- **Average Transaction Value:** $41.58
- **Transaction Volume:** 14,018 completed transactions

### Customer Behavior
- **Churn Rate:** 35.03% (365 churned customers using 90-day threshold)
- **Retention Rate:** 64.97% active customers
- **Customer Lifetime Value:** $559.41 average
- **VIP Customers:** 601 customers with 10+ purchases generating $474K revenue

### Regional Performance
- **Top State:** California ($177,345.13 revenue)
- **Top City:** Seattle ($61,599.72 revenue)
- **Product Preferences:** Concentrates lead in CA (27.2%), Vapes in AZ (21.1%)

### Product Insights
- **Top Category:** Concentrates (25.8% of revenue)
- **Best-Selling Product:** Rosin 1g ($34,494.84 revenue)
- **Most Popular:** CBD Lotion 100mg (748 units sold)

---

## 📸 Dashboard Visualizations

### Executive Overview
Comprehensive KPI dashboard showing revenue trends, customer metrics, and top-performing regions.

![Executive Overview](images/Executive%20Overview.png)

### Customer Churn Analysis
Deep dive into customer retention, churn rates by segment, and lifetime value distribution.

![Customer Churn](images/Customer%20Churn.png)

### Regional Demand Analysis
Geographic performance breakdown with state-level revenue and product category preferences.

![Regional Demand](images/Regional%20Demand.png)

### Product Performance
Category trends, top products, and sales performance over time.

![Product Performance](images/Product%20Performance.png)

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| **Python** | Data cleaning, transformation, and exploratory analysis |
| **Pandas** | Data manipulation and statistical analysis |
| **SQL** | Advanced querying and data aggregation |
| **Power BI** | Interactive dashboard creation and visualization |
| **DAX** | Custom measures and calculated columns |

---

## 📁 Project Structure

```
dispensary-data-analysis/
├── data/
│   ├── raw/                          # Original transaction data
│   │   └── dispensary_transactions.csv
│   └── cleaned/                      # Processed and validated data
│       └── dispensary_data_cleaned.csv
├── analysis/
│   ├── data_cleaning.py              # Data cleaning and validation script
│   └── exploratory_analysis.py       # Statistical analysis and KPI calculations
├── sql/
│   └── analysis_queries.sql          # 25+ SQL queries for business analysis
├── powerbi/
│   ├── Dispensary Data Analysis.pbix # Interactive Power BI dashboard
│   └── DAX_Measures.md               # Documentation of DAX measures
├── images/                           # Dashboard screenshots
│   ├── Executive Overview.png
│   ├── Customer Churn.png
│   ├── Regional Demand.png
│   └── Product Performance.png
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

---

## 📋 Methodology

### 1. Data Collection & Preparation
- **Dataset:** 14,258 transactions over 18 months (July 2024 - January 2026)
- **Coverage:** 1,042 unique customers across 10 cities in 6 states
- **Product Range:** 6 categories, 33 unique products

### 2. Data Cleaning Process
Comprehensive data quality improvements:
- ✅ Removed 240 duplicate transactions (1.7%)
- ✅ Standardized date formats (3 different formats unified)
- ✅ Normalized location data (city/state naming inconsistencies)
- ✅ Imputed 1,683 missing values using statistical methods
- ✅ Validated transaction calculations (fixed 726 discrepancies)
- ✅ Created 7 derived fields for enhanced analysis

**Key Transformations:**
```python
# Date standardization
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

# Customer metrics
df['days_since_first_purchase'] = (df['transaction_date'] - df['customer_first_purchase_date']).dt.days

# Time-based features
df['transaction_month'] = df['transaction_date'].dt.month
df['day_of_week'] = df['transaction_date'].dt.day_name()
```

### 3. Exploratory Data Analysis
Performed comprehensive statistical analysis covering:
- Revenue and transaction trends (monthly, quarterly, day-of-week)
- Customer segmentation (One-time, Occasional, Regular, VIP)
- Churn analysis using 90-day inactivity threshold
- Product performance across categories and regions
- Payment method preferences
- Customer lifetime value distribution

### 4. SQL Analytics
Developed 25+ production-ready SQL queries organized into:
- Business KPIs and metrics
- Customer retention and churn analysis
- Regional demand patterns
- Product performance tracking
- Time-based trend analysis
- Cohort and RFM analysis
- Advanced cross-sell insights

### 5. Power BI Dashboard
Built a 4-page interactive dashboard featuring:
- **Executive Overview:** High-level KPIs, revenue trends, category breakdown
- **Customer Churn:** Retention metrics, segment analysis, LTV distribution
- **Regional Demand:** Geographic heatmap, city rankings, regional preferences
- **Product Performance:** Category trends, top products, inventory insights

**DAX Highlights:**
- 20+ custom measures for dynamic calculations
- Time intelligence functions for YTD and growth metrics
- Customer segmentation logic with iterators
- Advanced filtering using CALCULATE and FILTER functions

---

## 🔍 Detailed Analysis Results

### Customer Segmentation

| Segment | Customers | Avg Purchases | Total Revenue | Avg LTV |
|---------|-----------|---------------|---------------|---------|
| VIP | 601 | 19.00 | $474,397.94 | $789.35 |
| Regular | 342 | 7.01 | $100,908.91 | $295.06 |
| Occasional | 66 | 2.53 | $6,284.42 | $95.22 |
| One-time | 33 | 1.00 | $1,316.69 | $39.90 |

### Churn Analysis by Demographics

**By Age Group:**
- 18-25: 33.46% churn rate (254 customers)
- 26-35: 35.00% churn rate (180 customers)
- 36-45: 36.45% churn rate (214 customers)
- 46-55: 36.89% churn rate (206 customers)
- 56+: 33.51% churn rate (188 customers)

**By Membership Tier:**
- Platinum: 38.74% churn (highest risk!)
- Silver: 40.93% churn
- Gold: 33.22% churn
- Standard: 29.21% churn (best retention)

### Product Category Performance

| Category | Revenue | Revenue % | Units Sold |
|----------|---------|-----------|------------|
| Concentrates | $150,108.83 | 25.75% | 2,905 |
| Flower | $114,724.64 | 19.68% | 2,884 |
| Vapes | $109,269.09 | 18.75% | 3,024 |
| Topicals | $104,147.33 | 17.87% | 2,861 |
| Edibles | $58,640.01 | 10.06% | 2,940 |
| Accessories | $46,018.06 | 7.89% | 2,884 |

### Top 10 Products by Revenue

1. Rosin 1g - $34,494.84
2. Distillate 1g - $34,213.31
3. Massage Oil 200mg - $31,405.68
4. CBD Lotion 100mg - $29,878.12
5. Live Resin Cart 0.5g - $28,498.92
6. Live Resin 1g - $28,287.19
7. Wax 1g - $27,972.27
8. THC Balm 200mg - $26,200.72
9. Shatter 1g - $25,141.22
10. Sativa Cart 0.5g - $21,908.88

---

## 💡 Business Recommendations

### 1. Address Platinum Member Churn
- **Issue:** 38.74% churn rate among highest-tier members
- **Action:** Implement VIP retention program with exclusive perks
- **Impact:** Retaining 10% more Platinum members could add ~$14K annual revenue

### 2. Expand High-Performing Categories
- **Insight:** Concentrates generate 25.8% of revenue
- **Action:** Increase product variety and promote premium concentrates
- **Opportunity:** Cross-sell with vapes (complementary products)

### 3. Regional Marketing Strategy
- **California Opportunity:** Largest market ($177K) with room to grow
- **Seattle Focus:** Highest per-city revenue - replicate success model
- **State-Specific Campaigns:** Tailor product mix to regional preferences

### 4. Customer Engagement Program
- **Target:** 96.8% repeat rate is strong, focus on increasing purchase frequency
- **Strategy:** Implement loyalty rewards for 10+ purchases (VIP tier)
- **Goal:** Convert Regular customers (342) to VIP status

### 5. Product Bundling
- **Analysis:** CBD topicals are volume leaders but lower revenue
- **Action:** Bundle topicals with higher-margin concentrates
- **Benefit:** Increase average transaction value from $41.58 to $50+

---

## 📊 Dataset Information

**Source:** Synthetic dataset created for demonstration  
**Time Period:** July 2024 - January 2026 (18 months)  
**Records:** 14,018 transactions after cleaning  
**Customers:** 1,042 unique customers  
**Locations:** 10 cities across 6 states (CA, AZ, CO, WA, NV, OR)  
**Products:** 33 products across 6 categories  

**Key Fields:**
- Transaction details (ID, date, time, amount)
- Customer demographics (ID, age group, location, membership tier)
- Product information (category, name, quantity, price)
- Derived metrics (LTV, churn status, purchase frequency)

---
