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
	docker exec -it spark /bin/bash

##############
copy-spark-cassandra-connector:
	docker cp path/to/spark-cassandra-connector spark:/opt/bitnami/workspace

###################### Utils ######################
cassandra-status:
	docker exec -it cassandra nodetool status

spark-status:
	docker exec -it spark ./bin/spark-shell sc.parallelize( 1 to 50 ).sum()

###################### Start & stop ######################
run-local: 
	docker-compose up -d

stop-local:
	docker-compose down

###################### Red zone ######################
clean-volume:
	docker volume rm cassandra-spark-docker_cassandra_data

clean-all-volumes: # Clear all volumes
	docker volume rm $$(docker volume ls -q)

clean-all-images: # Clear all images
	docker rmi $$(docker images -q)
