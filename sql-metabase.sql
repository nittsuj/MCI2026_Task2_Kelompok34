-- Katalog query untuk Questions Metabase
-- Tabel sumber: analytics.orders_top_products

-- Q1. KPI jumlah produk pada snapshot terbaru
SELECT COUNT(*) AS total_products
FROM analytics.orders_top_products;

-- Q2. KPI total order line
SELECT SUM(total_orders) AS total_order_lines
FROM analytics.orders_top_products;

-- Q3. KPI total reorder
SELECT SUM(reorder_count) AS total_reorders
FROM analytics.orders_top_products;

-- Q4. KPI rata-rata order per produk
SELECT AVG(total_orders) AS avg_orders_per_product
FROM analytics.orders_top_products;

-- Q5. Top 10 produk berdasarkan total_orders
SELECT product_name, total_orders
FROM analytics.orders_top_products
ORDER BY total_orders DESC
LIMIT 10;

-- Q6. Top 10 produk berdasarkan reorder_count
SELECT product_name, reorder_count
FROM analytics.orders_top_products
ORDER BY reorder_count DESC
LIMIT 10;

-- Q7. Top 10 produk berdasarkan unique_users
SELECT product_name, unique_users
FROM analytics.orders_top_products
ORDER BY unique_users DESC
LIMIT 10;

-- Q8. Jumlah produk per department
SELECT department, COUNT(*) AS total_products
FROM analytics.orders_top_products
GROUP BY department
ORDER BY total_products DESC;

-- Q9. Total orders per department
SELECT department, SUM(total_orders) AS total_orders
FROM analytics.orders_top_products
GROUP BY department
ORDER BY total_orders DESC;

-- Q10. Rasio reorder per produk untuk produk teratas
SELECT product_name, total_orders, reorder_count,
       reorder_count * 100.0 / total_orders AS reorder_ratio_percent
FROM analytics.orders_top_products
WHERE total_orders > 0
ORDER BY total_orders DESC
LIMIT 10;

-- Q11. Tabel ringkas produk teratas
SELECT product_name, department, total_orders, reorder_count, unique_users
FROM analytics.orders_top_products
ORDER BY total_orders DESC
LIMIT 20;
