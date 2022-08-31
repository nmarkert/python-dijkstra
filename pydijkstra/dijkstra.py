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
        if other is None:
            return False
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
        node = graph[0]
        min_dist = node.dist
        for n in graph[1:]:
            if n.dist < min_dist:
                min_dist = n.dist
                node = n
        return node

    def get_dijkstra_node(self, graph: List[DijkstraNode], node: Any) -> DijkstraNode | None:
        for n in graph:
            if n == node:
                return n
        return None

    def reconstruct_path(self, nodes: List[DijkstraNode], start_node: Any, target_node: Any):
        node = self.get_dijkstra_node(nodes, target_node)
        if node is None:
            return []
        path = [node.obj]
        while node != start_node:
            node = node.prev
            path.append(node.obj)
        path.reverse()
        return path

    def reformat_output(self, nodes: List[DijkstraNode], output_format: str, start_node: Any,
                        target_node: Any = None) -> Any:
        try:
            hash(start_node)
        except TypeError:
            as_dict = False
            output = []
        else:
            as_dict = True
            output = {}

        def append_output(key, value):
            if as_dict:
                output[key] = value
            else:
                output.append((key, value))

        if output_format == 'dijkstra':
            for node in nodes:
                prev = None
                if node.prev is not None:
                    prev = node.prev.obj
                append_output(node.obj, {'dist': node.dist, 'prev': prev})

        elif output_format == 'path':
            for node in nodes:
                append_output(node.obj, self.reconstruct_path(nodes, start_node, node.obj))

        elif output_format == 'path+dist':
            for node in nodes:
                append_output(node.obj, (self.reconstruct_path(nodes, start_node, node.obj), node.dist))

        elif output_format == 'target_path':
            if target_node is None:
                raise ValueError('target_path is not allowed as output_format if no target is specified!')
            output = self.reconstruct_path(nodes, start_node, target_node)

        else:
            raise ValueError(str(output_format) + ' is no valid output format!')

        return output

    def dijkstra_search(self, start: Any, target: Any = None, output_format: str = 'dijkstra'):
        unvisited = self.init_graph(start)
        visited = []

        while len(unvisited) > 0:
            u = self.get_node_with_min_dist(unvisited)
            if u.dist == math.inf:
                # Node with min dist has inf dist -> graph is not fully connected
                break

            unvisited.remove(u)
            visited.append(u)

            # Early Stopping if target node is found
            if u == target:
                break

            for neighbor in self.neighbors(u.obj):
                v = self.get_dijkstra_node(unvisited, neighbor)
                if v is None:
                    # neighbor was already visited
                    continue

                alt = u.dist + self.weight(u.obj, v.obj)
                if alt < v.dist and u.dist != math.inf:
                    v.dist = alt
                    v.prev = u

        return self.reformat_output(visited, output_format, start, target)

    @abstractmethod
    def neighbors(self, node: Any) -> List[Any]:
        """ Get all neighbor nodes of the given node """
        raise NotImplementedError

    @abstractmethod
    def all_nodes(self) -> List[Any]:
        """ Get all nodes in the graph """
        raise NotImplementedError

    @abstractmethod
    def weight(self, node1: Any, node2: Any) -> float | int:
        """ Get the weight for going from node1 to node2 (i.e. the distance) """
        raise NotImplementedError
