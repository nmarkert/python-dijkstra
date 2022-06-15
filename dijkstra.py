from abc import ABC, abstractmethod


class Dijkstra(ABC):

    def dijkstra_search(self, start, end):
        # TODO implementation of dijkstra algorithm
        pass

    @abstractmethod
    def get_neighbors(self, node):
        raise NotImplementedError

    # TODO more abstract methods which are needed for the dijkstra search
