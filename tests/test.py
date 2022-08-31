import unittest
import simple_graph


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

    def testCost(self):
        out = self.graph.dijkstra_search(self.n1, output_format='dijkstra')
        self.assertEqual(out[self.n2][0], 7)
        self.assertEqual(out[self.n3][0], 9)
        self.assertEqual(out[self.n4][0], 20)
        self.assertEqual(out[self.n5][0], 20)
        self.assertEqual(out[self.n6][0], 11)

    def testPrev(self):
        out = self.graph.dijkstra_search(self.n1, output_format='dijkstra')
        self.assertEqual(out[self.n2][1], self.n1)
        self.assertEqual(out[self.n3][1], self.n1)
        self.assertEqual(out[self.n4][1], self.n3)
        self.assertEqual(out[self.n5][1], self.n6)
        self.assertEqual(out[self.n6][1], self.n3)

    def testPath(self):
        paths = self.graph.dijkstra_search(self.n1, output_format='paths')
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


if __name__ == '__main__':
    unittest.main()