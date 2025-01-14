cmake_minimum_required(VERSION 3.15)
project(pycxxwrapper)

# Set the Python version you want to use
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

add_subdirectory(src)

