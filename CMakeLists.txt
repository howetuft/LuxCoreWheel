cmake_minimum_required(VERSION 30)
project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup(KEEP_RPATHS)

add_subdirectory(LuxCore)
