-- SQL ClickHouse untuk pipeline orders
-- Gunakan file ini untuk membuat database, tabel, dan verifikasi hasil load.

CREATE DATABASE IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.orders_top_products (
    product_name String,
    department String,
    total_orders Int32,
    reorder_count Int32,
    unique_users Int32
) ENGINE = MergeTree()
ORDER BY total_orders;

-- Verifikasi struktur
SHOW DATABASES;

USE analytics;

SHOW TABLES;

DESCRIBE TABLE orders_top_products;

-- Verifikasi data
SELECT COUNT(*) AS total_products
FROM orders_top_products;

SELECT product_name, department, total_orders, reorder_count, unique_users
FROM orders_top_products
ORDER BY total_orders DESC
LIMIT 10;
