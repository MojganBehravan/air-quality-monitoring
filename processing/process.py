from pyspark.sql import SparkSession
from pyspark.sql.functions import avg

# Start Spark session
spark = SparkSession.builder \
    .appName("PollutionETL") \
    .getOrCreate()
print(" Spark session started")
# Read raw data from HDFS
df = spark.read.csv("hdfs://namenode:8020/user/hadoop/raw/pollution_us_2000_2016.csv", header=True, inferSchema=True)

print(" Data loaded")
df.show(5)

print(" DataFrame preview done")
# Clean: remove rows with nulls
df_clean = df.dropna()

# Transform: average pollution per state and date
df_agg = df_clean.groupBy("state", "Date Local").agg(
    avg("NO2 Mean").alias("avg_NO2"),
    avg("O3 AQI").alias("avg_O3"),
    avg("SO2 AQI").alias("avg_SO2"),
    avg("CO Mean").alias("avg_CO")
)

# Write output to HDFS
df_agg.write.mode("overwrite").json("hdfs://namenode:8020/user/hadoop/processed/summary.json")

spark.stop()
