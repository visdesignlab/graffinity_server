#!/usr/bin/env bash
sudo /var/lib/neo4j/bin/neo4j stop
/home/vagrant/neo4j_marclab start
/home/vagrant/neo4j_flights start
