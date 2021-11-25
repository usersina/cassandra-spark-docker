test:
	echo "Make file is working!"

cassandra-connection:
	docker exec -ti $(CONTAINER_ID) bash \
	&& cqlsh -u cassandra -p cassandra