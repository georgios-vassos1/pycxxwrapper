from pycxxwrapper.algorithms import compute_shortest_path as csppy
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
    sp_nodes, sp_edges = csppy(graph, source, sink)
    print("Shortest path:", sp_nodes)
    print("Edges in shortest path:", sp_edges)

    # Plot the graph with the shortest path highlighted
    plotxx(graph, sp_edges)

