import os
import azure.functions as func
import psycopg2

def execute_etl_queries(conn_string, queries):
    try:
        # Connect to the database
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        # Execute each query in the list
        for query in queries:
            cursor.execute(query)
            conn.commit()

        cursor.close()
        conn.close()

        return "ETL queries executed successfully."
    except Exception as e:
        return f"Error executing ETL queries: {e}"

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
       
        conn_string = 'postgresql://postgres:yourpassword@20.68.37.64:5432/yourdbname'

        etl_queries = [
            "DROP TABLE IF EXISTS BI.SALE_REVENUE;" ,
            "CREATE TABLE BI.SALE_REVENUE AS SELECT     p.name AS product_name,     SUM(CAST(pay.amount AS NUMERIC)) AS total_revenue FROM products p LEFT JOIN activities a ON p._id = a.productid LEFT JOIN payments pay ON a.user_id = pay.user_id GROUP BY p._id, p.name ORDER BY total_revenue DESC; " ,
            "DROP TABLE IF EXISTS BI.AVG_PRICE; " ,
            "CREATE TABLE BI.AVG_PRICE AS SELECT     COUNT(*) AS total_products,     AVG(CAST(price AS NUMERIC)) AS average_price_all_products,     MIN(CAST(price AS NUMERIC)) AS min_price_all_products,     MAX(CAST(price AS NUMERIC)) AS max_price_all_products FROM products;  ",
            "DROP TABLE IF EXISTS BI.AVG_PRICE_USER;"  ,
            "CREATE TABLE BI.AVG_PRICE_USER AS SELECT     u.username,     COUNT(p._id) AS total_products_purchased,     AVG(CAST(p.price AS NUMERIC)) AS average_price_per_user,     MIN(CAST(p.price AS NUMERIC)) AS min_price_per_user,     MAX(CAST(p.price AS NUMERIC)) AS max_price_per_user FROM users u LEFT JOIN activities a ON u._id = a.user_id LEFT JOIN products p ON a.productid = p._id GROUP BY u._id, u.username ORDER BY average_price_per_user DESC;" ,
            "DROP TABLE IF EXISTS BI.AVG_PRICE_BRANDS; ",
            "CREATE TABLE BI.AVG_PRICE_BRANDS AS SELECT     b.name AS brand_name,     COUNT(p._id) AS total_products,     AVG(CAST(p.price AS NUMERIC)) AS average_price_per_brand,     MIN(CAST(p.price AS NUMERIC)) AS min_price_per_brand,     MAX(CAST(p.price AS NUMERIC)) AS max_price_per_brand FROM brands b LEFT JOIN products p ON b._id = p.brand GROUP BY b._id, b.name ORDER BY average_price_per_brand DESC; "
        ]

        result = execute_etl_queries(conn_string, etl_queries)

        return func.HttpResponse(result, status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Error: {e}", status_code=500)
