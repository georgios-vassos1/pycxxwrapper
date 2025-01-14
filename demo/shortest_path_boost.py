from pycxxwrapper.boost_wrapper import compute_shortest_path as cspcxx
from pycxxwrapper.utils import load_graph
from pycxxwrapper.plot_utils import plot_graph_with_shortest_path as plotxx
import sys, os


if __name__ == '__main__':
    source = int(sys.argv[1])
    sink   = int(sys.argv[2])
    gpath = os.path.join(os.getcwd(), 'graphs', sys.argv[3] + ".graphml")

    # Load the graph from the file
    graph = load_graph(gpath)
    print("Graph loaded successfully.")

    # Compute the shortest path
    num_vertices = graph.vcount()
    edge_list = graph.get_edgelist()
    weights = graph.es["distance"]

    sp = cspcxx(num_vertices, edge_list, weights, source, sink)

    print("Shortest path:", sp)

    # Extract edges in the shortest path
    sp_edges = [
        graph.get_eid(sp[i], sp[i + 1]) for i in range(len(sp) - 1)
    ]

    # Plot the graph with the shortest path highlighted
    plotxx(graph, sp_edges)
