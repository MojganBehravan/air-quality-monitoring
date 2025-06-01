from hdfs import InsecureClient
import pandas as pd
import os
import time

HDFS_URL = os.getenv("HDFS_URL", "http://namenode:9870")
HDFS_USER = os.getenv("HDFS_USER", "hadoop")
LOCAL_CSV_PATH = "/data/pollution_us_2000_2016.csv"
HDFS_DEST_PATH = "/raw/pollution_us_2000_2016.csv"

# Wait to ensure HDFS (namenode) is ready
time.sleep(10)
def main():
    client = InsecureClient('http://namenode:50070', user='hadoop')
    client.upload('/user/hadoop/raw/pollution_us_2000_2016.csv', '/data/pollution_us_2000_2016.csv', overwrite=True)

    # Retry HDFS connection
    for _ in range(10):
        try:
            df = pd.read_csv(LOCAL_CSV_PATH)
            client.write(HDFS_DEST_PATH, data=df.to_csv(index=False), overwrite=True)
            print(f"Uploaded to {HDFS_DEST_PATH}")
            break
        except Exception as e:
            print("Waiting for HDFS...", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
