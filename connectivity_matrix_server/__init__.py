from flask import Flask
import py2neo as neo

app = Flask(__name__)


@app.route("/")
def hello_world():
    neo.authenticate('localhost:7474', 'neo4j', 'neo4j')
    neo_graph = neo.Graph('http://localhost:7474/db/data')
    results = neo_graph.cypher.execute("MATCH (n) RETURN n LIMIT 10 ")
    string = "hello\n"
    for result in results:
        string += str(result[0].properties['id']) + '\n'
    return string



if __name__ == '__main__':
    app.run()
