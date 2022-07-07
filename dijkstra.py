# https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
import math
from abc import ABC, abstractmethod


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

    def init_graph(self, start):
        nodes = self.get_nodes()
        graph = []
        for n in nodes:
            dijkstra_node = DijkstraNode(n)
            if n == start:
                dijkstra_node.dist = 0
            graph.append(dijkstra_node)
        return graph

    def get_node_with_min_dist(self, graph):
        min_dist = math.inf
        node = None
        for n in graph:
            if n.dist < min_dist:
                min_dist = n.dist
                node = n
        return node

    def get_dijkstra_node(self, graph, node):
        for n in graph:
            if n == node:
                return n
        return None

    def reformat_output(self, nodes):
        output = []
        for n in nodes:
            output.append((n.obj, n.dist, n.prev))
        return output

    def dijkstra_search(self, start, end):
        graph = self.init_graph(start)
        visited = []

        while len(graph) > 0:
            u = self.get_node_with_min_dist(graph)
            graph.remove(u)
            visited.append(u)

            for neigh in self.get_neighbors(u.obj):
                v = self.get_dijkstra_node(graph, neigh)
                if v is None:
                    continue
                alt = u.dist + self.get_weight(u.obj, v.obj)
                if alt < v.dist and u.dist != math.inf:
                    v.dist = alt
                    v.prev = u

        return self.reformat_output(visited)

    @abstractmethod
    def get_neighbors(self, node):
        """ Get all neighbor nodes of the given node """
        raise NotImplementedError

    @abstractmethod
    def get_nodes(self):
        """ Get all nodes in the graph """
        raise NotImplementedError

    @abstractmethod
    def get_weight(self, node1, node2):
        """ Get the weight for going from node1 to node2 (i.e. the distance) """
        raise NotImplementedError
