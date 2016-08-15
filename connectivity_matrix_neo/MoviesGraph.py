from Graph import *


class MoviesGraph(Graph):
    """ Implementation of a Graph object for converting from movies neo4j database to something for the frontend.

        This is currently broken. It doesn't have support for multi-typed nodes that appear in the movies dataset.

        TODO: Use neo4j schema to automatically generate this object.
    """

    def __init__(self):
        Graph.__init__(self)

    def _get_edge_id(self, edge):
        return edge["edge_id"]

    def _get_node_id(self, node):
        return node["node_id"]

    def _init_edge_attributes(self):
        self._edge_attributes.append({
            "Name": "ID",
            "DisplayName": "id",
            "DatabaseName": "edge_id",
            "Type": "int",
            "DataType": "index",
            "Unique": "true"
        })

    def _init_node_attributes(self):
        self._node_attributes.append({
            "Name": "ID",
            "DisplayName": "id",
            "DatabaseName": "node_id",
            "Type": "int",
            "DataType": "index",
            "Unique": "true"
        })

        self._node_attributes.append({
            "Name": "Name",
            "DisplayName": "name",
            "DatabaseName": "name",
            "Type": "string",
            "DataType": "id",
            "Unique": "false"
        })

    def _get_edge_as_dict(self, source, target, edge):
        edge_dictionary = {
            "ID": Utils.get_property_as_int(edge, "edge_id"),
            "SourceStructureID": Utils.get_property_as_int(source, "node_id"),
            "TargetStructureID": Utils.get_property_as_int(target, "node_id"),
            "SourceID": Utils.get_property_as_int(source, "node_id"),
            "TargetID": Utils.get_property_as_int(target, "node_id"),
        }
        return edge_dictionary
