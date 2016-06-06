import py2neo as neo
from py2neo import cypher

neo.authenticate('localhost:7475', 'neo4j', 'neo4j')
neo_graph = neo.Graph('http://localhost:7475/db/data')

num_entities = 0
nodes = neo_graph.cypher.execute("match (n) return n;")

for node in nodes:
    node[0].properties['node_id'] = num_entities
    num_entities += 1

edges = neo_graph.cypher.execute("match ()-[r]->() return r limit 10;")
for edge in edges:
    edge[0].properties['edge_id'] = num_entities
    num_entities += 1

neo_graph.push()

