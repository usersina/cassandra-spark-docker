# Cassandra & Spark in Docker

This repository is a preconfigured **Cassandra** & **Spark** playground.

## Prerequisites

- [docker & docker-compose](https://www.docker.com/)
- [go-task](https://taskfile.dev/)

If Task is not installed, you can check the [Taskfile](./Taskfile.yml) for the commands.

## Start the containers

```bash
task up
```

## Test the environment

Verify that cassandra is working

```BASH
task cassandra-status
```

Verify that spark is working

```BASH
# Enter the spark shell
task spark-shell

# Execute a spark action
sc.parallelize(1 to 50).sum()

# Exit
CTRL/CMD+C
```

## Create data in Cassandra

```bash
task cqlsh
```

Create the `employees_keyspace` & use it

```sql
CREATE KEYSPACE employees_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE employees_keyspace;
```

Create an `employee_by_id` table & insert data to it

```sql
CREATE TABLE employee_by_id (id int PRIMARY KEY, name text, position text);
INSERT INTO employee_by_id (id, name, position) VALUES(1, 'John', 'Manager');
INSERT INTO employee_by_id (id, name, position) VALUES(2, 'Bob', 'Adminstrator');
```

Check the data

```sql
SELECT * FROM employee_by_id;
```

Exit the cassandra container

```bash
CTRL + D
```

## Querying the data from spark

Open a bash in the spark container

```BASH
task spark-bash
```

Run spark shell with the [spark-cassandra-connector package](https://mvnrepository.com/artifact/com.datastax.spark/spark-cassandra-connector_2.12/3.5.0)

```BASH
$SPARK_HOME/bin/spark-shell \
    --conf spark.cassandra.connection.host=cassandra \
    --conf spark.cassandra.auth.username=cassandra \
    --conf spark.cassandra.auth.password=cassandra \
    --conf spark.sql.extensions=com.datastax.spark.connector.CassandraSparkExtensions \
    --conf spark.sql.catalog.mycatalog=com.datastax.spark.connector.datasource.CassandraCatalog \
    --packages com.datastax.spark:spark-cassandra-connector_2.12:3.5.0
```

Query the previously created `employee_by_id` table

```scala
spark.sql("SELECT * FROM mycatalog.employees_keyspace.employee_by_id").show
```

## References

- <https://github.com/datastax/spark-cassandra-connector/blob/master/doc/0_quick_start.md>
- <https://github.com/datastax/spark-cassandra-connector/blob/master/doc/1_connecting.md>
- <https://github.com/datastax/spark-cassandra-connector/blob/master/doc/reference.md>
