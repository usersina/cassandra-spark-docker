FROM python:3.12-bullseye
WORKDIR /app

RUN apt-get update && apt-get install -y openjdk-11-jdk

RUN pip install --no-cache-dir pyspark==3.1.2

ADD . /app

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_LOCAL_IP=spark
ENV HDFS_URL=hdfs://namenode:9000

CMD ["python", "process.py"]
