from pycxxwrapper.random_connected_graph import create_random_connected_graph
from igraph import Graph
import sys, os
from pycxxwrapper.plot_utils import plot_weighted_graph


def gen_and_store_graph(n: int, m: int, weights: list[float] = None, filename: str = None) -> Graph:
    """
    Generates a random connected graph and stores it in a file.

    Parameters:
    - n: int, number of vertices in the graph.
    - m: int, number of edges in the graph.
    - weights: list of floats, distances (weights) for each edge.
    - filename: str, name of the file to store the graph.

    Returns:
    - graph: igraph.Graph object, the generated graph.
    """
    # Generate a random connected graph
    graph = create_random_connected_graph(n, m, weights)

    # Store the graph in a file if needed
    if filename is not None:
        print("Store graph data")
        graph.write(filename)

    return graph

if __name__ == "__main__":
    n_vertx  = int(sys.argv[1])
    n_edges  = int(sys.argv[2])
    filename = sys.argv[3]
    graph = gen_and_store_graph(n_vertx, n_edges, filename = os.path.join(os.getcwd(), "graphs", filename + ".graphml"))

    # Plot the graph
    plot_weighted_graph(graph)
