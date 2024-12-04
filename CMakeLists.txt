# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.30.0)
project(luxcore_wrapper)

enable_language(C)
enable_language(CXX)

include(CMakePrintHelpers)
cmake_print_variables(CMAKE_BUILD_TYPE)
cmake_print_variables(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT)
cmake_print_variables(CMAKE_CXX_FLAGS)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -w")
set(CMAKE_INSTALL_NAME_DIR "$ENV{CMAKE_INSTALL_NAME_DIR}")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

set(CMAKE_VERBOSE_MAKEFILE ON)
set(BUILD_LUXCORE_DLL 1)
set(LUXRAYS_ENABLE_OPENCL TRUE)
set(LUXRAYS_ENABLE_CUDA TRUE)
set(LUXRAYS_ENABLE_OPTIX TRUE)
unset(LUXRAYS_DISABLE_OPENCL)
unset(LUXRAYS_DISABLE_CUDA)
unset(LUXRAYS_DISABLE_OPTIX)
cmake_policy(SET CMP0074 NEW)  # *_ROOT variable

message(STATUS "LuxCoreWheel - Add conan targets")
find_package(TBB REQUIRED)
find_package(minizip REQUIRED)
find_package(spdlog REQUIRED)
find_package(OpenImageIO REQUIRED)
find_package(PNG REQUIRED)
find_package(OpenColorIO REQUIRED)
find_package(OpenEXR REQUIRED)
find_package(embree REQUIRED)
find_package(Blosc REQUIRED)
find_package(oidn REQUIRED)
find_package(Boost_python REQUIRED)
find_package(Boost REQUIRED)
find_package(OpenVDB REQUIRED)
find_package(Imath REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(blender-types REQUIRED)

# Bison/Flex
find_package(BISON REQUIRED)
find_package(FLEX REQUIRED)

# Python
MESSAGE(STATUS "LuxCoreWheel - Python_ROOT_DIR: ${Python_ROOT_DIR}")
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

# If we are here, it means we have found all dependencies
# So let's tell LuxCore all is ok
set(OPENIMAGEIO_FOUND TRUE)
set(EMBREE_FOUND TRUE)
set(OIDN_FOUND TRUE)
set(BLOSC_FOUND TRUE)

if(APPLE)
  # OpenMP
  find_package(OpenMP REQUIRED)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Xclang -fopenmp")
endif(APPLE)

if(LINUX)
  set(OpenGL_GL_PREFERENCE "LEGACY")
endif(LINUX)

if(MSVC)
  # Minimizes Windows header files
  #ADD_DEFINITIONS(-DWIN32_LEAN_AND_MEAN)
  # Do not define MIN and MAX macros
  ADD_DEFINITIONS(-DNOMINMAX)
  # Do not warn about standard but insecure functions
  ADD_DEFINITIONS(-D_CRT_SECURE_NO_WARNINGS -D_SCL_SECURE_NO_WARNINGS)
  # Enable Unicode
  ADD_DEFINITIONS(-D_UNICODE)
  # Enable SSE2/SSE/MMX
  ADD_DEFINITIONS(-D__SSE2__ -D__SSE__ -D__MMX__)
  add_link_options("/INCREMENTAL:NO" "/PDBALTPATH:%_PDB%")
endif(MSVC)

# Add LuxCore
add_subdirectory(LuxCore)

# Add deps targets to LuxCore libs
target_link_libraries(luxrays embree openimageio::openimageio boost::boost)
target_link_libraries(opensubdiv PRIVATE boost::boost)
target_link_libraries(bcd PRIVATE boost::boost Eigen3::Eigen)
target_link_libraries(slg-core PRIVATE
    boost::boost
    OpenColorIO::OpenColorIO
    OpenVDB::openvdb
    openexr::openexr
    Imath::Imath
    embree
    openimageio::openimageio
)
target_link_libraries(slg-kernels PRIVATE boost::boost)
target_link_libraries(slg-film PRIVATE
    boost::boost
    OpenColorIO::OpenColorIO
    embree
    oidn::oidn
    openimageio::openimageio
)

target_link_libraries(pyluxcore PRIVATE
    slg-core
    slg-film
    slg-kernels
    luxrays
    bcd
    opensubdiv
    OpenVDB::openvdb
    spdlog::spdlog_header_only
    Boost::python
    boost::boost
    Python::Module
    blender-types
)
set_property(TARGET pyluxcore PROPERTY CXX_STANDARD 17)

if(APPLE)
  target_link_libraries(opensubdiv PRIVATE llvm-openmp::llvm-openmp)
  target_link_libraries(bcd PRIVATE llvm-openmp::llvm-openmp)
  target_link_libraries(slg-core PRIVATE llvm-openmp::llvm-openmp)
  target_link_libraries(pyluxcore PRIVATE llvm-openmp::llvm-openmp)
endif(APPLE)

INSTALL(TARGETS pyluxcore DESTINATION pyluxcore)
