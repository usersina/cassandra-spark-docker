# cassandra-spark-docker

# TODO: Organize notes
Cassandra: (Seeding a table)
1. CREATE KEYSPACE employees_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
2. USE employees_keyspace;
3. CREATE TABLE employee_by_id (id int PRIMARY KEY, name text, position text);
4. INSERT INTO employee_by_id (id, name, position) VALUES(1, 'John', 'Manager');
5. INSERT INTO employee_by_id (id, name, position) VALUES(1, 'Bob', 'Adminstrator');
6. SELECT * FROM employee_by_id;

Spark: (Should connect to cassandra)
1. sc.parallelize( 1 to 50 ).sum()