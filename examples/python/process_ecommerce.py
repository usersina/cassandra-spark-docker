import os

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from pyspark.sql import SparkSession


# Create keyspace and table if they do not exist
def create_keyspace_and_table():
    print("Connecting to Cassandra...")
    auth_provider = PlainTextAuthProvider(
        username=os.environ["CASSANDRA_USER"], password=os.environ["CASSANDRA_PASSWORD"]
    )
    cluster = Cluster([os.environ["CASSANDRA_HOST"]], auth_provider=auth_provider)
    session = cluster.connect()

    print("Creating keyspace if it does not exist...")
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS cleaned_data
        WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 1 }
    """)

    # print("Dropping table if it exists...")
    # session.execute("""
    #     DROP TABLE IF EXISTS cleaned_data.ecommerce_transactions
    # """)

    print("Creating table if it does not...")
    session.execute("""
        CREATE TABLE IF NOT EXISTS cleaned_data.ecommerce_transactions (
            transaction_id UUID PRIMARY KEY,
            user_id INT,
            product_id INT,
            amount DECIMAL,
            timestamp TIMESTAMP
        )
    """)

    print("Keyspace and table setup completed.")
    session.shutdown()
    cluster.shutdown()


create_keyspace_and_table()

print("Creating Spark session...")
spark: SparkSession = (
    SparkSession.builder.appName("Ecommerce Transactions")
    .config(
        "spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.5.0"
    )
    .config("spark.cassandra.connection.host", os.environ["CASSANDRA_HOST"])
    .config("spark.cassandra.auth.username", os.environ["CASSANDRA_USER"])
    .config("spark.cassandra.auth.password", os.environ["CASSANDRA_PASSWORD"])
    .getOrCreate()
)

if type(spark) != SparkSession:
    raise Exception("Spark session not created")

print("Loading data from HDFS...")
data = spark.read.json(os.environ["HDFS_URL"] + "/data/ecommerce_transactions/*.json")

print("Data schema:")
data.printSchema()

print("Sample data:")
data.show()

print("Converting camelCase to snake_case...")
data = (
    data.withColumnRenamed("transactionId", "transaction_id")
    .withColumnRenamed("userId", "user_id")
    .withColumnRenamed("productId", "product_id")
)

print("Writing data to Cassandra...")
data.write.format("org.apache.spark.sql.cassandra").mode("append").option(
    "keyspace", "cleaned_data"
).option("table", "ecommerce_transactions").save()

print("Data write completed.")
