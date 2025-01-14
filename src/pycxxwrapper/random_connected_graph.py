from igraph import Graph
import random

def create_random_connected_graph(n_vertices: int, n_edges: int, weights: list[int] = None) -> Graph:
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


# Example usage
if __name__ == "__main__":
    n_vertx = 10
    n_edges = 15

    graph = create_random_connected_graph(n_vertx, n_edges)
    print(graph.summary())

    # vertex_labels = g.vs["name"]  # Assuming vertex names are set
    # labeled_edge_list = [(vertex_labels[edge[0]], vertex_labels[edge[1]]) for edge in g.get_edgelist()]
    # print(graph.get_edgelist())
    # print(graph.es["distance"])
    # print(get_edgelist_custom(graph))
