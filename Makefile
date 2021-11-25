test:
	echo "Make file is working!"

###################### Main commands ######################
# Creates a cassandra shell instance
cassandra-shell:
	docker exec -it cassandra cqlsh -u cassandra -p cassandra

# Creates a spark shell instance
spark-shell:
	docker exec -it spark ./bin/spark-shell

###################### Start bashes ######################
cassandra-bash:
	docker exec -it cassandra bash;

spark-bash:
	docker exec -it spark bash;

###################### Utils ######################
cassandra-status:
	docker exec -ti cassandra nodetool status

###################### Start & stop ######################
run-local: 
	docker-compose up -d

stop-local:
	docker-compose down