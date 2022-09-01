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

    @staticmethod
    def __get_node_with_min_dist(graph: List[DijkstraNode]) -> DijkstraNode:
        """
        Finds the DijkstraNode with the minimum distance in a given graph.

        :param graph: List of DijkstraNodes.
        :return: DijkstraNode with the minimum distance.
        """
        node = graph[0]
        min_dist = node.dist
        for n in graph[1:]:
            if n.dist < min_dist:
                min_dist = n.dist
                node = n
        return node

    @staticmethod
    def __get_dijkstra_node(graph: List[DijkstraNode], node: Any) -> DijkstraNode | None:
        """
        Finds the DijkstraNode in the graph which represents the given node.

        :param graph: List of DijkstraNodes.
        :param node: Node to which the related DijkstraNode should be found.
        :return: DijkstraNode representing the given node.
        """
        for n in graph:
            if n == node:
                return n
        return None

    @staticmethod
    def __reconstruct_path(nodes: List[DijkstraNode], start_node: Any, target_node: Any) -> List[Any]:
        """
        Reconstructs a path from a start_node to an end_node based on the given DijkstraNodes.

        :param nodes: List of DijkstraNodes from which the path should be reconstructed
        :param start_node: Node from which the path should start
        :param target_node: Node where the path should end
        :return: List of nodes representing the path
        """
        node = Dijkstra.__get_dijkstra_node(nodes, target_node)
        if node is None:
            return []
        path = [node.obj]
        while node != start_node:
            node = node.prev
            path.append(node.obj)
        path.reverse()
        return path

    @staticmethod
    def __reformat_output(nodes: List[DijkstraNode], output_format: str, start_node: Any,
                          target_node: Any = None) -> Any:
        """
        Reformats a list of DijkstraNodes into an output defined by the output_format.

        If it returns outputs for multiple nodes (i.e. when using 'dijkstra' or 'path'), it tries to return it as a
        dictionary with the node as the key. If the node is not hashable (and so not usable as a key in the dictionary),
        it instead returns a list with tuples where the node is the first object of the tuple and the output the second
        object.

        :param nodes: List of DijkstraNodes which defines the result of the dijkstra search.
        :param output_format: A string which defines the format of the output.
        :param start_node: Start node of the search. (Needed when reconstructing paths)
        :param target_node: Target node of the search. (Needed when reconstructing the target path)
        :return: The formatted output of the dijkstra search.
        """
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
                append_output(node.obj, Dijkstra.__reconstruct_path(nodes, start_node, node.obj))

        elif output_format == 'path+dist':
            for node in nodes:
                append_output(node.obj, {'path': Dijkstra.__reconstruct_path(nodes, start_node, node.obj),
                                         'dist': node.dist})

        elif output_format == 'target_path':
            if target_node is None:
                raise ValueError('target_path is not allowed as output_format if no target is specified!')
            output = Dijkstra.__reconstruct_path(nodes, start_node, target_node)

        else:
            raise ValueError(str(output_format) + ' is no valid output format!')

        return output

    def __init_graph(self, start: Any) -> List[DijkstraNode]:
        """
        Initializes the graph needed for the dijkstra search.

        :param start: Start node of the dijkstra search.
        :return: List of DijkstraNodes representing the graph.
        """
        nodes = self.all_nodes()
        graph = []
        for n in nodes:
            dijkstra_node = DijkstraNode(n)
            if n == start:
                dijkstra_node.dist = 0
            graph.append(dijkstra_node)
        return graph

    def dijkstra_search(self, start: Any, target: Any = None, output_format: str = 'dijkstra'):
        """
        Performs a dijkstra search from a given start node.

        :param start: Node to start the dijkstra search from.
        :param target: Target node in order to perform early stopping. (Optional)
        :param output_format: String which defines the format of the output. Options:
            - 'dijkstra' (Default): For found each node, it gives the previous visited node and the distance from the
                start node.
            - 'path': For each found node, it gives a list of nodes, which represents the shortest path from the start
                node.
            - 'path+dist': For each found node, it gives the shortest path and the distance from the start node.
            - 'target_path': Gives a list of nodes, which represents the shortest path from the start node to the target
                node. (Only possible if target is given.)
        :return: The result of the dijkstra search.
        """
        unvisited = self.__init_graph(start)
        visited = []

        while len(unvisited) > 0:
            u = Dijkstra.__get_node_with_min_dist(unvisited)
            if u.dist == math.inf:
                # Node with min dist has inf dist -> graph is not fully connected
                break

            unvisited.remove(u)
            visited.append(u)

            # Early Stopping if target node is found
            if u == target:
                break

            for neighbor in self.neighbors(u.obj):
                v = Dijkstra.__get_dijkstra_node(unvisited, neighbor)
                if v is None:
                    # neighbor was already visited
                    continue

                alt = u.dist + self.weight(u.obj, v.obj)
                if alt < v.dist and u.dist != math.inf:
                    v.dist = alt
                    v.prev = u

        return Dijkstra.__reformat_output(visited, output_format, start, target)

    @abstractmethod
    def all_nodes(self) -> List[Any]:
        """ Return all nodes in the graph """
        raise NotImplementedError

    @abstractmethod
    def neighbors(self, node: Any) -> List[Any]:
        """ Return all neighbor nodes of the given node """
        raise NotImplementedError

    @abstractmethod
    def weight(self, node1: Any, node2: Any) -> float | int:
        """ Return the weight for going from node1 to node2 (i.e. the distance) """
        raise NotImplementedError
