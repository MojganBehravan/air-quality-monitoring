from hdfs import InsecureClient
from pymongo import MongoClient
import json

# Connect to HDFS
hdfs_client = InsecureClient('http://namenode:50070', user='hadoop')

# List all JSON part files in the output directory
file_list = hdfs_client.list('/user/hadoop/processed/summary.json')

data = []
for file in file_list:
    if file.startswith("part-") and file.endswith(".json"):
        with hdfs_client.read(f'/user/hadoop/processed/summary.json/{file}') as reader:
            for line in reader:
                data.append(json.loads(line))

# Connect to MongoDB and upload
mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client['air_quality']
collection = db['summary']

collection.delete_many({})  # Clear old records
collection.insert_many(data)

print(" MongoDB updated successfully.")
