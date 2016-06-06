class ConnectivityMatrix:
    """ Class for creating a matrix representation of multi-hop relationships in neo4j databases.
    """

    def __init__(self, path_list, node_id_key, edge_id_key):
        self.node_id_key = node_id_key
        self.edge_id_key = edge_id_key
        self._paths = []
        self._source_ids = []
        self._target_ids = []
        self._matrix = []
        self._init_source_and_targets(path_list)
        self._init_matrix(path_list)

    def _get_or_create_index(self, ids, node, allow_create=True):
        node_id = node.properties[self.node_id_key]
        for i in range(0, len(ids)):
            if ids[i] == node_id:
                return i

        if allow_create:
            ids.append(node_id)
            return len(ids) - 1

        raise Exception("Something went wrong creating the connectivity matrix!")

    def _get_or_create_source_index(self, node):
        return self._get_or_create_index(self._source_ids, node)

    def _get_or_create_target_index(self, node):
        return self._get_or_create_index(self._target_ids, node)

    def _get_path_as_id_list(self, path):
        id_list = []
        id_list.append(path.nodes[0].properties[self.node_id_key])
        for i in range(0, len(path.relationships)):
            id_list.append(path.relationships[i].properties[self.edge_id_key])
            id_list.append(path.nodes[i + 1].properties[self.node_id_key])
        return id_list

    def _get_source_index(self, node):
        return self._get_or_create_index(self._source_ids, node, False)

    def _get_target_index(self, node):
        return self._get_or_create_index(self._target_ids, node, False)

    def _init_source_and_targets(self, path_list):
        for path in path_list:
            self._get_or_create_source_index(path.nodes[0])
            self._get_or_create_target_index(path.nodes[-1])

    def _init_matrix(self, path_list):
        # Create empty matrix as a list of lists.
        for i in range(0, len(self._source_ids)):
            row = []
            for j in range(0, len(self._target_ids)):
                row.append([])
            self._matrix.append(row)

        # Shove each path into the matrix. Chop off the start and end vertices.
        for path in path_list:
            source = self._get_source_index(path.nodes[0])
            target = self._get_target_index(path.nodes[-1])
            self._matrix[source][target].append(self._get_path_as_id_list(path))

    def get_as_dictionary(self):
        return {
            "source_ids": self._source_ids,
            "target_ids": self._target_ids,
            "matrix": self._matrix
        }
