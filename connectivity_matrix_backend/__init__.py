from flask import Flask
from flask import request
import py2neo as neo
from py2neo import cypher
import connectivity_matrix_neo as cm_neo
import json

app = Flask(__name__)

neo.authenticate('localhost:7474', 'neo4j', 'neo4j')
neo_graph = neo.Graph('http://localhost:7474/db/data')


def run_query(graph, query):
    """
    :param graph: py2neo graph object
    :param query: cypher query string that must return paths
    :return:
    """
    try:
        results = neo_graph.cypher.execute(query)
        path_list = []
        for result in results:
            path_list.append(neo.Path(result.p))

        matrix = cm_neo.ConnectivityMatrix(path_list)
        graph = cm_neo.MarcLabGraph(results.to_subgraph())
        return json.dumps({
            "graph": graph.get_as_json_object(),
            "matrix": matrix.get_as_dictionary()
        })

    except cypher.CypherError as error:
        return json.dumps({
            "status_code": 400,
            "message": error.message
        })


@app.route("/", methods=["GET", "POST"])
def default_resource():
    if request.method == "POST":
        query = request.get_json()[u'query']
        return run_query(neo_graph, query)
    elif request.method == "GET":
        return "Please send a POST request here! See _example_requests folder for details."


if __name__ == '__main__':
    app.run()
