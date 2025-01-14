from igraph import Graph
from pycxxwrapper.utils import load_graph
from pycxxwrapper.plot_utils import plot_weighted_graph
import sys, os


if __name__ == "__main__":
    gpath = os.path.join(os.getcwd(), 'graphs', sys.argv[1] + ".graphml")
    # Load the graph from the file
    graph = load_graph(gpath)
    print("Graph loaded successfully.")
    # Plot the graph
    plot_weighted_graph(graph)
