# By: Huzaim Ali Khan, EE-24122


class Node:
    def __init__(self, id, node_type, data=None):
        self.id = id  # Unique identifier (e.g., 'User_1', 'Naruto')
        self.type = node_type  # Is the node a 'user' or 'anime'?
        self.data = data or {}  # for storing additional info like genre, score, etc.


class Edge:
    def __init__(self, source, target, weight):
        self.source = source  # Node ID
        self.target = target  # Node ID
        self.weight = weight  # Rating, similarity, etc.


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.adjacency = {}

    def add_node(self, id, node_type, data=None):
        if id not in self.nodes:
            self.nodes[id] = Node(id, node_type, data)
            self.adjacency[id] = []

    def add_edge(self, source, target, weight):
        if source in self.nodes and target in self.nodes:
            edge = Edge(source, target, weight)
            self.edges.append(edge)
            self.adjacency[source].append((target, weight))
        else:
            raise ValueError("Both source and target must be valid nodes.")

    def get_neighbors(self, node_id):
        return self.adjacency.get(node_id, [])
