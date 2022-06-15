class Node:
    def __init__(self, node_id: int):
        self.id = node_id


class Edge:
    def __init__(self, edge_id: int, start: Node, end: Node, weight: float):
        self.id = edge_id
        self.start = start
        self.end = end
        self.weight = weight


class Graph:

    def __init__(self):
        self.nodes = list()
        self.edges = list()
        self.node_id = 0
        self.edge_id = 0

    def add_node(self):
        node = Node(self.node_id)
        self.node_id += 1
        self.nodes.append(node)
        return node

    def add_edge(self, start: Node, end: Node, weight: float, bidirectional: bool = True):
        self.edges.append(Edge(self.edge_id, start, end, weight))
        self.edge_id += 1

        if bidirectional:
            self.edges.append(Edge(self.edge_id, end, start, weight))
            self.edge_id += 1


