# A/B Testing & Statistical Significance Analysis for Conversion Rate Optimization

## 📊 Project Overview

This project evaluates an A/B test for an e-commerce checkout experience to determine whether a new Variant checkout flow improves conversion rate, revenue, and Average Order Value (AOV) compared with the existing Control experience.

The project follows an end-to-end data analytics workflow using Python, SQL, PostgreSQL, statistical hypothesis testing, bootstrap validation, and Power BI.

---

## 🎯 Business Problem

An e-commerce company introduced a new checkout experience and wants to determine whether the new experience improves customer conversion and revenue performance.

The analysis evaluates:

- Conversion Rate
- Conversion Lift
- Statistical Significance
- Average Order Value
- Revenue per Session
- Cart Abandonment
- Experiment Randomization
- Customer Segments

---

## ❓ Business Questions

1. Does the Variant checkout experience increase conversion rate?
2. Is the observed conversion-rate difference statistically significant?
3. Does the Variant increase Average Order Value?
4. Is the AOV difference statistically significant?
5. Was the experiment properly randomized?
6. How does performance vary by device, traffic source, and country?
7. What business insights can be derived from the experiment?

---

## 🔬 Experiment Design

| Parameter | Value |
|---|---:|
| Experiment Groups | Control vs Variant |
| Allocation | 50% / 50% |
| Total Sessions | 150,000 |
| Significance Level (α) | 0.05 |
| Statistical Power | 80% |
| Beta (β) | 0.20 |
| Minimum Detectable Effect | 2% |

### Control

Existing checkout experience.

### Variant

New checkout experience being evaluated.

---

## 🧹 Data Preparation

The project initially generated approximately 150,050 session records.

Data preparation included:

- Duplicate removal
- Missing-value checks
- Data-type validation
- Experiment-group validation
- Conversion validation
- Revenue validation

After cleaning:

| Group | Sessions |
|---|---:|
| Control | 75,000 |
| Variant | 75,000 |
| Total | 150,000 |

---

## 🧪 Sample Ratio Mismatch (SRM)

A Chi-Square Goodness-of-Fit test was used to validate whether the experiment followed the expected 50/50 allocation.

### Result

| Metric | Result |
|---|---:|
| Control Sessions | 75,000 |
| Variant Sessions | 75,000 |
| Expected Split | 50% / 50% |
| Chi-Square Statistic | 0 |
| p-value | 1.0000 |

The observed allocation matches the expected allocation, so there is no evidence of Sample Ratio Mismatch in this experiment.

---

## 📈 Conversion Rate Analysis

| Metric | Control | Variant |
|---|---:|---:|
| Sessions | 75,000 | 75,000 |
| Conversions | 3,150 | 3,281 |
| Conversion Rate | 4.20% | 4.37% |

### Conversion Lift

Absolute Lift:

**+0.1747 percentage points**

Relative Lift:

**+4.16%**

The Variant has a higher observed conversion rate than the Control.

---

## 📊 Statistical Significance Test

A two-sample, two-tailed Z-test for proportions was used to evaluate the conversion-rate difference.

### Hypotheses

**H₀:** There is no difference in conversion rates between Control and Variant.

**H₁:** There is a difference in conversion rates between Control and Variant.

### Results

| Metric | Result |
|---|---:|
| Z-statistic | 1.6697 |
| p-value | 0.09497 |
| Significance Level | 0.05 |
| 95% CI Lower | -0.0304% |
| 95% CI Upper | +0.3797% |

The p-value is greater than 0.05, so the observed conversion-rate difference is not statistically significant at the 5% significance level.

The confidence interval also crosses zero.

---

## 💰 Revenue Analysis

| Metric | Control | Variant |
|---|---:|---:|
| Total Revenue | $329,667.01 | $359,760.86 |
| AOV | $104.66 | $109.65 |
| Revenue / Session | $4.40 | $4.80 |

The Variant generated higher observed revenue, AOV, and revenue per session in the experiment dataset.

These observed differences should be interpreted together with statistical testing.

---

## 🛒 Average Order Value Analysis

A Welch Two-Sample t-test was used to compare Average Order Value between converted users in the Control and Variant groups.

| Metric | Result |
|---|---:|
| Control AOV | $104.66 |
| Variant AOV | $109.65 |
| AOV Difference | +$4.99 |
| Relative Difference | +4.77% |
| t-statistic | 1.7983 |
| p-value | 0.07217 |

The observed AOV difference is not statistically significant at the 5% significance level.

---

## 🔁 Bootstrap Validation

Bootstrap resampling was performed using 10,000 bootstrap samples.

### Conversion Rate Difference

95% Bootstrap Confidence Interval:

**[-0.0307%, +0.3787%]**

### AOV Difference

95% Bootstrap Confidence Interval:

**[-$0.44, +$10.54]**

Both confidence intervals include zero, consistent with the hypothesis-test results.

---

## 📱 Segment Analysis

Experiment performance was analyzed across:

### Device Type

- Desktop
- Mobile
- Tablet

### Traffic Source

Conversion performance was compared across traffic acquisition channels.

### Country

Conversion performance was compared across geographic segments.

These analyses help identify differences in experiment performance across customer segments.

---

## 🗄️ PostgreSQL Analysis

The cleaned experiment dataset was loaded into PostgreSQL.

### Database

`ab_testing_db`

### Main Table

`experiment_sessions`

### Analysis View

`experiment_daily_summary`

SQL analysis includes:

- Experiment-group performance
- Conversion rate
- Conversion lift
- Device-level conversion
- Traffic-source conversion
- Country-level conversion
- Revenue analysis
- AOV analysis
- Cart abandonment
- Daily experiment performance

---

## 📊 Power BI Dashboard

The project includes an interactive Power BI dashboard:

**A/B Testing & Conversion Rate Optimization Dashboard**

### Page 1 — Executive Overview

The Executive Overview page contains:

- Total Sessions KPI
- Total Conversions KPI
- Conversion Rate KPI
- Total Revenue KPI
- AOV KPI
- Experiment Group slicer
- Device Type slicer
- Traffic Source slicer
- Country slicer
- Experiment Date slicer
- Conversion Rate — Control vs Variant
- Daily Conversion Rate Trend

### Page 2 — Detailed Analysis

The Detailed Analysis page contains:

- Conversion Rate by Device
- Conversion Rate by Traffic Source
- Revenue by Experiment Group
- Average Order Value — Control vs Variant
- Conversion Rate by Country
- Relative Lift
- AOV Difference
- Revenue per Session
- Key experiment insights

---

## 🔄 Project Workflow

```text
Raw Data
   ↓
Data Cleaning
   ↓
Data Validation
   ↓
Sample Ratio Mismatch Check
   ↓
Exploratory Analysis
   ↓
Conversion Rate Analysis
   ↓
Hypothesis Testing
   ↓
AOV Analysis
   ↓
Bootstrap Validation
   ↓
Business Impact Analysis
   ↓
PostgreSQL Analysis
   ↓
Power BI Dashboard
   ↓
Business Interpretation


📁 Project Structure

ab-testing-conversion-analysis/
│
├── data/
│   ├── raw/
│   │   └── raw_sessions.csv
│   │
│   └── processed/
│       └── cleaned_experiment_data.csv
│
├── notebooks/
│   ├── 01_data_cleaning_srm_check.py
│   └── 02_hypothesis_testing_bootstrapping.py
│
├── sql/
│   ├── 01_create_database.sql
│   ├── 02_create_table.sql
│   └── 03_extract_experiment_metrics.sql
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── generate_data.py
│   ├── data_cleaning.py
│   ├── srm_check.py
│   ├── hypothesis_testing.py
│   ├── bootstrap.py
│   └── run_pipeline.py
│
├── outputs/
│   ├── figures/
│   ├── experiment_summary.csv
│   ├── srm_results.csv
│   ├── hypothesis_results.csv
│   ├── bootstrap_results.csv
│   └── business_impact.csv
│
├── dashboard/
│   ├── AB_Testing_Conversion_Analysis.pbix
│   ├── powerbi_measures.dax
│   ├── dashboard_page1.png
│   └── dashboard_page2.png
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt

## 🎯 Skills Demonstrated

### 📊 Data Analytics

- Data cleaning
- Data validation
- Exploratory data analysis
- KPI calculation
- Customer segmentation
- Business metric analysis

### 🗄️ SQL

- SELECT
- WHERE
- GROUP BY
- ORDER BY
- Aggregations
- CASE WHEN
- Conditional aggregation
- Common Table Expressions (CTEs)
- PostgreSQL views
- Date-based analysis

### 📈 Statistics

- A/B testing
- Hypothesis testing
- Conversion rate testing
- Z-test for proportions
- Welch's t-test
- Chi-Square test
- Confidence intervals
- Statistical significance
- Bootstrap validation
- Sample Ratio Mismatch (SRM) detection

### 🐍 Python

- Pandas
- NumPy
- SciPy
- Statsmodels
- Matplotlib
- Seaborn
- Modular Python project structure

### 📊 Power BI

- Power BI dashboards
- DAX measures
- KPI cards
- Slicers
- Interactive charts
- Trend analysis
- Segment analysis
- Business reporting

### 💻 Portfolio & Engineering

- Git
- GitHub
- Reproducible analysis
- Project organization
- End-to-end analytics workflow
- Business problem solving


## ⭐ Project Highlights

- Analyzed **150,000 experiment sessions**
- Built an end-to-end A/B testing workflow
- Performed data cleaning and validation
- Performed Sample Ratio Mismatch (SRM) testing
- Calculated Control vs Variant conversion performance
- Calculated absolute and relative conversion lift
- Performed statistical significance testing
- Conducted revenue analysis
- Analyzed Average Order Value (AOV)
- Performed 10,000 bootstrap simulations
- Performed device-level analysis
- Performed traffic-source analysis
- Performed country-level analysis
- Stored and analyzed data using PostgreSQL
- Created reusable SQL analysis views
- Built an interactive Power BI dashboard
- Created business-focused KPIs
- Created statistical analysis outputs
- Documented the complete end-to-end project

---

## ▶️ How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/arnojivivekvardhan22/ab-testing-conversion-analysis.git


### 2. Open the Project

cd ab-testing-conversion-analysis

### 3. Create a Virtual Environment

python -m venv .venv

### 4. Activate the Virtual Environment
Windows
.venv\Scripts\activate

### 5. Install Dependencies
pip install -r requirements.txt

### 6. Run the Complete Python Pipeline
python -m src.run_pipeline

## 🐘 PostgreSQL SQL Analysis

PostgreSQL was used to store and analyze the cleaned experiment dataset.

### Database

`ab_testing_db`

### Main Table

`experiment_sessions`

### Records

`150,000`

### SQL Analysis Performed

- Experiment group performance
- Conversion rate analysis
- Conversion lift analysis
- Device analysis
- Traffic-source analysis
- Country analysis
- Revenue analysis
- AOV analysis
- Cart abandonment analysis
- Daily experiment performance
- Conditional aggregations
- Common Table Expressions
- PostgreSQL views

### PostgreSQL Analysis View

A reusable view was created:

`experiment_daily_summary`

The view contains:

- Session date
- Experiment group
- Sessions
- Conversions
- Conversion rate
- Total revenue
- AOV
- Revenue per session
- Cart abandonment rate

---

## 📊 Power BI Dashboard

The project includes an interactive Power BI dashboard:

**A/B Testing & Conversion Rate Optimization Dashboard**

Power BI file:

`dashboard/AB_Testing_Conversion_Analysis.pbix`

### Page 1 — Executive Overview

Dashboard title:

**A/B TESTING & CONVERSION RATE OPTIMIZATION**

Subtitle:

**Executive Overview | Control vs Variant Performance**

The page contains:

- Total Sessions KPI
- Total Conversions KPI
- Conversion Rate KPI
- Total Revenue KPI
- AOV KPI
- Experiment Group slicer
- Device Type slicer
- Traffic Source slicer
- Country slicer
- Experiment Date slicer
- Conversion Rate — Control vs Variant
- Daily Conversion Rate Trend

### Page 2 — Detailed Analysis

Dashboard title:

**A/B TESTING & CONVERSION RATE OPTIMIZATION**

Subtitle:

**Detailed Analysis | Segment, Revenue & Experiment Performance**

The page contains:

- Conversion Rate by Device
- Conversion Rate by Traffic Source
- Revenue by Experiment Group
- Average Order Value — Control vs Variant
- Conversion Rate by Country
- Relative Lift
- AOV Difference
- Revenue Per Session
- Statistical Significance
- Key Insights

---

## 🔄 Project Workflow

```text
Raw Data
    ↓
Data Generation / Data Collection
    ↓
Data Cleaning
    ↓
Data Validation
    ↓
Sample Ratio Mismatch Check
    ↓
Exploratory Data Analysis
    ↓
Conversion Rate Analysis
    ↓
Statistical Hypothesis Testing
    ↓
Revenue Analysis
    ↓
AOV Analysis
    ↓
Bootstrap Validation
    ↓
Segment Analysis
    ↓
PostgreSQL SQL Analysis
    ↓
Power BI Dashboard
    ↓
Business Interpretation


## Author

**Arnoji Vivek Vardhan**  
Aspiring Data Analyst | AI Engineer

- GitHub: `Arnoji-Vivek-Vardhan`
- Skills: Python, SQL, PostgreSQL, Statistics, Power BI, Data Analytics
- Focus: Data Analytics, A/B Testing, Business Intelligence & AI Engineering