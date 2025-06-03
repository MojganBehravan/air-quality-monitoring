from hdfs import InsecureClient
import pandas as pd
import os
import time
import re

HDFS_URL = os.getenv("HDFS_URL", "http://namenode:50070")  # adjust if 9870 is needed
HDFS_USER = os.getenv("HDFS_USER", "hadoop")
LOCAL_DATA_DIR = "/data"
HDFS_DEST_DIR = "/user/hadoop/raw"
TRACKING_FILE = "/app/uploaded_files.txt"

# Wait for HDFS to start
time.sleep(10)

# Compile filename pattern for allowed files
file_pattern = re.compile(r'pollution_us_\d{4}_\d{2}\.csv|pollution_us_2000_2016\.csv')

def main():
    client = InsecureClient(HDFS_URL, user=HDFS_USER)

    # Initialize tracking file
    if not os.path.exists(TRACKING_FILE):
        open(TRACKING_FILE, "w").close()

    with open(TRACKING_FILE, "r") as f:
        uploaded_files = set(f.read().splitlines())

    # Iterate through files in /data
    for file in os.listdir(LOCAL_DATA_DIR):
        if not file_pattern.match(file):
            print(f"Skipping unrelated file: {file}")
            continue

        if file in uploaded_files:
            print(f"Already uploaded: {file}")
            continue

        local_file_path = os.path.join(LOCAL_DATA_DIR, file)
        hdfs_file_path = os.path.join(HDFS_DEST_DIR, file)

        print(f"Uploading {file} to HDFS...")

        # Retry uploading file to HDFS
        for _ in range(10):
            try:
                df = pd.read_csv(local_file_path)
                client.write(hdfs_file_path, data=df.to_csv(index=False), overwrite=True, encoding='utf-8')
                print(f" Uploaded {file} to {hdfs_file_path}")
                with open(TRACKING_FILE, "a") as track:
                    track.write(file + "\n")
                break
            except Exception as e:
                print(f"Waiting for HDFS or retrying upload for {file}...", e)
                time.sleep(5)

if __name__ == "__main__":
    main()
