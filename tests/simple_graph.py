import math
from typing import List, Tuple

import dijkstra


class Node:

    def __init__(self, node_id: int, name: str = None):
        self.id = node_id
        self.name = name

    def __str__(self) -> str:
        return '<Node:' + self.name + '>'

    def __repr__(self) -> str:
        return str(self)


class Edge:

    def __init__(self, edge_id: int, start: Node, end: Node, weight: float):
        self.id = edge_id
        self.start = start
        self.end = end
        self.weight = weight

    def __str__(self) -> str:
        return str(self.start) + " --" + str(self.weight) + "--> " + str(self.end)

    def __repr__(self) -> str:
        return str(self)


class Graph(dijkstra.Dijkstra):

    def __init__(self):
        self.nodes = list()
        self.edges = list()
        self.node_id = 0
        self.edge_id = 0

    def add_nodes(self, amount: int = 1, node_names: list = None) -> Node | Tuple[Node]:
        nodes = []
        if node_names is None or len(node_names) != amount:
            node_names = [None] * amount
        for i in range(amount):
            node = Node(self.node_id, node_names[i])
            self.node_id += 1
            self.nodes.append(node)
            nodes.append(node)
        if amount == 1:
            return nodes[0]
        return tuple(nodes)

    def add_edge(self, start: Node, end: Node, weight: float = 1, bidirectional: bool = True):
        self.edges.append(Edge(self.edge_id, start, end, weight))
        self.edge_id += 1

        if bidirectional:
            self.edges.append(Edge(self.edge_id, end, start, weight))
            self.edge_id += 1

    def all_nodes(self) -> List[Node]:
        return self.nodes

    def neighbors(self, node: Node) -> List[Node]:
        neighbors = []
        for edge in self.edges:
            if edge.start == node:
                neighbors.append(edge.end)
        return neighbors

    def weight(self, node1: Node, node2: Node) -> float:
        for e in self.edges:
            if e.start == node1 and e.end == node2:
                return e.weight
        return math.inf


if __name__ == '__main__':
    # Test graph: https://de.wikipedia.org/wiki/Dijkstra-Algorithmus#/media/Datei:Dijkstra_Animation.gif
    graph = Graph()
    n1, n2, n3, n4, n5, n6 = graph.add_nodes(6, ['1', '2', '3', '4', '5', '6'])
    graph.add_edge(n1, n2, 7)
    graph.add_edge(n1, n3, 9)
    graph.add_edge(n1, n6, 14)
    graph.add_edge(n2, n3, 10)
    graph.add_edge(n2, n4, 15)
    graph.add_edge(n3, n4, 11)
    graph.add_edge(n3, n6, 2)
    graph.add_edge(n4, n5, 6)
    graph.add_edge(n5, n6, 9)
    out1 = graph.dijkstra_search(n1)
    print(out1)



