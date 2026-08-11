# ☕ Afficionado Coffee Roasters — Product Optimization & Revenue Contribution Analysis

A full end-to-end Business Analytics capstone project analyzing product-level sales data for a coffee business, 
built to identify hero products, revenue concentration, and menu optimization opportunities.

**Business Analyst Intern Capstone Project — Unified Mentor Pvt. Ltd. (2026)**

---

## 🔗 Quick Links

| Deliverable | Link |
|---|---|
| 🚀 Live Streamlit Dashboard | [Open App] (https://afficionado-coffee-revenue-analysis11.streamlit.app/)|
| 📄 Published Research Paper | [View on Figshare] (https://figshare.com/articles/journal_contribution/Product_Optimization_Revenue_Contribution_Analysis_-_Afficionado_Coffee_Roasters/33213333?file=67445109)|
| 📊 Power BI Report | See `Power BI/Coffee_Sales_Dashboard.pbix`, or screenshots below |
| 📝 Executive Summary | [Documents/Executive_Summary_Afficionado_Coffee_Roasters.pdf](Documents/Executive_Summary_Afficionado_Coffee_Roasters.pdf) |

---

## 📌 Project Overview

Afficionado Coffee Roasters sells 80 individual products across 9 categories from three store
locations. This project analyzes 149,116 real transaction records to answer a simple but
important question: **which products actually drive the business, and where is there room to
optimize the menu?**

The analysis covers the full analytics pipeline — from raw, messy transaction data to a live,
interactive web dashboard — using Python, MySQL, Power BI, and Streamlit.

---

## 🧠 Key Insights

- **Revenue is highly concentrated.** Just **11 of 29 product types generate 80%** of total
  revenue — a clear 80/20 (Pareto) pattern.
- **The top 10 products alone account for 78.96%** of total revenue.
- **Coffee and Tea dominate**, together contributing **66.7%** of total revenue across all
  9 categories.
- **Barista Espresso** is the single highest revenue-generating product ($91,406), even though
  **Brewed Chai Tea** sells in slightly higher volume — proof that popularity and profitability
  aren't always the same thing.
- A consistent group of underperforming products (Green Beans, House Blend Beans, select
  merchandise) sell in very low volumes year-round, flagging them as candidates for menu review.

---

## 🛠️ Tools & Tech Stack

| Stage | Tool |
|---|---|
| Data Cleaning | Python (pandas), Jupyter Notebook |
| Exploratory Data Analysis | MySQL |
| Static Reporting | Power BI |
| Interactive Web App | Streamlit, Plotly |
| Hosting / Deployment | Streamlit Community Cloud |

---

## 📂 Repository Structure

```
├── Documents/
│   ├── Executive_Summary_Afficionado_Coffee_Roasters.pdf
│   └── Research_Paper_Afficionado_Coffee_Roasters.pdf
├── Power BI/
│   ├── Coffee_Sales_Dashboard.pbix
│   ├── Page1.png              # Executive Overview
│   ├── Page2.png              # Product Performance
│   ├── Page3.png              # Revenue Contribution & Menu Optimization
│   └── table.png
├── app.py                     # Streamlit application
├── cleaned_coffee_sales.csv   # Cleaned dataset (149,116 transactions)
├── coffee_sales_analysis_queries.sql # # MySQL EDA queries(ranking, Pareto, revenue contribution)
├── Data_Cleaning.ipynb        # Python data cleaning notebook
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 📊 Power BI Report Preview

**Page 1 — Executive Overview**
![Executive Overview](Power%20BI/Page1.png)

**Page 2 — Product Performance**
![Product Performance](Power%20BI/Page2.png)

**Page 3 — Revenue Contribution & Menu Optimization**
![Revenue Contribution](Power%20BI/Page3.png)

---

## 🗃️ Dataset

- **149,116** individual sales transactions
- **3** store locations (Lower Manhattan, Hell's Kitchen, Astoria)
- **80** product SKUs across **9** product categories
- Covers full calendar year **2025**
- Fields: transaction ID, date/time, store, product details, unit price, quantity, revenue

---

## 🧮 SQL Concepts Demonstrated

`SELECT` · `GROUP BY` · `ORDER BY` · `LIMIT` · Aggregate Functions · Subqueries · `HAVING` ·
CTEs · Window Functions (`RANK()`, `DENSE_RANK()`)

Covers business overview KPIs, product ranking, revenue contribution %, hero/underperforming
product identification, Pareto (80/20) analysis, and category performance — see
[`coffee_sales_analysis_queries.sql`](coffee_sales_analysis_queries.sql) for all 17 queries.

---

## ▶️ Run Locally

```bash
# Clone the repo
git clone https://github.com/kehkasha786/Afficionado-coffee-revenue-analysis.git
cd Afficionado-coffee-revenue-analysis

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 👤 Author

**Kehkasha Ansari**
Business Analyst Intern, Unified Mentor Pvt. Ltd.
[LinkedIn](https://www.linkedin.com/in/kehkasha-ansari/) · [GitHub](https://github.com/kehkasha786)

---

## 📄 License

This project is licensed under the terms of the [MIT License](LICENSE).
