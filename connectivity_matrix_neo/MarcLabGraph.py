from Graph import *


class MarcLabGraph(Graph):
    """ Implementation of a Graph object for converting from marclab neo4j database to something for the frontend.

        TODO: Use neo4j schema to automatically generate this object.
    """

    def __init__(self):
        Graph.__init__(self)

    def _get_edge_id(self, edge):
        return edge["id"]

    def _get_node_id(self, node):
        return node["id"]

    def _get_edge_as_dict(self, source, target, edge):
        edge_dictionary = {
                    "ID": Utils.get_property_as_int(edge, "id"),
                    "SourceStructureID": Utils.get_property_as_int(source, "id"),
                    "TargetStructureID": Utils.get_property_as_int(target, "id"),
                    "SourceID": Utils.get_property_as_int(source, "id"),
                    "TargetID": Utils.get_property_as_int(target, "id"),
                    "Type": Utils.get_property_as_string(edge, "type"),
                    "LinkedStructures": Utils.get_property_as_string(edge, "structures")
                }
        return edge_dictionary

    def _init_edge_attributes(self):
        self._edge_attributes.append({
            "Name": "ID",
            "DisplayName": "id",
            "Type": "int",
            "DataType": "index",
            "Unique": "true"
        })

        self._edge_attributes.append({
            "Name": "SourceID",
            "DisplayName": "source id",
            "Type": "int",
            "DataType": "source-index",
            "Unique": "false"
        })

        self._edge_attributes.append({
            "Name": "TargetID",
            "DisplayName": "target id",
            "Type": "int",
            "DataType": "target-index",
            "Unique": "true"
        })

        self._edge_attributes.append({
            "Name": "TargetID",
            "DisplayName": "target id",
            "Type": "int",
            "DataType": "target-index",
            "Unique": "true"
        })

        self._edge_attributes.append({
            "Name": "type",
            "DisplayName": "edge type",
            "Type": "string",
            "DataType": "categorical",
            "Unique": "false"
        })

        self._edge_attributes.append({
            "Name": "LinkedStructures",
            "DisplayName": "structures",
            "Type": "string",
            "DataType": "string",
            "Unique": "false"
        })

    def _init_node_attributes(self):
        self._node_attributes.append({
            "Name": "ID",
            "DisplayName": "id",
            "DatabaseName": "id",
            "Type": "int",
            "DataType": "index",
            "Unique": "true"
        })

        self._node_attributes.append({
            "Name": "Label",
            "DisplayName": "label",
            "DatabaseName": "label",
            "Type": "string",
            "DataType": "categorical",
            "Unique": "false"
        })

        self._node_attributes.append({
            "Name": "Structure",
            "DisplayName": "structure uri",
            "DatabaseName": "structure",
            "Type": "string",
            "DataType": "id",
            "Unique": "true"
        })

        self._node_attributes.append({
            "Name": "StructureID",
            "DisplayName": "structure id",
            "DatabaseName": "id",
            "Type": "int",
            "DataType": "id",
            "Unique": "true"
        })

        # self._node_attributes.append({
        #     "Name": "HullArea",
        #     "DisplayName": "area",
        #     "DatabaseName": "hull",
        #     "Type": "float",
        #     "DataType": "quantitative",
        #     "Unique": "false"
        # })

        # self._node_attributes.append({
        #     "Name": "Locations",
        #     "DisplayName": "locations",
        #     "DatabaseName": "locations",
        #     "Type": "int",
        #     "DataType": "quantitative",
        #     "Unique": "false"
        # })
