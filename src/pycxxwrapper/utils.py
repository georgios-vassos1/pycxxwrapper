from igraph import Graph


def get_edgelist_custom(graph: Graph) -> list[tuple[int, int, float]]:
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

def load_graph(file_path: str) -> Graph:
    """
    Loads a graph from a DOT file.

    Parameters:
    - file_path: str, path to the DOT file.

    Returns:
    - graph: igraph.Graph object
    """
    graph = Graph.Read(file_path, format="graphml")
    return graph

