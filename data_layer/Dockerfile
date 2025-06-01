FROM python:3.9-slim

WORKDIR /app

COPY upload_to_mongo.py .

RUN pip install pymongo hdfs

CMD ["python", "upload_to_mongo.py"]
