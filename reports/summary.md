# Customer Retention & Churn Analysis — Summary Report
**Dataset**: Telco Customer Churn (7,043 customers)  
**Tools**: Python (VS Code) · Power BI  
**Author**: Bennedick Bett  
**Date**: March 2026

---

## 1. Project Overview

This report presents a full customer retention and churn analysis for a 
telecom subscription business. The goal was to identify why customers leave, 
which segments are most at risk, how long customers typically stay, and what 
actions can reduce churn and protect revenue.

---

## 2. Key Metrics at a Glance

| Metric | Value |
|---|---|
| Total Customers | 7,043 |
| Churned Customers | 1,869 (26.54%) |
| Retained Customers | 5,174 (73.46%) |
| Avg Monthly Charge | $64.76 |
| Avg Customer Tenure | 32.4 months |
| Avg Lifetime Value | $2,279.58 |
| Total Revenue | $16,055,091 |
| Revenue Lost to Churn | $2,862,576 (17.8%) |

---

## 3. Churn Analysis Findings

### 3.1 Contract Type
Contract type is the single strongest predictor of churn.

| Contract | Customers | Churn Rate |
|---|---|---|
| Month-to-month | 3,875 | 42.7% |
| One year | 1,473 | 11.3% |
| Two year | 1,695 | 2.8% |

- Month-to-month customers churn at **15x the rate** of two-year customers
- Converting a customer from month-to-month to two-year adds **$2,336 in LTV**

### 3.2 Tenure Band
Churn drops significantly the longer a customer stays.

| Tenure Band | Customers | Churn Rate |
|---|---|---|
| 0–12 mo | 2,186 | 47.4% |
| 13–24 mo | 1,024 | 28.7% |
| 25–36 mo | 832 | 21.6% |
| 37–48 mo | 762 | 19.0% |
| 49–60 mo | 832 | 14.4% |
| 61–72 mo | 1,407 | 6.6% |

- Nearly **1 in 2 new customers** leaves within the first year
- Customers past **5 years** churn at only 6.6%

### 3.3 Internet Service
| Service | Churn Rate |
|---|---|
| Fiber optic | 41.9% |
| DSL | 19.0% |
| No internet | 7.4% |

- Fiber optic customers churn at **2x the rate** of DSL customers
- Likely driven by high monthly charges and competition

### 3.4 Payment Method
| Payment Method | Churn Rate |
|---|---|
| Electronic check | 45.3% |
| Mailed check | 19.1% |
| Bank transfer | 16.7% |
| Credit card | 15.2% |

- Electronic check customers churn at **3x the rate** of automatic payment customers
- Automatic payments strongly correlate with lower churn

---

## 4. Cohort Analysis Findings

### 4.1 Retention Heatmap — Tenure x Contract

| Tenure Band | Month-to-month | One year | Two year |
|---|---|---|---|
| 0–12 mo | 51.4% | 10.5% | 0.0% |
| 13–24 mo | 37.7% | 8.1% | 0.0% |
| 25–36 mo | 32.5% | 8.0% | 2.1% |
| 37–48 mo | 33.5% | 13.1% | 2.2% |
| 49–60 mo | 27.8% | 13.7% | 4.0% |
| 61–72 mo | 22.2% | 12.1% | 3.1% |

Key finding: Two-year contract customers show **0% churn** in the first 
24 months — the strongest retention cohort in the entire dataset.

### 4.2 Retention Curve
- Month-to-month retention improves from 48.6% → 77.8% over 6 years
- Two-year retention stays above 96% across all tenure bands
- The gap between contract types **never closes** — early contract 
  type determines long-term retention

---

## 5. Segmentation Findings

### 5.1 Risk Segments
| Segment | Customers | Churn Rate | Annual Rev at Risk |
|---|---|---|---|
| Critical Risk | 1,618 | 61.3% | $1,022,942 |
| High Risk | 1,624 | 34.2% | $369,131 |
| Medium Risk | 1,634 | 15.1% | $232,812 |
| Low Risk | 2,167 | 3.4% | $40,520 |

- **1,618 Critical Risk customers** are the immediate priority
- Combined Critical + High Risk = **$1.39M annual revenue at risk**

### 5.2 Behavior Segments
| Segment | Customers | Churn Rate |
|---|---|---|
| New & Flexible | 1,994 | 51.4% |
| Established & Flexible | 1,881 | 33.6% |
| Committed (1yr) | 1,473 | 11.3% |
| Loyal (2yr) | 1,695 | 2.8% |

### 5.3 Value Segments
| Segment | Avg LTV | Avg Tenure | Churn Rate |
|---|---|---|---|
| Top Value | $5,713 | 61 months | 14.5% |
| High Value | $2,395 | 39 months | 23.1% |
| Mid Value | $860 | 24 months | 25.6% |
| Low Value | $151 | 4 months | 43.0% |

---

## 6. Lifetime Value Findings

| Metric | Value |
|---|---|
| Avg LTV Retained | $2,549.77 |
| Avg LTV Churned | $1,531.61 |
| LTV Gap | $1,018.16 |
| Two-year Avg LTV | $3,706.76 |
| Month-to-month Avg LTV | $1,370.12 |
| LTV difference | $2,336.64 |

- Retained customers generate **$1,018 more** than churned customers
- Every customer moved from month-to-month to two-year is worth 
  an extra **$2,336 in lifetime revenue**

---

## 7. Recommendations

### 7.1 Convert Month-to-Month Customers — HIGH PRIORITY
- Launch a **contract upgrade campaign** offering discounts or 
  perks for switching to annual or two-year contracts
- Target the **1,994 New & Flexible** customers first — 
  they are in their first year and most likely to churn
- Offer 1–2 months free or a reduced rate for committing to annual

### 7.2 Fix the First Year Experience — HIGH PRIORITY
- The first 12 months have a **47.4% churn rate** — the business 
  is losing nearly half of all new customers in year one
- Implement an **onboarding program** with check-in calls, 
  tutorials, and early engagement campaigns
- Set up automated alerts when a new customer shows low engagement

### 7.3 Investigate Fiber Optic Churn — HIGH PRIORITY
- Fiber optic customers churn at **41.9%** — far above DSL at 19%
- Conduct customer surveys to identify if the issue is pricing, 
  service quality, or competitor offers
- Consider a **fiber optic loyalty discount** for customers 
  past 12 months

### 7.4 Move Customers to Automatic Payments — MEDIUM PRIORITY
- Electronic check customers churn at **45.3%**
- Offer a **small monthly discount** (e.g. $5/mo) for switching 
  to automatic bank transfer or credit card
- Automatic payment customers churn at only 15–17%

### 7.5 Protect Critical Risk Customers — MEDIUM PRIORITY
- **1,618 Critical Risk customers** represent $1.02M annual 
  revenue at risk
- Build a **proactive retention team** that contacts these 
  customers before they churn
- Offer personalized deals based on their usage and tenure

### 7.6 Reward and Protect Top Value Customers — MEDIUM PRIORITY
- **1,761 Top Value customers** generate avg LTV of $5,713
- These customers must never feel neglected
- Implement a **VIP loyalty program** with priority support, 
  exclusive offers, and annual rewards

---

## 8. Expected Impact of Recommendations

| Action | Target Segment | Expected Outcome |
|---|---|---|
| Contract upgrade campaign | 1,994 New & Flexible | Reduce yr1 churn by 15–20% |
| Onboarding program | All new customers | Reduce yr1 churn by 10–15% |
| Fiber optic loyalty discount | 3,096 fiber customers | Reduce fiber churn by 10% |
| Auto payment incentive | 2,365 e-check customers | Reduce payment churn by 20% |
| Critical risk outreach | 1,618 Critical Risk | Save $200–400K annual revenue |
| VIP loyalty program | 1,761 Top Value | Reduce top value churn by 5% |

---

## 9. Conclusion

This analysis reveals that churn in this telecom business is not random — 
it is highly predictable and concentrated in specific segments. 
The three biggest levers to reduce churn are:

1. **Contract type** — moving customers to longer contracts 
   dramatically reduces churn
2. **First year experience** — nearly half of all new customers 
   leave in year one, making onboarding the most critical intervention
3. **Payment method** — automatic payments strongly predict retention 
   and are an easy win through small incentives

Addressing these three areas alone could reduce overall churn from 
**26.54% to below 15%** and recover over **$1M in annual revenue**.

---

*Report generated from Python analysis pipeline · 
Visualized in Power BI · GitHub: github.com/bennedictbett/FUTURE_DS_02*