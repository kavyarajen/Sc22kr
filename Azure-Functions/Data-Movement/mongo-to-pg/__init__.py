import os
import azure.functions as func
import pyarrow.parquet as pq
import pandas as pd
import psycopg2
from azure.storage.blob import BlobServiceClient
import io
import psutil
import time

def get_resource_utilization():
    cpu_percent = psutil.cpu_percent(interval=1)  # Get CPU utilization as a percentage
    memory_info = psutil.virtual_memory()  # Get memory utilization information

    return cpu_percent, memory_info.percent 

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        postgres_conn_string = "postgresql://postgres:yourpassword@20.68.37.64:5432/yourdbname"
        postgres_table_name = "data"

        blob_name = req.params.get("blob_name")
        
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
            # return func.HttpResponse(f"Parquet data loaded into {blob_content} successfully", status_code=200)
            # parquet_table = pq.read_table(source=blob_content)
            parquet_table = pq.ParquetFile(buffer)
            table = parquet_table.read()
            df = table.to_pandas()
            conn = psycopg2.connect(postgres_conn_string)

            cursor = conn.cursor()
            columns = ", ".join([f"{column} TEXT" for column in df.columns])
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {blob_name.split('.')[0]} ({columns})"

            # Execute CREATE TABLE command
            cursor.execute(create_table_sql)
            conn.commit()
            i=0
            start_time = time.time()
            for index, row in df.iterrows():
                insert_sql = f"INSERT INTO {blob_name.split('.')[0]} ({', '.join(row.keys())}) VALUES ({', '.join(['%s'] * len(row))})"
                cursor.execute(insert_sql, row)
                i=i+1
                if time.time() - start_time > 120:
                    break
            conn.commit()

            cursor.close()
            conn.close()
            cpu_utilization, memory_utilization = get_resource_utilization()
            success_message = f"Parquet data loaded into {postgres_table_name.split('.')[0]} successfully"
            response_message = f"{success_message}\nCPU Utilization: {cpu_utilization}%\nMemory Utilization: {memory_utilization}%\nRows Ingested: {i}"
            return func.HttpResponse(response_message, status_code=200)
        else:
            return func.HttpResponse("Blob name is required in the query string", status_code=400)
    except Exception as e:
        return func.HttpResponse(f"Error: {e}", status_code=500)