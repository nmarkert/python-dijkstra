# PyDijkstra

This python package provides an implementation of the  Dijkstra Search Algorithm for any kind of graphs.
The focus of this realization lies on the usability. <br>
If you have already written your own class which represents some sort of graph, and you want to 
use the dijkstra algorithm for path searching in this graph, this package is extremely easy to 
integrate. You don't have to transform your graph into another special search graph or something.
The only things you have to do, is inheriting from the provided class and override some methods.

## How to Use
**Install Package**
```
pip install pydijkstra
```

**Import Package and Inherit from Dijkstra Class**
```python
import pydijkstra

class MyGraph(pydijkstra.Dijkstra):
    ...
```

**Implement the Abstract Methods**
```python
def all_nodes(self) -> List[Any]:
    """ Return all nodes in the graph """

def neighbors(self, node: Any) -> List[Any]:
    """ Return all neighbor nodes of the given node """

def weight(self, node1: Any, node2: Any) -> float | int:
    """ Return the weight for going from node1 to node2 (i.e. the distance) """
```
*The typing 'Any' here stands for the representation of one node. So you are free in the choice
how you want to represent a node, i.e. use your own defined class, coordinates, ...*

**Use the dijkstra_search Method**
<br>which was inherited from the Dijkstra class
```python
dijkstra_search(start: Any, 
                target: Any = None, 
                output_format: str = 'dijkstra')
```
- (param) **start**: Node to start the dijkstra search from.
- (param) **target**: Target node in order to perform early stopping.
- (param) **output_format**: String which defines the format of the output. More on this at [Output Formats](#markdown-header-output-formats).
- (return) Result of the dijkstra search based on the output_format.

### Output Formats
For different uses you  may be need different outputs from the dijkstra search, so you can define the output of the
function by the output_format parameter. <br>
**Important!** The algorithm to calculate the path finding stays the same, independent of the output format. So changing
the output format does not lead to a change in calculation cost.
<br> <br>
The different options:
- `dijkstra` For each found node, it gives the previous visited node and the distance from the start node.
The value pair for each node is represented as a dict with 'prev' and 'dist' as its keys.
- `path` For each found node, it gives a list of nodes, which represents the shortest path from the start node.
- `path+dist` For each found node, it gives the shortest path and the distance from the start node.
The value pair for each node is represented as a dict with 'path' and 'dist' as its keys.
- `target_path` Gives a list of nodes, which represents the shortest path from the start node to the target node. (Only
                possible if target is given).

If the output format defines outputs for multiple nodes (i.e. when using 'dijkstra' or 'path'), it tries to return it 
as a dictionary with the nodes as the keys. If the node is not hashable (and so not usable as a key in the dictionary),
it instead returns a list with tuples where the node is the first object and the output the second
object of the tuple.

### Examples
Some examples on how the package can be used are found in the tests package. <br>
In simple_graph.py, a new graph structure is defined, which inherits from pydijkstra.Dijkstra and implements the needed functions
to be able to perform a dijkstra search on the graph it represents. <br>
In nx_search.py, a search class is defined, which gets a NetworkX graph and implements the needed functions with the
help of the functions provided by the graph, so it can serve as a path finding class for NetworkX graphs. <br>
In test.py, some unittests for the dijkstra algorithm are defined, which use the two implemented classes in order to
test the correctness of the dijkstra algorithm.
