cmake_minimum_required(VERSION 3.0)
project(PhysicsGameV2)

find_package(pybind11 REQUIRED)
set(CMAKE_CXX_STANDARD 14)

pybind11_add_module(physics bindings.cpp physics.cpp)