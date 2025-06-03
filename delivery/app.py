from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Connect to MongoDB (adjust host if needed)
mongo_host = os.getenv("MONGO_HOST", "mongodb")
client = MongoClient(f"mongodb://{mongo_host}:27017/")
db = client.air_quality
collection = db.summary

@app.route("/summary", methods=["GET"])
def get_summary():
    records = list(collection.find().limit(10))
    for r in records:
        r["_id"] = str(r["_id"])
    return jsonify(records)

@app.route("/filter", methods=["POST","GET"])
def filter_summary():
    filters = request.args if request.method == "GET" else request.json
    query = {}
    if "state" in filters:
        query["state"] = filters["state"]
    if "year" in filters:
        query["Date Local"] = {"$regex": f"^{filters['year']}"}
    records = list(collection.find(query).limit(50))
    for r in records:
        r["_id"] = str(r["_id"])
    return jsonify(records)

@app.route("/metadata", methods=["GET"])
def get_metadata():
    years = collection.distinct("Date Local")
    states = collection.distinct("state")

    # Extract unique years from ISO date strings
    years_clean = sorted(set(str(date)[:4] for date in years if date))
    states_clean = sorted([s for s in states if s])

    return jsonify({"years": years_clean, "states": states_clean})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
