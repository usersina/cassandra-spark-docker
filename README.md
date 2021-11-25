# **Cassandra & Spark Dockerized**
This repository is a preconfigured **Cassandra** & **Spark** playground.

## **0. Prerequisites**
- docker* (version 20 minimum)
- docker-compose* (version 1.29 minimum) 
- make (optional)

If make is not installed, you can check the `./Makefile` for the needed commands. 

You can run the following commands to check whether docker & docker-compose are installed:
- docker -v
- docker-compose -v

## **1. Start the containers**
```BASH
make run-local
```

## **2. Test the environment**
```BASH
make cassandra-status
```

```BASH
make spark-shell # Connect to spark

sc.parallelize( 1 to 50 ).sum() # Execute a spark action

CTRL/CMD + C # Exit bash 
```

## **3. Create some data in Cassandra**
Open a bash instance in the **cassandra container** as follows
```BASH
make cassandra-shell
```

Create the `employees_keyspace` & use it
```SQL
CREATE KEYSPACE employees_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE employees_keyspace;
```
Create an `employee_by_id` table & insert data to it
```SQL
CREATE TABLE employee_by_id (id int PRIMARY KEY, name text, position text);
INSERT INTO employee_by_id (id, name, position) VALUES(1, 'John', 'Manager');
INSERT INTO employee_by_id (id, name, position) VALUES(2, 'Bob', 'Adminstrator');
```
Check the data 
```SQL
SELECT * FROM employee_by_id;
```
Exit the cassandra container
```SQL
exit
```

## **4. Connecting to Spark**
*   Connect to the **spark container** bash
```BASH
make spark-bash
```

<!-- *   Install the **Spark Cassandra Connector**
Already included in the next command
```BASH
$SPARK_HOME/bin/spark-shell --packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0
$SPARK_HOME/bin/spark-submit --packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0
``` -->

*   Run the spark shell with custom configuration
```BASH
$SPARK_HOME/bin/spark-shell \
    --conf spark.cassandra.connection.host=cassandra \
    --conf spark.cassandra.auth.username=cassandra \
    --conf spark.cassandra.auth.password=cassandra \
    --conf spark.sql.extensions=com.datastax.spark.connector.CassandraSparkExtensions \
    --packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0 \
```

## **5. Interacting with Cassandra's data from Spark**

*   Create a Catalog Reference to the **Cassandra Cluster**
```SCALA
spark.conf.set(s"spark.sql.catalog.mycatalog", "com.datastax.spark.connector.datasource.CassandraCatalog")
```
*   Query the previously created `employee_by_id` table
```SCALA
spark.sql("SELECT * FROM mycatalog.employees_keyspace.employee_by_id").show
```


### References:
- https://github.com/datastax/spark-cassandra-connector/blob/master/doc/0_quick_start.md
- https://github.com/datastax/spark-cassandra-connector/blob/master/doc/1_connecting.md
- https://github.com/datastax/spark-cassandra-connector/blob/master/doc/reference.md