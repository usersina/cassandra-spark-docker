import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as _sum

spark: SparkSession = (
    SparkSession.builder.appName("Sales Analysis")
    .config(
        # Resolve already downloaded packages
        "spark.jars.packages",
        "com.datastax.spark:spark-cassandra-connector_2.12:3.5.0",
    )
    .config("spark.cassandra.connection.host", os.environ["CASSANDRA_HOST"])
    .config("spark.cassandra.auth.username", os.environ["CASSANDRA_USER"])
    .config("spark.cassandra.auth.password", os.environ["CASSANDRA_PASSWORD"])
    .getOrCreate()
)

if type(spark) != SparkSession:
    raise Exception("Spark session not created")

# Load the data from HDFS
data = spark.read.csv(
    os.environ["HDFS_URL"] + "/input/purchases.txt", sep="\t", header=False
)

# Rename the columns for easier access
data = data.selectExpr(
    "_c0 as date",
    "_c1 as time",
    "_c2 as store",
    "_c3 as item",
    "_c4 as cost",
    "_c5 as payment",
)

# Convert the cost column to float
data = data.withColumn("cost", data["cost"].cast("float"))

# Group by the store column and sum the cost column
result = data.groupBy("store").agg(_sum("cost").alias("total_sales"))

# Print the result
result.show()

# Append the result to the sales_analytics table in the cleaned_data keyspace
result.write.format("org.apache.spark.sql.cassandra").mode("append").option(
    "keyspace", "cleaned_data"
).option("table", "sales_analytics").save()
