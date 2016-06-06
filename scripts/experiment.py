import py2neo as neo
from py2neo import cypher

neo.authenticate('localhost:7475', 'neo4j', 'neo4j')
neo_graph = neo.Graph('http://localhost:7475/db/data')

nodes = neo_graph.cypher.execute("match (n:Person) return n limit 100;")

for node in nodes:
    print node
    print node[0].labels

