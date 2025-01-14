from igraph import Graph, plot
import random
import matplotlib.pyplot as plt

def create_random_connected_graph(n_vertices, n_edges, weights = None):
    """
    Creates a random graph with a guaranteed bridge and assigns random distances to edges.

    Parameters:
    - n_vertices: int, number of vertices in the graph.
    - n_edges: int, number of edges in the graph. Must be >= (n_vertices - 1).

    Returns:
    - An igraph.Graph object containing a random graph with at least one bridge.
    - List of tuples representing the bridges in the graph.
    """
    if n_edges < n_vertices - 1:
        raise ValueError("Number of edges must be at least n_vertices - 1 for a connected graph.")

    # Start with a connected random graph
    graph = Graph.Erdos_Renyi(n=n_vertices, m=n_edges, directed=False)
    while not graph.is_connected():
        graph = Graph.Erdos_Renyi(n=n_vertices, m=n_edges, directed=False)

    # Assign random distances (weights) to edges
    if weights is None:
        graph.es["distance"] = [random.randint(1, 100) for _ in range(graph.ecount())]
    else:
        graph.es["distance"] = weights

    # # Ensure there is a bridge if needed
    # bridges = graph.bridges()
    # if not bridges:
    #     # Add a bridge only if the graph is not fully connected
    #     components = graph.connected_components()
    #     if len(components) > 1:  # Only proceed if multiple components exist
    #         comp1 = components[0]
    #         comp2 = components[1]
    #         v1 = random.choice(comp1)
    #         v2 = random.choice(comp2)
    #         graph.add_edge(v1, v2, distance=random.randint(1, 100))  # Add a bridge with a random distance
    #         bridges = graph.bridges()  # Recalculate bridges

    return graph


def get_edgelist_custom(graph):
    """
    Converts an igraph.Graph object into a format suitable for C++.

    Parameters:
    - graph: igraph.Graph object with a 'distance' attribute on edges.

    Returns:
    - edges: List of tuples [(source, target, distance), ...].
    """
    if "distance" not in graph.edge_attributes():
        raise ValueError("The graph does not have a 'distance' edge attribute.")

    # Extract edges and distances
    edges = []
    for edge in graph.es:
        source = edge.source
        target = edge.target
        distance = edge["distance"]
        edges.append((source, target, distance))

    return edges


def plot_weighted_graph(graph):
    """
    Plots the graph with distances (weights) and highlights bridges.

    Parameters:
    - graph: igraph.Graph object, the graph to plot.
    - bridges: list of tuples, edges that are bridges in the graph.
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


# Example usage
if __name__ == "__main__":
    n_vertx = 10
    n_edges = 15
    graph = create_random_connected_graph(n_vertx, n_edges)
    print(graph.summary())
    # plot_weighted_graph(graph)
    print("Store graph data")
    # vertex_labels = g.vs["name"]  # Assuming vertex names are set
    # labeled_edge_list = [(vertex_labels[edge[0]], vertex_labels[edge[1]]) for edge in g.get_edgelist()]
    print(graph.get_edgelist())
    print(graph.es["distance"])
    print(get_edgelist_custom(graph))
    # graph.write_dot("graphs/random_graph.dot")
    # graph.write_graphml("graphs/random_graph.graphml")

