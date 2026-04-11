# Customer Retention & Churn Analysis
> A full end-to-end customer churn analysis project built with Python and Power BI

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow)
![Status](https://img.shields.io/badge/Status-Complete-green)

---

## Project Overview

This project analyzes customer churn for a telecom subscription business
using the Telco Customer Churn dataset (7,043 customers). The goal is to
identify why customers leave, which segments are most at risk, how long
customers stay, and what actions can reduce churn and protect revenue.

**Key Finding:** 26.54% of customers churn, representing $2.86M in lost
revenue — concentrated in month-to-month contracts and first-year customers.

---

## Project Structure
FUTURE_DS_02/
│
├── src/
│   ├── load_clean.py           # Data loading & cleaning pipeline
│   ├── churn_metrics.py        # Churn rate calculations & charts
│   ├── cohort_analysis.py      # Cohort & retention analysis
│   ├── segmentation.py         # Customer segmentation
│   ├── lifetime_value.py       # LTV analysis
│   └── export_for_powerbi.py   # Export clean data to Excel
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_churn_analysis.ipynb
│   ├── 03_cohort_retention.ipynb
│   └── 04_segmentation.ipynb
│
├── data/
│   ├── raw/                    # Original Kaggle CSV (not tracked)
│   └── processed/              # Cleaned & exported data (not tracked)
│
├── reports/
│   ├── figures/                # All saved charts & plots
│   └── summary.md              # Full insights & recommendations
│
├── powerbi/                    # Power BI dashboard (.pbix)
├── requirements.txt
├── setup.py
└── README.md

---

## Dataset

**Telco Customer Churn Dataset**
- Source: [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- Records: 7,043 customers
- Features: 21 columns including demographics, services, contract, and churn status

> Download the dataset from Kaggle and place it in `data/raw/`

---

## Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/bennedictbett/FUTURE_DS_02.git
cd FUTURE_DS_02
```

**2. Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Download the dataset**
- Go to https://www.kaggle.com/datasets/blastchar/telco-customer-churn
- Download and place `WA_Fn-UseC_-Telco-Customer-Churn.csv` in `data/raw/`

---

## How to Run

Run each script in order from the project root:

```bash
# Step 1 — Clean the data
python src/load_clean.py

# Step 2 — Run churn metrics
python src/churn_metrics.py

# Step 3 — Run cohort analysis
python src/cohort_analysis.py

# Step 4 — Run segmentation
python src/segmentation.py

# Step 5 — Run LTV analysis
python src/lifetime_value.py

# Step 6 — Export for Power BI
python src/export_for_powerbi.py
```

Or run the notebooks in order:
```bash
jupyter notebook
```

---

## Key Results

### Churn Overview
| Metric | Value |
|---|---|
| Total Customers | 7,043 |
| Churn Rate | 26.54% |
| Revenue Lost | $2,862,576 |
| Avg LTV | $2,279.58 |

### Top Churn Drivers
| Driver | Churn Rate |
|---|---|
| Month-to-month contract | 42.7% |
| Electronic check payment | 45.3% |
| Fiber optic internet | 41.9% |
| First year customers | 47.4% |

### Risk Segments
| Segment | Customers | Churn Rate | Rev at Risk |
|---|---|---|---|
| Critical Risk | 1,618 | 61.3% | $1,022,942 |
| High Risk | 1,624 | 34.2% | $369,131 |
| Medium Risk | 1,634 | 15.1% | $232,812 |
| Low Risk | 2,167 | 3.4% | $40,520 |

---

## Power BI Dashboard

The dashboard has 4 pages:

| Page | Content |
|---|---|
| Overview | KPI cards, churn by contract, tenure, payment, internet |
| Cohort | Heatmap, retention curves, volume by tenure |
| Segments | Risk, behavior and value segment breakdowns |
| LTV | Lifetime value analysis and revenue at risk |

---

## Top Recommendations

1. **Launch contract upgrade campaign** — target 1,994 New & Flexible
   customers with discounts to switch to annual contracts
2. **Fix first year onboarding** — 47.4% churn in year 1 is the
   biggest single opportunity to reduce overall churn
3. **Investigate fiber optic churn** — 41.9% churn rate needs
   urgent attention through pricing or quality improvements
4. **Incentivize automatic payments** — offer $5/mo discount to
   move electronic check customers to auto-pay
5. **Proactive outreach to Critical Risk** — 1,618 customers
   represent $1.02M annual revenue at risk

---

## Tools & Technologies

| Tool | Purpose |
|---|---|
| Python 3.13 | Data cleaning, analysis, visualization |
| Pandas | Data manipulation |
| Matplotlib / Seaborn | Charts and figures |
| Scikit-learn | Risk scoring |
| Jupyter Notebook | Interactive analysis |
| Power BI | Dashboard and reporting |
| Git / GitHub | Version control |

---

## Author

**Bennedick Bett**
- GitHub: [@bennedictbett](https://github.com/bennedictbett)

---

## License

This project is for educational purposes as part of a Data Science
internship program.