from flask import Flask
from flask import request
import py2neo as neo
from py2neo import cypher
import connectivity_matrix_neo as cm_neo
import json
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)


def get_graph(graph_name):
    if graph_name == "marclab":
        neo.authenticate('localhost:7474', 'neo4j', 'neo4j')
        neo_graph = neo.Graph('http://localhost:7474/db/data')
    elif graph_name == "movies":
        neo.authenticate('localhost:7475', 'neo4j', 'neo4j')
        neo_graph = neo.Graph('http://localhost:7475/db/data')
    elif graph_name == "flights":
        neo.authenticate('localhost:7476', 'neo4j', 'neo')
        neo_graph = neo.Graph('http://localhost:7476/db/data')
    return neo_graph


def run_match(graph_name, key):
    graph = 0
    neo_graph = get_graph(graph_name)
    matches = []
    if graph_name == "marclab":
        graph = cm_neo.MarcLabGraph()
    elif graph_name == "movies":
        graph = cm_neo.MoviesGraph()
    elif graph_name == "flights":
        graph = cm_neo.FlightGraph()
    else:
        return json.dumps({
            "message": "Need to specify which graph -- either marclab or movies"
        }), 400

    node_attributes = graph.get_node_attributes()
    for attribute in node_attributes:
        attribute_type = attribute["DataType"]
        if attribute_type != "quantitative":
            attribute_name = attribute["DatabaseName"]
            query = "MATCH (n) WHERE n." + attribute_name + " =~ '(?i)" + key + ".*'" + " RETURN DISTINCT n." + attribute_name + " LIMIT 3;"
            results = neo_graph.cypher.execute(query)
            for result in results:
                matches.append({
                    "attribute": attribute_name,
                    "value": result[0]
                })

    return matches


def run_edge_match(graph_name, key):
    graph = 0
    neo_graph = get_graph(graph_name)
    matches = []
    if graph_name == "marclab":
        graph = cm_neo.MarcLabGraph()
    elif graph_name == "movies":
        graph = cm_neo.MoviesGraph()
    elif graph_name == "flights":
        graph = cm_neo.FlightGraph()
    else:
        return json.dumps({
            "message": "Need to specify which graph -- either marclab or movies"
        }), 400

    edge_attributes = graph.get_edge_attributes()
    for attribute in edge_attributes:
        attribute_type = attribute["DataType"]
        if attribute_type == "categorical":
            attribute_name = attribute["Name"]
            query = "MATCH ()-[r]->() WHERE r." + attribute_name + " =~ '(?i)" + key + ".*'" + " RETURN DISTINCT r." + attribute_name
            results = neo_graph.cypher.execute(query)
            for result in results:
                matches.append({
                    "attribute": attribute_name,
                    "value": result[0]
                })
    return matches



def run_query(graph_name, query):
    neo_graph = get_graph(graph_name)
    try:
        results = neo_graph.cypher.execute(query)
        path_list = []
        length_dictionary = {}
        for result in results:
            neo_path = neo.Path(neo.Path(result.p))
            path_list.append(neo_path)
            path_length = len(neo_path)
            if path_length not in length_dictionary:
                length_dictionary[path_length] = 1
            else:
                length_dictionary[path_length] += 1

        if graph_name == "marclab":
            matrix = cm_neo.ConnectivityMatrix(path_list, 'id', 'id')
            graph = cm_neo.MarcLabGraph()
        elif graph_name == "movies":
            matrix = cm_neo.ConnectivityMatrix(path_list, 'node_id', 'edge_id')
            graph = cm_neo.MoviesGraph()
        elif graph_name == "flights":
            matrix = cm_neo.ConnectivityMatrix(path_list, 'id', 'id')
            graph = cm_neo.FlightGraph()
        else:
            return json.dumps({
                "message": "Need to specify which graph -- either marclab or movies"
            }), 400

        graph.activate(results.to_subgraph())

        return json.dumps({
            "graph": graph.get_as_json_object(),
            "matrix": matrix.get_as_dictionary(),
            "lengths": length_dictionary
        })

    except cypher.CypherError as error:
        return json.dumps({
            "message": error.message
        }), 400


@app.route("/", methods=["GET", "POST"])
def default_resource():
    if request.method == "POST":
        query = request.get_json()[u'query']
        graph_name = request.get_json()[u'graph_name']
        return run_query(graph_name, query)
    elif request.method == "GET":
        return "Please send a POST request here! See _example_requests folder for details."


@app.route("/match", methods=["POST"])
def match_resource():
    request_data = request.get_json()
    graph_name = request_data[u'graph_name']
    key = request_data[u'key']
    return json.dumps(run_match(graph_name, key))


@app.route("/match_edge", methods=["POST"])
def match_edge():
    request_data = request.get_json()
    graph_name = request_data[u'graph_name']
    key = request_data[u'key']
    return json.dumps(run_edge_match(graph_name, key))

if __name__ == '__main__':
    app.run()
