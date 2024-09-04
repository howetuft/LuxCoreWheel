cmake_minimum_required(VERSION 30)
project(cmake_wrapper)

enable_language(C)
enable_language(CXX)
set (CMAKE_CXX_STANDARD 14)

include(conanbuildinfo.cmake)
conan_basic_setup(KEEP_RPATHS)

add_subdirectory(LuxCore)
