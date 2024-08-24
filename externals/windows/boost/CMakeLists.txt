cmake_minimum_required(VERSION 3.15)
project(boost-python CXX)




add_library(boost-python src/boost-python.cpp)
target_include_directories(boost-python PUBLIC include)



set_target_properties(boost-python PROPERTIES PUBLIC_HEADER "include/boost-python.h")
install(TARGETS boost-python)
