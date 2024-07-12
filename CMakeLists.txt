cmake_minimum_required(VERSION 3.15...3.27)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

#Python_add_library(pyluxcore MODULE WITH_SOABI)
# install(TARGETS _module DESTINATION ${SKBUILD_PROJECT_NAME})

add_subdirectory(LuxCore)
