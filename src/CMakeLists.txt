cmake_minimum_required(VERSION 3.15)
project(pycxxwrapper)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Policy to suppress FindBoost warning
if(POLICY CMP0167)
    cmake_policy(SET CMP0167 NEW)
endif()

# # Add Python include paths
# set(CPLUS_INCLUDE_PATH "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/include/python3.13:${CPLUS_INCLUDE_PATH}")
# include_directories(${CPLUS_INCLUDE_PATH})
#
# # Add pybind11 include paths
# set(CPLUS_INCLUDE_PATH "/opt/homebrew/opt/pybind11/include:${CPLUS_INCLUDE_PATH}")
# include_directories(${CPLUS_INCLUDE_PATH})

# Find Pybind11 package
find_package(Python3 COMPONENTS Development REQUIRED)
find_package(pybind11 REQUIRED)
find_package(Boost REQUIRED)

# Add the Pybind11 module
# pybind11_add_module(toy toy.cpp)
pybind11_add_module(boost_wrapper MODULE shortest_path.cpp)

# Set the output directory for the shared libraries
set_target_properties(boost_wrapper PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/src)

# Specify the installation directory for the module
install(
    TARGETS boost_wrapper
    DESTINATION pycxxwrapper
)

