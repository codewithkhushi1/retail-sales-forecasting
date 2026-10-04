-- 1. Top 10 Stores by Total Sales

SELECT
    store_id,
    SUM(weekly_sales) AS total_sales
FROM retail_sales
GROUP BY store_id
ORDER BY total_sales DESC
LIMIT 10;


-- 2. Average Sales: Holiday vs Non-Holiday

SELECT
    is_holiday,
    AVG(weekly_sales) AS average_weekly_sales
FROM retail_sales
GROUP BY is_holiday;


-- 3. Monthly Sales Trend

SELECT
    year,
    month,
    SUM(weekly_sales) AS total_sales
FROM retail_sales
GROUP BY year, month
ORDER BY year, month;


-- 4. Top 10 Departments by Sales

SELECT
    dept_id,
    SUM(weekly_sales) AS total_sales
FROM retail_sales
GROUP BY dept_id
ORDER BY total_sales DESC
LIMIT 10;


-- 5. Average Sales by Store

SELECT
    store_id,
    AVG(weekly_sales) AS average_sales
FROM retail_sales
GROUP BY store_id
ORDER BY average_sales DESC;


-- 6. Maximum and Minimum Weekly Sales

SELECT
    MAX(weekly_sales) AS highest_weekly_sales,
    MIN(weekly_sales) AS lowest_weekly_sales
FROM retail_sales;


-- 7. Store-wise Holiday Sales

SELECT
    store_id,
    SUM(weekly_sales) AS holiday_sales
FROM retail_sales
WHERE is_holiday = 1
GROUP BY store_id
ORDER BY holiday_sales DESC;


-- 8. Year-wise Sales

SELECT
    year,
    SUM(weekly_sales) AS total_sales
FROM retail_sales
GROUP BY year
ORDER BY year;

-- Note:
-- Depending on the processed dataset, the holiday column may be named
-- is_holiday or is_holiday_sales.