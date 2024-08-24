cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

find_package(boost-python CONFIG REQUIRED)

add_executable(example src/example.cpp)
target_link_libraries(example boost-python::boost-python)
