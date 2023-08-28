import os
import pyarrow.parquet as pq
import pandas as pd
import psycopg2
from azure.storage.blob import BlobServiceClient
import io
import json

def handle(req):

    try:
        # Retrieve connection details from environment variables
        postgres_conn_string = "postgresql://postgres:yourpassword@20.68.37.64:5432/yourdbname"
        postgres_table_name = "data"

        # Get blob name from the request query string
        # return type(req)
        reqs = json.loads(req)
        blob_name=reqs.get("blob_name")
        if blob_name:
            # Configure Azure Blob Storage
            storage_account_name = 'storageaccountdm'
            storage_account_key = 'Lmq5JUTQ2P4FYfzt6s3+756M087jPWoXbboRwHtepHL3jsxEcAVWxQeLYbYO0o3yyt9nywmI7EdV+AStw+Y5mA=='
            container_name = 'dms'

            blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net", credential=storage_account_key)
            blob_client = blob_service_client.get_blob_client(container_name, blob_name)

            # Download blob content
            blob_content = blob_client.download_blob().readall()
            buffer = io.BytesIO(blob_content)

            #buffer = pq.BufferReader(blob_content)
            # Load Parquet file using pyarrow
            # return func.HttpResponse(f"Parquet data loaded into {blob_content} successfully", status_code=200)
            # parquet_table = pq.read_table(source=blob_content)
            parquet_table = pq.ParquetFile(buffer)
            table = parquet_table.read()
            # Convert Parquet table to pandas DataFrame
            df = table.to_pandas()

            # Configure PostgreSQL
            conn = psycopg2.connect(postgres_conn_string)

            # Create a cursor
            cursor = conn.cursor()

            # Generate CREATE TABLE SQL command dynamically from DataFrame
            columns = ", ".join([f"{column} TEXT" for column in df.columns])
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {blob_name.split('.')[0]} ({columns})"

            # Execute CREATE TABLE command
            cursor.execute(create_table_sql)
            conn.commit()

            # Insert data into PostgreSQL
            for index, row in df.iterrows():
                insert_sql = f"INSERT INTO {blob_name.split('.')[0]} ({', '.join(row.keys())}) VALUES ({', '.join(['%s'] * len(row))})"
                cursor.execute(insert_sql, row)
            conn.commit()

            cursor.close()
            conn.close()

            return {"message":f"Parquet data loaded into {postgres_table_name.split('.')[0]} successfully"}
        else:
            return {"message":"Blob name is required in the query string"}
    except Exception as e:
        return {"message":f"Error: {e}"}