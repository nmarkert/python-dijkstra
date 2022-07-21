# https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
import math
from abc import ABC, abstractmethod
from typing import List, Any


class DijkstraNode:
    def __init__(self, obj):
        self.obj = obj
        self.dist = math.inf
        self.prev = None

    def __eq__(self, other):
        if type(other) != DijkstraNode:
            return self.obj == other
        else:
            return self.obj == other.obj


class Dijkstra(ABC):

    def init_graph(self, start: Any):
        nodes = self.all_nodes()
        graph = []
        for n in nodes:
            dijkstra_node = DijkstraNode(n)
            if n == start:
                dijkstra_node.dist = 0
            graph.append(dijkstra_node)
        return graph

    def get_node_with_min_dist(self, graph: List[DijkstraNode]) -> DijkstraNode:
        min_dist = math.inf
        node = None
        for n in graph:
            if n.dist < min_dist:
                min_dist = n.dist
                node = n
        return node

    def get_dijkstra_node(self, graph: List[DijkstraNode], node: Any) -> DijkstraNode | None:
        for n in graph:
            if n == node:
                return n
        return None

    def reconstruct_path(self, nodes, start_node, end_node):
        node = self.get_dijkstra_node(nodes, end_node)
        path = [node.obj]
        while node != start_node:
            node = node.prev
            path.append(node.obj)
        path.reverse()
        return path

    def reformat_output(self, nodes: List[DijkstraNode], output_format: str, start_node: Any = None,
                        end_node: Any = None):
        output = None
        if output_format == 'dijkstra':
            output = []
            for node in nodes:
                prev = None
                if node.prev is not None:
                    prev = node.prev.obj
                output.append((node.obj, node.dist, prev))

        elif output_format == 'single_path':
            output = self.reconstruct_path(nodes, start_node, end_node)

        elif output_format == 'all_paths':
            output = []
            for node in nodes:
                output.append((node.obj, self.reconstruct_path(nodes, start_node, node)))

        elif output_format == 'costs':
            output = []
            for node in nodes:
                output.append((node.obj, node.dist))

        return output

    def dijkstra_search(self, start, end=None, output_format='dijkstra'):
        graph = self.init_graph(start)
        visited = []

        while len(graph) > 0:
            u = self.get_node_with_min_dist(graph)
            graph.remove(u)
            visited.append(u)
            if end is not None and u == end:
                break

            for neighbor in self.neighbors(u.obj):
                v = self.get_dijkstra_node(graph, neighbor)
                if v is None:
                    continue
                alt = u.dist + self.weight(u.obj, v.obj)
                if alt < v.dist and u.dist != math.inf:
                    v.dist = alt
                    v.prev = u

        return self.reformat_output(visited, output_format, start, end)

    @abstractmethod
    def neighbors(self, node):
        """ Get all neighbor nodes of the given node """
        raise NotImplementedError

    @abstractmethod
    def all_nodes(self):
        """ Get all nodes in the graph """
        raise NotImplementedError

    @abstractmethod
    def weight(self, node1, node2):
        """ Get the weight for going from node1 to node2 (i.e. the distance) """
        raise NotImplementedError
