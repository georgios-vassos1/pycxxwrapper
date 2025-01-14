from igraph import Graph
import boost_wrapper # The compiled pybind11 module

def load_graph(file_path):
    """
    Loads a graph from a DOT file.

    Parameters:
    - file_path: str, path to the DOT file.

    Returns:
    - graph: igraph.Graph object
    """
    graph = Graph.Read(file_path, format="graphml")
    return graph

def main():
    graph = load_graph("graphs/random_graph.graphml")
    print("Graph loaded successfully.")

    # Compute the shortest path
    source, sink = 1, 9  # Define source and sink vertices
    num_vertices = 10
    num_edges = 15

    edge_list = graph.get_edgelist()
    weights = graph.es["distance"]

    shortest_path = boost_wrapper.compute_shortest_path(num_vertices, edge_list, weights, source, sink)

    print("Shortest path:", shortest_path)

if __name__ == "__main__":
    main()

