-- Query 1: Overall Business KPIs
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT invoice_no) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(quantity) AS units_sold,
    ROUND(
        SUM(revenue) / COUNT(DISTINCT invoice_no),
        2
    ) AS average_order_value
FROM sales;


-- Query 2: Monthly Sales Performance
SELECT
    year_month,
    ROUND(SUM(revenue), 2) AS revenue,
    COUNT(DISTINCT invoice_no) AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    SUM(quantity) AS units_sold,
    ROUND(
        SUM(revenue) / COUNT(DISTINCT invoice_no),
        2
    ) AS average_order_value
FROM sales
GROUP BY year_month
ORDER BY year_month;


-- Query 3: Top Countries by Revenue
SELECT
    country,
    ROUND(SUM(revenue), 2) AS revenue,
    COUNT(DISTINCT invoice_no) AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    SUM(quantity) AS units_sold
FROM sales
GROUP BY country
ORDER BY revenue DESC
LIMIT 10;


-- Query 4: Top Products by Revenue
SELECT
    description,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    COUNT(DISTINCT invoice_no) AS orders
FROM sales
WHERE UPPER(description) NOT IN (
    'DOTCOM POSTAGE',
    'POSTAGE',
    'MANUAL'
)
GROUP BY description
ORDER BY revenue DESC
LIMIT 10;


-- Query 5: Top Customers by Revenue
SELECT
    customer_id,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT invoice_no) AS orders,
    SUM(quantity) AS units_purchased,
    ROUND(
        SUM(revenue) / COUNT(DISTINCT invoice_no),
        2
    ) AS average_order_value
FROM sales
WHERE customer_id IS NOT NULL
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 10;


-- Query 6: Sales by Day of Week
SELECT
    day_of_week,
    ROUND(SUM(revenue), 2) AS revenue,
    COUNT(DISTINCT invoice_no) AS orders,
    SUM(quantity) AS units_sold
FROM sales
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