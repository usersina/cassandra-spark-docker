import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as _sum

spark = (
    SparkSession.builder.appName("Sales Analysis").getOrCreate()  # type: ignore
)

# Load the data from HDFS
data = spark.read.csv(os.environ["HDFS_URL"] + "/purchases.txt", sep="\t", header=False)

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
