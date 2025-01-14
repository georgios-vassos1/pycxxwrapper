# Compiled Packaging with pybind11

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Wrapping C++ Code with pybind11](#wrapping-c-code-with-pybind11)
4. [Building with CMake](#building-with-cmake)

## Installation

To install the `pycxxwrapper` package, follow these steps:

1. **Create and Activate a Virtual Environment**:
   Use a tool like <a href="https://virtualenvwrapper.readthedocs.io/en/latest/" target="_blank">`virtualenvwrapper`</a> to set up a clean environment for your project.

2. **Install Build Dependencies**:
   Install the required build package using pip:
   ```bash
   pip install build==1.2.2.post1
   ```

3. **Build the Package**:
   Use <a href="https://scikit-build-core.readthedocs.io/en/latest/" target="_blank">`scikit-build-core`</a> to compile the project and generate a wheel file:
   ```bash
   python -m build
   pip install dist/pycxxwrapper-XXX-XXX-XXX.whl
   ```

> **Note**: Ensure that any C++ libraries specified in the `CMakeLists.txt` file are installed separately, as these are not managed by the Python dependencies.

### Build System Configuration

The build process relies on the `pyproject.toml` file to configure the build backend. For `scikit-build-core`, include the following in your `pyproject.toml`:

```toml
[build-system]
requires = ["scikit-build-core"]
build-backend = "scikit_build_core.build"
```

`scikit-build-core` simplifies the process of building Python projects that integrate native extensions or require CMake. It:

- Configures the build environment.
- Runs CMake commands to generate build files.
- Compiles the project (e.g., shared libraries or executables).
- Creates Python-compatible distributions (`.whl` and `.tar.gz`).

### Build Outputs

Upon successful build, the distribution files (e.g., `dist/project-XXX-XXX-XXX.whl`) will be available in the `dist/` directory.

After building the package, the project directory structure will look like this:

```
├── CMakeLists.txt
├── README.md
├── build
├── demo
│   ├── gen_and_store_graph.py
│   ├── graphs
│   │   ├── graph001.graphml
│   │   ├── graph002.graphml
│   │   ├── graph003.graphml
│   │   ├── graph004.graphml
│   │   └── graph005.graphml
│   ├── shortest_path_boost.py
│   ├── shortest_path_igraph.py
│   └── view_graph_from_file.py
├── dist
│   ├── pycxxwrapper-0.1.0-cp313-cp313-macosx_15_0_arm64.whl
│   └── pycxxwrapper-0.1.0.tar.gz
├── pyproject.toml
├── src
│   ├── CMakeLists.txt
│   ├── pycxxwrapper
│   │   ├── __init__.py
│   │   ├── algorithms.py
│   │   ├── graphs
│   │   │   └── random_graph.graphml
│   │   ├── plot_utils.py
│   │   ├── random_connected_graph.py
│   │   └── utils.py
└── └── shortest_path.cpp
```

## Getting Started

After installation, you can begin using the package by importing its modules and utilities. Here's how you can get started:

### Running the Demo Scripts

The `demo/` directory contains several scripts that demonstrate the package's capabilities. Change to the `demo/` directory and run the scripts using Python:
```bash
cd demo
```

The following command will create a connected graph with 10 nodes and 15 edges and store it in a file named `demo/graphs/graphXXX.graphml`:
```bash
python gen_and_store_graph.py 10 15 graphXXX
```

To visualize one of the graphs stored as a GraphML file in the `demo/graphs` directory, run the following command:
```bash
python view_graph_from_file.py graphXXX
```

You can compute and visualize the shortest path between a source and a sink, for instance, 0 and 8, in any of the graphs stored in `demo/graphs`, e.g., `graphXXX.graphml`, using the following command:
```bash
python shortest_path_igraph.py graphXXX 0 8
```
This script uses the `igraph` library to compute the shortest path between the source and sink nodes in the graph.

The same operation can be performed using the `shortest_path_boost.py` script, which uses the Boost library to compute the shortest path in C++ through a Python call:
```bash
python shortest_path_boost.py graphXXX 0 8
```

You can inspect the source code in the demo scripts to understand how the package is used to perform various operations.

## Wrapping C++ Code with pybind11

### Overview of `pybind11`

- `pybind11` is a lightweight header-only library for creating Python bindings for C++ code.
- It allows seamless interaction between Python and C++ by mapping types and exposing functions/classes.

### The `PYBIND11_MODULE` Macro

The `PYBIND11_MODULE` macro defines the Python module:

- **Module Name**: The name specified (e.g., `boost_wrapper`) is how the module is imported in Python.
- **`pybind11::module` Object**: Used to bind functions, classes, and variables to the module.

Example:

```cpp
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

    // Implementation in src/shortest_path.cpp
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
```

### Automatic Type Conversion
`pybind11` handles conversions between Python and C++ types:
- Python lists/tuples map to `std::vector` or `std::pair`.
- C++ containers are returned as Python lists.

### Boost Graph Library
- **Graph Representation**: `adjacency_list` is used for the graph structure.
- **Dijkstra's Algorithm**: Computes the shortest paths from a source vertex to all others.

### Python Interface
- Graph details are passed as Python arguments.
- The function `compute_shortest_path` processes these details and returns the shortest path as a Python list.


## Building with CMake

The `CMakeLists.txt` file defines the build configuration for your project. Below is an explanation of its components.

### Key Sections

1. **Project Configuration**:
   - `cmake_minimum_required(VERSION 3.15)`: Ensures compatibility with CMake version 3.15 or higher.
   - `project(pycxxwrapper)`: Sets the project name.
   - `set(CMAKE_CXX_STANDARD 17)`: Specifies that the project uses C++17.

2. **Dependencies**:
   - `find_package(Python3 COMPONENTS Development REQUIRED)`: Finds the Python3 development libraries.
     - Ensures the necessary Python headers and libraries are available for compilation.
   - `find_package(pybind11 REQUIRED)`: Locates the `pybind11` library, which simplifies creating Python bindings for C++.
     - Ensures all required components of `pybind11` are included.
   - `find_package(Boost REQUIRED)`: Locates the Boost C++ libraries.
     - Boost provides a collection of portable and high-performance libraries.

3. **Module Creation**:
   - `pybind11_add_module(boost_wrapper MODULE shortest_path.cpp)`: Compiles the `shortest_path.cpp` file into a Python module named `boost_wrapper`.
     - Automatically links the necessary Python and `pybind11` libraries.
     - The `MODULE` keyword specifies that the output will be a Python extension module.

4. **Output Directory**:
   - `set_target_properties(boost_wrapper PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/src)`: Configures the directory where the compiled module (`boost_wrapper`) will be placed.
     - `${CMAKE_BINARY_DIR}` refers to the directory where the build files are generated.

5. **Installation**:
   - `install(TARGETS boost_wrapper DESTINATION pycxxwrapper)`: Installs the compiled module into the `pycxxwrapper` directory.
     - Ensures the module is copied to the correct location during the installation process.

### How These Commands Work

- **`find_package`**:
  - Searches for installed libraries or packages required by the project.
  - Ensures the necessary dependencies (e.g., Python, `pybind11`, Boost) are available for compilation.

- **`pybind11_add_module`**:
  - Simplifies the creation of Python modules from C++ source files.
  - Automatically handles linking Python, `pybind11`, and any specified dependencies.

- **`set_target_properties`**:
  - Customizes properties for the build target (e.g., output directory, build flags).
  - In this case, it specifies where the compiled Python module (`boost_wrapper`) will be placed.

- **`install`**:
  - Defines rules for installing built files or targets.
  - Specifies the destination directory for the compiled Python module, ensuring it can be accessed by Python after installation.

This configuration ensures seamless integration between Python and C++ while leveraging Boost and pybind11 to enable advanced functionality.

## Additional Resources

For more information:

- [scikit-build-core Documentation](https://scikit-build-core.readthedocs.io/en/latest/)
- [virtualenvwrapper Guide](https://virtualenvwrapper.readthedocs.io/en/latest/)
- [CMake Documentation](https://cmake.org/documentation/)
