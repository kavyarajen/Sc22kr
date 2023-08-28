-- BI.SALE_REVENUE

DROP TABLE IF EXISTS BI.SALE_REVENUE;

CREATE TABLE BI.SALE_REVENUE AS SELECT
    p.name AS product_name,
    SUM(CAST(pay.amount AS NUMERIC)) AS total_revenue
FROM products p
LEFT JOIN activities a ON p._id = a.productid
LEFT JOIN payments pay ON a.user_id = pay.user_id
GROUP BY p._id, p.name
ORDER BY total_revenue DESC;

DROP TABLE IF EXISTS BI.AVG_PRICE;

CREATE TABLE BI.AVG_PRICE AS
SELECT
    COUNT(*) AS total_products,
    AVG(CAST(price AS NUMERIC)) AS average_price_all_products,
    MIN(CAST(price AS NUMERIC)) AS min_price_all_products,
    MAX(CAST(price AS NUMERIC)) AS max_price_all_products
FROM products;

DROP TABLE IF EXISTS BI.AVG_PRICE_USER;

CREATE TABLE BI.AVG_PRICE_USER AS
SELECT
    u.username,
    COUNT(p._id) AS total_products_purchased,
    AVG(CAST(p.price AS NUMERIC)) AS average_price_per_user,
    MIN(CAST(p.price AS NUMERIC)) AS min_price_per_user,
    MAX(CAST(p.price AS NUMERIC)) AS max_price_per_user
FROM users u
LEFT JOIN activities a ON u._id = a.user_id
LEFT JOIN products p ON a.productid = p._id
GROUP BY u._id, u.username
ORDER BY average_price_per_user DESC;


DROP TABLE IF EXISTS BI.AVG_PRICE_BRANDS;
CREATE TABLE BI.AVG_PRICE_BRANDS AS
SELECT
    b.name AS brand_name,
    COUNT(p._id) AS total_products,
    AVG(CAST(p.price AS NUMERIC)) AS average_price_per_brand,
    MIN(CAST(p.price AS NUMERIC)) AS min_price_per_brand,
    MAX(CAST(p.price AS NUMERIC)) AS max_price_per_brand
FROM brands b
LEFT JOIN products p ON b._id = p.brand
GROUP BY b._id, b.name
ORDER BY average_price_per_brand DESC;
