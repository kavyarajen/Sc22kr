import azure.functions as func
from pymongo import MongoClient
import pandas as pd
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from io import BytesIO
import psutil
def get_resource_utilization():
    cpu_percent = psutil.cpu_percent(interval=1)  # Get CPU utilization as a percentage
    memory_info = psutil.virtual_memory()  # Get memory utilization information

    return cpu_percent, memory_info.percent 
def main(req: func.HttpRequest) -> func.HttpResponse:
    mongo_connection_string = "mongodb://20.68.37.64:27017"
    mongo_database_name = "ecommerce_db"
    #mongo_collection_name = req.params.get('collection_name')
    azure_blob_connection_string = "DefaultEndpointsProtocol=https;AccountName=storageaccountdm;AccountKey=Lmq5JUTQ2P4FYfzt6s3+756M087jPWoXbboRwHtepHL3jsxEcAVWxQeLYbYO0o3yyt9nywmI7EdV+AStw+Y5mA==;EndpointSuffix=core.windows.net"
    azure_blob_container_name = "dms"

    try:
        mongo_collection_name = req.params.get('collection_name')
        # Connect to MongoDB and retrieve data from collection
        client = MongoClient(mongo_connection_string)
        db = client[mongo_database_name]
        collection = db[mongo_collection_name]
        cursor = collection.find()
        data = list(cursor)
        for document in data:
            if '_id' in document:
                document['_id'] = str(document['_id'])
            if 'user_id' in document:
                document['user_id'] = str(document['user_id'])
            if 'productId' in document:
                document['productId'] = str(document['productId'])


        df = pd.DataFrame(data)
        parquet_output = BytesIO()
        df.to_parquet(parquet_output, index=False)
        parquet_output.seek(0)

        # # Convert DataFrame to Parquet format
        # parquet_output = "data.parquet"
        # df.to_parquet(parquet_output, index=False)

        # # Upload Parquet file to Azure Blob Storage
        # blob_service_client = BlobServiceClient.from_connection_string(azure_blob_connection_string)
        # blob_client = blob_service_client.get_blob_client(container=azure_blob_container_name, blob=parquet_output)
        # with open(parquet_output, "rb") as parquet_file_data:
        #     blob_client.upload_blob(parquet_file_data,overwrite=True)

        blob_service_client = BlobServiceClient.from_connection_string(azure_blob_connection_string)
        blob_client = blob_service_client.get_blob_client(container=azure_blob_container_name, blob=f"{mongo_collection_name}.parquet")
        blob_client.upload_blob(parquet_output, overwrite=True)
        cpu_utilization, memory_utilization = get_resource_utilization()
        success_message = f"Parquet data loaded successfully"
        response_message = f"{success_message}\nCPU Utilization: {cpu_utilization}%\nMemory Utilization: {memory_utilization}%\nRows Ingested: {i}"
        return func.HttpResponse(response_message, status_code=200)    
        #return func.HttpResponse("Data migration successful", status_code=200)

    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)