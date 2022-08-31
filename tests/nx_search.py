from typing import Any, List
import networkx as nx
import pydijkstra


class NetworkXSearch(pydijkstra.Dijkstra):

    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def all_nodes(self) -> List[Any]:
        return list(self.graph.nodes)

    def neighbors(self, node: Any) -> List[Any]:
        return list(self.graph.neighbors(node))

    def weight(self, node1: Any, node2: Any) -> float | int:
        if 'weight' in self.graph.edges[node1, node2]:
            return self.graph.edges[node1, node2]['weight']
        else:
            return 1
