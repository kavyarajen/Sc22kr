import pandas as pd
from pymongo import MongoClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from io import BytesIO
import json

def handle(req):
# Replace with your MongoDB connection details
    mongo_connection_string = "mongodb://20.68.37.64:27017"
    mongo_database_name = "ecommerce_db"
    #reqs = json.loads(req)
    #mongo_collection_name=reqs.get("collection_name")
    #reqs = json.loads(req)
    #mongo_collection_name =reqs.get("mongo_collection_name")
    # Replace with your Azure Blob Storage connection string and container name
    #azure_blob_connection_string = "DefaultEndpointsProtocol=https;AccountName=storageaccountdm;AccountKey=Lmq5JUTQ2P4FYfzt6s3+756M087jPWoXbboRwHtepHL3jsxEcAVWxQeLYbYO0o3yyt9nywmI7EdV+AStw+Y5mA==;EndpointSuffix=core.windows.net"
    #azure_blob_container_name = "dms"

    try:
        reqs = json.loads(req)
        mongo_collection_name=reqs.get("collection_name")
    #reqs = json.loads(req)
    #mongo_collection_name =reqs.get("mongo_collection_name")
    # Replace with your Azure Blob Storage connection string and container name
        azure_blob_connection_string = "DefaultEndpointsProtocol=https;AccountName=storageaccountdm;AccountKey=Lmq5JUTQ2P4FYfzt6s3+756M087jPWoXbboRwHtepHL3jsxEcAVWxQeLYbYO0o3yyt9nywmI7EdV+AStw+Y5mA==;EndpointSuffix=core.windows.net"
        azure_blob_container_name = "dms"
        #reqs = json.loads(req)
        #mongo_collection_name =reqs.get("mongo_collection_name")
        # Connect to MongoDB and retrieve data from collection
        client = MongoClient(mongo_connection_string)
        db = client[mongo_database_name]
        collection = db[mongo_collection_name]
        cursor = collection.find()
        data = list(cursor)
        for document in data:
            if '_id' in document:
                document['_id'] = str(document['_id'])
        df = pd.DataFrame(data)

        parquet_output = BytesIO()
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

        return {"message": "Data converted and uploaded successfully"}

    except Exception as e:
        return {"error": str(e)}