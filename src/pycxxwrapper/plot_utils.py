from igraph import Graph, plot
import matplotlib.pyplot as plt


def plot_weighted_graph(graph: Graph) -> None:
    """
    Plots the graph with distances (weights).

    Parameters:
    - graph: igraph.Graph object, the graph to plot.
    """
    # Extract edge distances
    edge_distances = graph.es["distance"]

    # Prepare the visual style
    edge_colors = "black"
    layout = graph.layout("kk")  # Kamada-Kawai layout

    visual_style = {
        "vertex_size": 60,  # Increase node size for better visibility
        "vertex_label": range(graph.vcount()),
        "edge_width": 2,  # Uniform edge width
        "edge_color": edge_colors,
        "layout": layout,
    }

    # Plot using igraph's built-in plotting function
    fig, ax = plt.subplots(figsize=(10, 10))
    plot(graph, target=ax, **visual_style)

    # Add edge labels for distances
    coords = layout.coords  # Get layout coordinates
    for edge, label in zip(graph.es, edge_distances):
        source, target = coords[edge.source], coords[edge.target]
        midpoint = ((source[0] + target[0]) / 2, (source[1] + target[1]) / 2)
        ax.text(midpoint[0], midpoint[1], str(label), color="blue", fontsize=8, ha="center")

    plt.show()


def plot_graph_with_shortest_path(graph: Graph, path_edges: list[int], output_file: str = None):
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
    if output_file is None:
        plt.show()
    else:
        # spath = os.path.join("static", "images", output_file)
        plt.savefig(output_file, bbox_inches="tight")
        print(f"Graph saved.")

