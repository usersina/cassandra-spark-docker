FROM python:3.12-bullseye
WORKDIR /app

RUN apt-get update && apt-get install -y openjdk-11-jdk wget

# Install PySpark and cassandra-driver
RUN pip install --no-cache-dir pyspark==3.5.0 cassandra-driver==3.29.2

# Pre-download dependencies using spark-submit
RUN /usr/local/bin/spark-submit --packages com.datastax.spark:spark-cassandra-connector_2.12:3.5.0 --class org.apache.spark.examples.SparkPi --master local /usr/local/lib/python3.12/site-packages/pyspark/examples/src/main/python/pi.py

# Add the application code
ADD . /app

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_LOCAL_IP=spark
ENV HDFS_URL=hdfs://namenode:9000
ENV CASSANDRA_HOST=cassandra
ENV CASSANDRA_USER=cassandra
ENV CASSANDRA_PASSWORD=cassandra
