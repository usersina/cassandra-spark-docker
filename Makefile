test:
	echo "Make file is working!"

cqlsh: # Creates a cassandra shell
	docker exec -it cassandra cqlsh -u cassandra -p cassandra

spark-shell: # Creates a spark shell
	docker exec -it spark ./bin/spark-shell

run-local: 
	docker-compose up -d

stop-local:
	docker-compose down