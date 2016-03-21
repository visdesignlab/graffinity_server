from flask import Flask

import py2neo as neo
import connectivity_matrix_neo as cm_neo
import json

app = Flask(__name__)


@app.route("/")
def hello_world():
    neo.authenticate('localhost:7474', 'neo4j', 'neo4j')
    neo_graph = neo.Graph('http://localhost:7474/db/data')
    results = neo_graph.cypher.execute("MATCH p=n-[:SYNAPSE*1..2]->m WHERE n.label='CBb3m'and m.label='GC' RETURN p")

    path_list = []

    for result in results:
        path_list.append(neo.Path(result.p))

    matrix = cm_neo.ConnectivityMatrix(path_list)
    graph = cm_neo.MarcLabGraph(results.to_subgraph())

    return json.dumps({
        "graph": graph.get_as_json_object(),
        "matrix": matrix.get_as_dictionary()
    })


if __name__ == '__main__':
    app.run()
