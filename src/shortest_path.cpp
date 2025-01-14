#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/dijkstra_shortest_paths.hpp>
#include <vector>
#include <limits>

namespace py = pybind11;
using namespace boost;

// Define the graph structure using Boost adjacency list
typedef adjacency_list<vecS, vecS, undirectedS, no_property, property<edge_weight_t, int>> Graph;
typedef graph_traits<Graph>::vertex_descriptor Vertex;

// Function to compute shortest path
std::vector<int> compute_shortest_path(
    int num_vertices,
    const std::vector<std::pair<int, int>>& edge_list,
    const std::vector<double>& weights,
    int source,
    int target) {
    
    Graph g(num_vertices);
    auto weight_map = get(edge_weight, g);

    // Add edges and weights to the graph
    for (size_t i = 0; i < edge_list.size(); ++i) {
        auto e = add_edge(edge_list[i].first, edge_list[i].second, g).first;
        weight_map[e] = weights[i];
    }

    std::vector<int> predecessors(num_vertices, -1);
    std::vector<int> distances(num_vertices, std::numeric_limits<int>::max());

    dijkstra_shortest_paths(
        g,
        source,
        predecessor_map(&predecessors[0]).distance_map(&distances[0]));

    // Backtrack from target to source using predecessors
    std::vector<int> path;
    for (Vertex v = target; v != source; v = predecessors[v]) {
        if (v == -1) { // No path found
            return {};
        }
        path.push_back(v);
    }
    path.push_back(source);
    std::reverse(path.begin(), path.end());
    return path;
}

// Bind the function to Python using pybind11
PYBIND11_MODULE(boost_wrapper, m) {
    m.doc() = "Shortest path computation module";
    m.def("compute_shortest_path", &compute_shortest_path,
          py::arg("num_vertices"),
          py::arg("edge_list"),
          py::arg("weights"),
          py::arg("source"),
          py::arg("target"),
          "Compute the shortest path between source and target.");
}

