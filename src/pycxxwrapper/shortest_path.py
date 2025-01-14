from igraph import Graph, plot
import matplotlib.pyplot as plt

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

def compute_shortest_path(graph, source, sink):
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

def plot_graph_with_shortest_path(graph, path_edges, output_file=None):
    """
    Plots the graph with the shortest path highlighted and edge distances labeled.

    Parameters:
    - graph: igraph.Graph object
    - path_edges: list of edge IDs representing the shortest path
    - output_file: str, optional, file name to save the plot
    """
    # Extract edge distances (weights)
    edge_distances = graph.es["distance"] if "distance" in graph.es.attributes() else [""] * graph.ecount()

    # Default color for edges
    edge_colors = ["gray"] * graph.ecount()

    # Highlight the shortest path edges in red
    for eid in path_edges:
        edge_colors[eid] = "red"

    # Visual style for plotting
    layout = graph.layout("kk")  # Kamada-Kawai layout
    visual_style = {
        "vertex_size": 60,  # Increase node size for better visibility
        "vertex_label": range(graph.vcount()),  # Label vertices with their IDs
        "edge_width": [2 if color == "red" else 1 for color in edge_colors],
        "edge_color": edge_colors,
        "layout": layout,
    }

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 10))
    plot(graph, target=ax, **visual_style)

    # Add edge labels for distances
    coords = layout.coords  # Get layout coordinates
    for edge, label in zip(graph.es, edge_distances):
        source, sink = coords[edge.source], coords[edge.target]
        midpoint = ((source[0] + sink[0]) / 2, (source[1] + sink[1]) / 2)
        ax.text(midpoint[0], midpoint[1], str(label), color="blue", fontsize=8, ha="center")

    # Save or show the plot
    if output_file:
        plt.show()
    else:
        plt.savefig(output_file, bbox_inches="tight")
        print(f"Graph plotted and saved to {output_file}.")

if __name__ == '__main__':
    # Load the graph from the DOT file
    graph = load_graph("graphs/random_graph.graphml")
    print("Graph loaded successfully.")

    # Compute the shortest path
    source, sink = 1, 9  # Define source and sink vertices
    path, edges_in_path = compute_shortest_path(graph, source, sink)
    print("Shortest path:", path)
    print("Edges in shortest path:", edges_in_path)

    # Plot the graph with the shortest path highlighted
    plot_graph_with_shortest_path(graph, edges_in_path, output_file="shortest_path_graph.png")
