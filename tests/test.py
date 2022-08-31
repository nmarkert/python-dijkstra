import unittest
import networkx as nx
import simple_graph
import nx_search


class TestWikiGraph(unittest.TestCase):
    def setUp(self):
        # https://de.wikipedia.org/wiki/Dijkstra-Algorithmus#/media/Datei:Dijkstra_Animation.gif
        self.graph = simple_graph.Graph()
        self.n1, self.n2, self.n3, self.n4, self.n5, self.n6 = self.graph.add_nodes(6, ['1', '2', '3', '4', '5', '6'])
        self.graph.add_edge(self.n1, self.n2, 7)
        self.graph.add_edge(self.n1, self.n3, 9)
        self.graph.add_edge(self.n1, self.n6, 14)
        self.graph.add_edge(self.n2, self.n3, 10)
        self.graph.add_edge(self.n2, self.n4, 15)
        self.graph.add_edge(self.n3, self.n4, 11)
        self.graph.add_edge(self.n3, self.n6, 2)
        self.graph.add_edge(self.n4, self.n5, 6)
        self.graph.add_edge(self.n5, self.n6, 9)

    def testDist(self):
        out = self.graph.dijkstra_search(start=self.n1, output_format='dijkstra')
        self.assertEqual(out[self.n2]['dist'], 7)
        self.assertEqual(out[self.n3]['dist'], 9)
        self.assertEqual(out[self.n4]['dist'], 20)
        self.assertEqual(out[self.n5]['dist'], 20)
        self.assertEqual(out[self.n6]['dist'], 11)

    def testPrev(self):
        out = self.graph.dijkstra_search(start=self.n1, output_format='dijkstra')
        self.assertEqual(out[self.n2]['prev'], self.n1)
        self.assertEqual(out[self.n3]['prev'], self.n1)
        self.assertEqual(out[self.n4]['prev'], self.n3)
        self.assertEqual(out[self.n5]['prev'], self.n6)
        self.assertEqual(out[self.n6]['prev'], self.n3)

    def testPath(self):
        paths = self.graph.dijkstra_search(start=self.n1, output_format='path')
        # Path n1 -> n2
        path1 = paths[self.n2]
        self.assertEqual(len(path1), 2)
        self.assertIn(self.n1, path1)
        self.assertIn(self.n2, path1)
        # Path n1 -> n6
        path2 = paths[self.n6]
        self.assertEqual(len(path2), 3)
        self.assertIn(self.n3, path2)
        # Path n1 -> n5
        path3 = paths[self.n5]
        self.assertEqual(len(path3), 4)
        self.assertIn(self.n3, path3)
        self.assertIn(self.n6, path3)
        self.assertNotIn(self.n4, path3)


class TestGfGGraph(unittest.TestCase):
    def setUp(self):
        # https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(9))
        self.graph.add_edges_from([(0, 1, {'weight': 4}),
                                   (0, 7, {'weight': 8}),
                                   (1, 2, {'weight': 8}),
                                   (1, 7, {'weight': 11}),
                                   (2, 3, {'weight': 7}),
                                   (2, 5, {'weight': 4}),
                                   (2, 8, {'weight': 2}),
                                   (3, 4, {'weight': 9}),
                                   (3, 5, {'weight': 14}),
                                   (4, 5, {'weight': 10}),
                                   (5, 6, {'weight': 2}),
                                   (6, 7, {'weight': 1}),
                                   (6, 8, {'weight': 6}),
                                   (7, 8, {'weight': 7})])
        self.nxs = nx_search.NetworkXSearch(self.graph)

    def testDist(self):
        out = self.nxs.dijkstra_search(start=0, output_format='dijkstra')
        self.assertEqual(out[0]['dist'], 0)
        self.assertEqual(out[1]['dist'], 4)
        self.assertEqual(out[2]['dist'], 12)
        self.assertEqual(out[3]['dist'], 19)
        self.assertEqual(out[4]['dist'], 21)
        self.assertEqual(out[5]['dist'], 11)
        self.assertEqual(out[6]['dist'], 9)
        self.assertEqual(out[7]['dist'], 8)
        self.assertEqual(out[8]['dist'], 14)

    def testPrev(self):
        out = self.nxs.dijkstra_search(start=0, output_format='dijkstra')
        self.assertEqual(out[0]['prev'], None)
        self.assertEqual(out[1]['prev'], 0)
        self.assertEqual(out[2]['prev'], 1)
        self.assertEqual(out[3]['prev'], 2)
        self.assertEqual(out[4]['prev'], 5)
        self.assertEqual(out[5]['prev'], 6)
        self.assertEqual(out[6]['prev'], 7)
        self.assertEqual(out[7]['prev'], 0)
        self.assertEqual(out[8]['prev'], 2)

    def testTargetPath(self):
        target_path = self.nxs.dijkstra_search(start=0, target=4, output_format='target_path')
        self.assertTrue(type(target_path) == list)
        self.assertEqual(len(target_path), 5)
        self.assertIn(0, target_path)
        self.assertIn(4, target_path)
        self.assertIn(6, target_path)
        self.assertNotIn(3, target_path)

    def testPaths(self):
        paths = self.nxs.dijkstra_search(start=0, output_format='path')
        self.assertEqual(len(paths), 9)
        # Path 0 -> 8
        path1 = paths[8]
        self.assertEqual(len(path1), 4)
        self.assertIn(2, path1)
        self.assertNotIn(7, path1)
        # Path 0 -> 3
        path2 = paths[3]
        self.assertEqual(len(path2), 4)
        self.assertIn(1, path2)
        self.assertNotIn(5, path2)


if __name__ == '__main__':
    unittest.main()
