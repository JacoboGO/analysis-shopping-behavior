# Customer Shopping Behavior Analysis — From Raw Data to Executive Dashboard

> End-to-end analytics project: a retail customer dataset is cleaned in Python, stored in PostgreSQL, analyzed with SQL and presented in a Power BI dashboard to identify which customer segments and behaviors drive revenue.

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Business Storytelling (SCQA)](#business-storytelling-scqa)
3. [Project Objectives](#project-objectives)
4. [Tech Stack](#tech-stack)
5. [Dataset](#dataset)
6. [Project Workflow](#project-workflow)
7. [Repository Structure](#repository-structure)
8. [Dashboard Preview](#dashboard-preview)
9. [Key Insights (C→F→I)](#key-insights-cfi)
10. [Business Recommendations](#business-recommendations)
11. [How to Reproduce](#how-to-reproduce)
12. [Future Improvements](#future-improvements)
13. [Lessons Learned](#lessons-learned)
14. [Author](#author)

---

## Executive Summary

- **Problem:** A retailer needs to understand which customers generate revenue, how discounts, subscriptions and shipping options relate to spending, and where the commercial opportunities are.
- **Why it matters:** Discount policy and loyalty programs directly affect margin and retention. Decisions about them should rest on evidence, not intuition.
- **What was built:** A reproducible pipeline: data cleaning and feature preparation in Python, secure loading into PostgreSQL (credentials kept in a `.env` file), ten business queries in SQL and an interactive Power BI dashboard connected to the database.
- **Business value:** The analysis reveals a revenue base concentrated in male customers, a subscription program with no measurable spending premium, and a high reliance on discounts (43% of purchases), each with a concrete next step.

---

## Business Storytelling (SCQA)

- **S (Situation):** The dataset describes 3,900 customers, each with one purchase amount in USD (233,081 USD in total), product, season, shipping type, payment method, subscription status and purchase history.
- **C (Complication):** Revenue is concentrated in one gender segment (67.7%), all subscribers in the data are male, and 43% of purchases carry a discount while subscribers spend about the same as non-subscribers.
- **Q (Question):** Which customer segments and behaviors drive revenue, and where should the business act on subscriptions, discounts and customer retention?
- **A (Answer):** Revenue differences between segments come mainly from customer volume, not from spending per customer. The subscription program shows no spending advantage, discounts are applied even to above-average purchases, and 79.9% of customers are already "Loyal", so growth depends on retention and subscription redesign rather than on onboarding.

---

## Project Objectives

### General Objective
Transform a raw customer shopping dataset into evidence-based insights on segment revenue, discount usage and subscription behavior, delivered through a SQL analysis and an executive Power BI dashboard.

### Specific Objectives
- Profile and clean the dataset (data types, nulls, duplicates, redundant columns, inconsistent names).
- Engineer analytical features (`age_group`, `purchase_frequency_days`).
- Load the processed data into PostgreSQL through a secure, reusable script.
- Answer ten business questions with SQL (aggregations, CTEs, window functions, subqueries).
- Communicate findings with a Power BI dashboard and a Cause → Finding → Impact narrative.

---

## Tech Stack

- **Python:** pandas, SQLAlchemy, psycopg2, python-dotenv
- **Jupyter Notebook** and **VS Code**
- **PostgreSQL** (SQL: CTEs, window functions, subqueries, conditional aggregation)
- **Power BI** (connected to PostgreSQL)
- **Git / Git Bash** and **GitHub** (Conventional Commits)

---

## Dataset

| Attribute | Description |
|-----------|-------------|
| Source | [Add dataset source and license before publishing] |
| Records | 3,900 |
| Features | 18 in the raw file; 19 after processing (1 dropped, 2 created) |
| Time Period | Not available (the dataset has no date field) |
| Granularity | One row per customer (`customer_id` is unique) |

**Data privacy:** the dataset contains no personal identifiers beyond an anonymous `customer_id`. Database credentials are stored in a local `.env` file that is excluded from version control.

### Data dictionary (processed table `customer_behavior`)

| Column | Type | Description |
|--------|------|-------------|
| customer_id | Integer | Unique customer identifier |
| age | Integer | Customer age (18–70) |
| gender | Text | Male / Female |
| item_purchased | Text | Product bought (25 items) |
| category | Text | Clothing, Accessories, Footwear, Outerwear |
| purchase_amount | Integer | Purchase amount in USD (renamed from `Purchase Amount (USD)`) |
| location | Text | US state (50 values) |
| size, color | Text | Product size and color |
| season | Text | Season of the purchase |
| rating | Float | Review rating (renamed from `Review Rating`); 37 nulls (0.95%), not imputed |
| subscription_status | Text | Yes / No |
| shipping_type | Text | Shipping option (6 values) |
| discount_applied | Text | Yes / No |
| previous_purchases | Integer | Number of previous purchases |
| payment_method | Text | Payment method (6 values) |
| frequency_of_purchases | Text | Declared purchase frequency (7 values) |
| purchase_frequency_days | Integer | **Created:** frequency converted to days (e.g. Weekly = 7, Quarterly = 90) |
| age_group | Category | **Created:** age quartiles: Young Adult (18–31), Adult (32–44), Middle-aged (45–57), Senior (58–70) |

**Transformations applied:**
- Column names normalized to `snake_case`.
- `promo_code_used` dropped: it was identical to `discount_applied` in 100% of rows (redundant).
- `Bi-Weekly` and `Fortnightly` are both mapped to 14 days (assumption: every two weeks).
- No exact duplicate rows were found.

---

## Project Workflow

```text
Raw CSV → Data Understanding (EDA) → Cleaning and Feature Engineering (Python)
→ Load to PostgreSQL (.env) → SQL Analysis (10 queries)
→ Power BI Dashboard → Business Insights → Recommendations
```

---

## Repository Structure

```text
analysis-shopping-behavior/
├── dashboards/
│   └── power-bi/
│       └── customer_behavior_dashboard.pbix
├── data/
│   └── raw/
│       └── customer_shopping_behavior.csv
├── images/
│   └── Power-BI/
│       └── Customer-Behavior-Dashboard.png
├── notebooks/
│   └── Comportamiento-de-compra.ipynb
├── sql/
│   └── customer_behavior.sql
├── src/
│   └── load_df_to_postgres.py
├── .gitignore
├── requirements.txt
└── README.md
```

The notebook documentation is written in Spanish. The `.env` file is intentionally not versioned.

---

## Dashboard Preview

### Power BI Dashboard

![Customer Behavior Dashboard](images/Power-BI/Customer-Behavior-Dashboard.png)

*Customer Behavior Dashboard built in Power BI on top of the PostgreSQL table.*

---

## Key Insights (C→F→I)

> Each insight follows the **Cause → Finding → Impact/Action** chain. All findings are descriptive: no hypothesis tests were run, and correlation does not imply causation. Figures come from the SQL queries (Q01–Q10) unless marked as a complementary calculation on the same table.

### Insight 1 — Revenue concentration by gender
- **Cause:** The customer base is unbalanced: 2,652 male customers (68.0%) vs 1,248 female customers (32.0%) *(complementary calculation)*.
- **Finding (Q01):** Male customers generated 157,890 USD (67.7%) and female customers 75,191 USD (32.3%). Average spend per customer is nearly identical (60.25 USD female vs 59.54 USD male, complementary calculation), so the gap comes from volume, not from ticket size.
- **Impact / Recommended Action:** Growth in female customers is the larger revenue lever. Test acquisition campaigns aimed at this segment before changing pricing or assortment.

### Insight 2 — Subscription shows no spending premium
- **Cause:** The subscription program does not translate into higher spend per customer.
- **Finding (Q05, Q09):** 1,053 subscribers (27.0% of customers) generate 26.9% of revenue, with an average spend of about 59 USD vs 60 USD for non-subscribers. All 1,053 subscribers are male; none of the 1,248 female customers subscribes *(complementary calculation)*. Among repeat buyers (more than 5 previous purchases), 958 of 3,476 subscribe (27.6%), compared with 22.4% for the remaining 424 customers *(complementary calculation, small comparison group)*.
- **Impact / Recommended Action:** Validate with the business owner whether the program is gender-restricted or whether this is a data issue, then redesign the subscription benefits so they give customers a reason to spend more.

### Insight 3 — High reliance on discounts
- **Cause:** Discounts are a standard part of the purchase experience rather than an exception.
- **Finding (Q02, Q06):** 43.0% of purchases carry a discount *(complementary calculation)*. The most discounted products are Hat (50.00%), Sneakers (49.66%), Coat (49.07%), Sweater (48.17%) and Pants (47.37%). About half of the discounted purchases (839 of 1,677) were at or above the average purchase amount of 59.76 USD.
- **Impact / Recommended Action:** Audit the discount policy against product margin (not available in this dataset) and restrict discounts on items that already sell at above-average ticket.

### Insight 4 — A mature, loyal customer base
- **Cause:** Most customers already have a long purchase history.
- **Finding (Q07):** Loyal (more than 10 previous purchases) 3,116 customers (79.9%), Returning (2–10) 701 (18.0%), New (1) 83 (2.1%). Segment thresholds are an analyst decision.
- **Impact / Recommended Action:** Prioritize retention and increase in purchase frequency over onboarding; investigate why few new customers enter the base.

### Insight 5 — Younger customers contribute the most revenue
- **Cause:** Age quartiles split the base into four groups of similar size, so revenue differences reflect spend per customer rather than group size.
- **Finding (Q10):** Young Adult 62,143 USD (26.7%), Middle-aged 59,197 USD (25.4%), Adult 55,978 USD (24.0%), Senior 55,763 USD (23.9%). The top group spends 11.4% more than the lowest.
- **Impact / Recommended Action:** Tailor communication and assortment to the 18–31 segment while keeping the other groups engaged; the gap is moderate and should be confirmed with a statistical test.

### Secondary observations
- **Shipping (Q04):** Express averages 60.48 USD vs 58.46 USD for Standard (+3.5%), a small difference.
- **Ratings (Q03):** The top-rated products are Gloves (3.86), Sandals (3.84), Boots (3.82), Hat (3.80) and Skirt (3.79); the spread is only 0.07 points. Null ratings are ignored by `AVG`.
- **Top products per category (Q08):** Jewelry, Blouse, Sandals and Jacket lead their categories. `ROW_NUMBER` breaks ties arbitrarily; `RANK` would be more appropriate where counts are equal.

---

## Business Recommendations

1. Validate the subscription program's eligibility and data, then redesign its benefits to drive higher spend.
2. Audit discount usage against margin and limit discounts on above-average purchases.
3. Invest in retention of the loyal base and run an acquisition test for female customers.
4. Evaluate whether an Express shipping promotion is worth it, given the small ticket uplift.
5. Validate any change through an A/B test before a full rollout.

---

## How to Reproduce

1. Clone the repository and create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate   # Git Bash on Windows
   pip install -r requirements.txt
   ```
2. Create a PostgreSQL database named `customer_behavior`.
3. Create a `.env` file in the project root with these variables (see the docstring of `src/load_df_to_postgres.py`):
   ```text
   PG_HOST=localhost
   PG_PORT=5432
   PG_DB=customer_behavior
   PG_USER=postgres
   PG_PASSWORD=your_password
   ```
4. Open `notebooks/Comportamiento-de-compra.ipynb`, update the dataset, `src` and `.env` paths to your local machine, and run all cells. The last cell loads the table `customer_behavior` into PostgreSQL.
5. Run `sql/customer_behavior.sql` in pgAdmin or `psql`.
6. Open `dashboards/power-bi/customer_behavior_dashboard.pbix` and update the data source to your local PostgreSQL instance. Screenshots are available in `images/`.

---

## Future Improvements

- Replace absolute paths in the notebook with relative paths.
- Add hypothesis tests (chi-square, t-test) to confirm the differences reported here.
- Incorporate cost and margin data to quantify the impact of discounts.
- Add a `.env.example` file and automated data-quality checks.
- Model the data as a star schema and explore dbt for transformations.

---

## Lessons Learned

- **Technical:** A Spanish-locale PostgreSQL server returned an error message that Python could not decode as UTF-8 (`UnicodeDecodeError`), hiding the real error; forcing `lc_messages=C` in the connection options solved the diagnosis. A case-sensitive mapping silently produced nulls in 1,131 rows, so validations such as `assert` are now part of the cleaning step. SQL integer division truncated percentages until `100.0` was used.
- **Business:** A large total can hide a simple explanation: the revenue gap between segments comes from customer volume, not from spend per customer.
- **Professional:** Reviewing every change before committing (`git status`, `git diff`, `git diff --staged`) and keeping secrets out of the repository are habits, not extras.

---

## Author

**Jacobo Galindo Ortiz**
Data Analyst Portfolio

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/jacobo-galindo-ortiz)
[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=flat&logo=github)](https://github.com/JacoboGO)
[![Tableau](https://img.shields.io/badge/Tableau-Public_Profile-E97627?style=flat&logo=tableau)](https://public.tableau.com/app/profile/jacobo.galindo.ortiz/vizzes)
[![Email](https://img.shields.io/badge/Email-Contact-EA4335?style=flat&logo=gmail)](mailto:jacobo.galindo.ortiz@hotmail.com)

---

> *"Language is a window into the mind."*
> — Noam Chomsky

<div align="center">

⭐ If this project was useful to you, consider leaving a star
on the repository — it helps a lot and is greatly appreciated.

</div>

---

## Usage Notice

This repository is provided for portfolio and educational review purposes.

The project may be viewed to evaluate the analytical approach,
methodology, and implementation. It is not intended for redistribution,
commercial use, or incorporation into other projects without prior
written permission from the author.

If you would like to reference or discuss any part of this work,
please contact the author.
