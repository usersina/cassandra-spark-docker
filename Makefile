test:
	echo "Make file is working!"

cassandra-connection:
	docker exec -ti cassandra cqlsh -u cassandra -p cassandra

run-local:
	docker-compose up -d

stop-local:
	docker-compose down