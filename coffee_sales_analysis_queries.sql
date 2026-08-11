-- ======================================================================================================
-- Product Optimization & Revenue Contribution Analysis 
-- Company : Afficionado Coffee Roasters

-- Objective:
-- Analyze product sales and revenue contribution to identify hero products, underperforming products, 
-- revenue concentration, and opportunities for menu optimization.

-- Author: Kehkasha Ansari
-- Tools: MySQL, Python, Power BI, Streamlit
-- =====================================================================================================

-- Setup: create the working database and confirm the table loaded correctly
create database coffee_project;
use coffee_project;
select count(*) AS Total_Records from cleaned_coffee_sales;

-- =====================================================================================================

-- Section 1 : Business Overview & Product Performance
-- Query 1: Total Revenue(KPI)
Select round(sum(Revenue),2) AS Total_Revenue from cleaned_coffee_sales;

-- Query 2: Total Unique Products(KPI)
Select count(distinct product_id) AS Total_Products from cleaned_coffee_sales;

-- Query 3: Total Product Categories
Select count(distinct product_category) AS Total_Categories from cleaned_coffee_sales;

-- Query 4: Revenue by Product Categories
Select product_category, round(sum(Revenue),2) AS Total_Revenue from cleaned_coffee_sales
Group by product_category
Order by Total_Revenue desc;

-- Query 5: Top 10 Products by Sales Volume
Select product_type, sum(transaction_qty) AS Unit_Sold from cleaned_coffee_sales
Group by product_type
Order by Unit_sold desc
limit 10;

-- Query 6: Bottom 10 Products by Sales Volume
Select product_type, sum(transaction_qty) AS Unit_Sold from cleaned_coffee_sales
Group by product_type
Order by Unit_sold asc
limit 10; 

-- Query 7: Top 10 Revenue-Generating Products
Select product_type, round(sum(Revenue),2) AS Total_Revenue from cleaned_coffee_sales
Group by product_type
Order by Total_Revenue desc
Limit 10;

-- Query 8: Bottom 10 Products by Revenue
Select product_type, round(sum(Revenue),2) AS Total_Revenue from cleaned_coffee_sales
Group by product_type
Order by Total_Revenue asc
Limit 10;

-- Section 2 : Product Revenue Contribution Analysis
-- Query 9: Revenue Contribution (%) of Each Product
Select product_type, round(sum(Revenue),2) AS Total_Revenue, 
round(sum(Revenue)*100/(Select sum(Revenue) from cleaned_coffee_sales),2) AS Revenue_Contribution_Percentage 
from cleaned_coffee_sales
Group by product_type
Order by Total_Revenue desc;

-- Query 10: Revenue Share by Product Categories
Select product_category, round(sum(Revenue),2) AS Total_Revenue, 
round(sum(Revenue)*100/(Select sum(revenue) from cleaned_coffee_sales),2) AS Revenue_Percentage 
from cleaned_coffee_sales
Group by product_category
Order by Total_Revenue desc;

-- Section 3 : Product Ranking & Menu Optimization
-- Query 11: Compare Sales Rank vs Revenue Rank
With product_summary AS 
(
Select product_type, sum(transaction_qty) AS Units_Sold, round(sum(Revenue),2) AS Total_Revenue
from cleaned_coffee_sales
Group by product_type
)
Select product_type, Units_Sold, Total_Revenue,
RANK() over(order by Units_Sold desc) AS Sales_Rank,
RANK() over(order by Total_Revenue desc) AS Revenue_Rank
from product_summary
order by Sales_Rank;

-- Query 12: Hero Products
With product_summary AS
(
Select product_type, sum(transaction_qty) AS Units_Sold, round(sum(Revenue),2) AS Total_Revenue
from cleaned_coffee_sales
group by product_type
),
ranked_products AS
(
Select *, 
Rank() over(order by Units_Sold desc) AS Sales_Rank,
Rank() over(Order by Total_Revenue desc) AS Revenue_Rank
from product_summary
)
Select product_type, Units_Sold, Total_Revenue, Sales_Rank, Revenue_Rank from ranked_products
where Sales_Rank <=10 AND Revenue_Rank <=10
Order by Revenue_Rank;

-- Query 13: Underperforming products
With product_summary AS
(
Select product_type, sum(transaction_qty) AS Units_Sold, round(sum(Revenue),2) AS Total_Revenue
from cleaned_coffee_sales
group by product_type
)
Select product_type, Units_Sold, Total_Revenue, 
dense_rank() over(order by Units_Sold asc) AS Low_Sales_Rank,
dense_rank() over(Order by Total_Revenue asc) AS Low_Revenue_Rank
from product_summary
Order by Low_Sales_Rank, Low_Revenue_Rank
Limit 10;

-- Section 4 : Revenue Concentration(Top 10 Products Revenue/Total Revenue) Analysis
-- Query 14: Pareto (80/20) Analysis
With product_revenue AS
(
Select product_type, sum(Revenue) AS Total_Revenue from cleaned_coffee_sales
Group by product_type
),
pareto AS (
	Select product_type, Total_revenue, sum(Total_Revenue) 
    Over (order by Total_Revenue desc) AS Running_Revenue,
    Sum(Total_Revenue) Over () AS Overall_Revenue
    from product_revenue
    )
    Select product_type, round(Total_Revenue,2) As Revenue,
    round((Running_Revenue/Overall_Revenue) * 100,2) AS Cumulative_Revenue_Percentage
    from pareto
    Order by Revenue desc;
    
-- Query 15: Revenue Concentration Ratio
With product_revenue AS (
Select product_type, sum(Revenue) AS Total_Revenue from cleaned_coffee_sales
Group by product_type
),
top_products AS (
Select product_type, Total_Revenue from product_revenue 
Order by Total_Revenue desc
Limit 10 )
select Round(
(sum(Total_Revenue) / (Select sum(Revenue) from cleaned_coffee_sales)) * 100, 2) AS Revenue_Concentration_Ratio
From top_products;

-- Section 5 : Product Efficiency Analysis
-- Query 16: Product Efficiency Score
Select product_type, Round(sum(Revenue),2) AS Total_Revenue,
Round(sum(Revenue) / sum(transaction_qty),2) AS Revenue_Per_Unit from cleaned_coffee_sales
Group by product_type
order by Revenue_Per_Unit desc;

-- Section 6 : Category Performance
-- Query 17: High Revenue Categories
Select product_category, round(sum(Revenue),2) AS Total_Revenue from cleaned_coffee_sales
Group by product_category
Having sum(Revenue)>
(
Select avg(Category_Revenue) 
from 
	(
		Select sum(Revenue) AS Category_Revenue
        from cleaned_coffee_sales
        Group by product_category
	) AS category_summary
)
Order by Total_Revenue desc;
