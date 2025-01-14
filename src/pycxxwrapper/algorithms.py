from igraph import Graph


def compute_shortest_path(graph: Graph, source: int, sink: int) -> tuple[list[int], list[int]]:
    """
    Computes the shortest path between a source and sink in the graph.

    Parameters:
    - graph: igraph.Graph object
    - source: int, source vertex index
    - sink: int, sink vertex index

    Returns:
    - path: list of vertex indices representing the shortest path
    - edges_in_path: list of edge IDs included in the shortest path
    """
    if "distance" not in graph.edge_attributes():
        raise ValueError("The graph does not have a 'distance' edge attribute.")

    # Compute the shortest path using 'distance' as the weight
    path = graph.get_shortest_paths(source, to=sink, weights="distance", output="vpath")[0]

    # Extract edges in the shortest path
    edges_in_path = [
        graph.get_eid(path[i], path[i + 1]) for i in range(len(path) - 1)
    ]

    return path, edges_in_path

# if __name__ == '__main__':
#     # Load the graph from the DOT file
#     graph = load_graph("graphs/random_graph.graphml")
#     print("Graph loaded successfully.")
#
#     # Compute the shortest path
#     source, sink = 1, 9  # Define source and sink vertices
#     path, edges_in_path = compute_shortest_path(graph, source, sink)
#     print("Shortest path:", path)
#     print("Edges in shortest path:", edges_in_path)
#
#     # Plot the graph with the shortest path highlighted
#     plot_graph_with_shortest_path(graph, edges_in_path, output_file="shortest_path_graph.png")
