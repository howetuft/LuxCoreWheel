# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

###########################################################################
#
# Configuration
#
###########################################################################

# Specialization for wheel Windows

MESSAGE(STATUS "Using Windows wheel settings")

find_package(OpenImageIO REQUIRED)
if (OpenImageIO_FOUND)
  set(OPENIMAGEIO_FOUND "TRUE")
  MESSAGE(STATUS "LuxCoreWheel - OpenImageIO_INCLUDE_DIR: ${OpenImageIO_INCLUDE_DIR}")
  include_directories(${OpenImageIO_INCLUDE_DIR})
else()
  MESSAGE(STATUS "LuxCoreWheel - OpenImageIO NOT FOUND")
endif()

find_package(embree REQUIRED)
if (embree_FOUND)
  set(EMBREE_FOUND "TRUE")
  MESSAGE(STATUS "LuxCoreWheel - Embree: ${embree_INCLUDE_DIR}")
  include_directories(${embree_INCLUDE_DIR})
else()
  MESSAGE(STATUS "LuxCoreWheel - Embree NOT FOUND")
endif()

find_package(tbb REQUIRED)
if (tbb_FOUND)
  set(TBB_FOUND "TRUE")
  MESSAGE(STATUS "LuxCoreWheel - tbb: ${TBB_INCLUDE_DIR}")
  include_directories(${TBB_INCLUDE_DIR})
  set(TBB_LIBRARY "${TBB_LIBRARIES}")  # TBB_LIBRARIES is referenced as TBB_LIBRARY in LuxCore...
else()
  MESSAGE(STATUS "LuxCoreWheel - tbb NOT FOUND")
endif()

find_package(ZLIB REQUIRED)
if (ZLIB_FOUND)
  MESSAGE(STATUS "LuxCoreWheel - ZLIB: ${ZLIB_INCLUDE_DIR}")
  include_directories(${ZLIB_INCLUDE_DIR})
else()
  MESSAGE(STATUS "LuxCoreWheel - ZLIB NOT FOUND")
endif()

find_package(oidn)
if (oidn_FOUND)
  set(OIDN_FOUND "TRUE")
  MESSAGE(STATUS "LuxCoreWheel - OIDN: ${oidn_INCLUDE_DIR}")
  include_directories(${oidn_INCLUDE_DIR})
else()
  MESSAGE(STATUS "LuxCoreWheel - OIDN NOT FOUND")
endif()

add_compile_definitions(SPDLOG_FMT_EXTERNAL)
find_package(fmt)
if (fmt_FOUND)
  set(FMT_FOUND "TRUE")
  MESSAGE(STATUS "LuxCoreWheel - fmt: ${fmt_INCLUDE_DIR}")
  include_directories(${fmt_INCLUDE_DIR})
else()
  MESSAGE(STATUS "LuxCoreWheel - fmt NOT FOUND")
endif()

# Nota: PYTHON_LIBRARY is set by scikit, see pyproject.toml
MESSAGE(STATUS "LuxCoreWheel - Python_ROOT_DIR: ${Python_ROOT_DIR}")
find_package(Python COMPONENTS Interpreter Development.Module)
if (Python_FOUND)
  MESSAGE(STATUS "LuxCoreWheel - Python includes: ${Python_INCLUDE_DIR}")
  include_directories(${Python_INCLUDE_DIR})
  add_definitions(-DBOOST_PYTHON_STATIC_LIB)

  MESSAGE(STATUS "LuxCoreWheel - Python lib dir: ${Python_LIBRARY_DIRS}")
  link_directories(${Python_LIBRARY_DIRS})
else()
  MESSAGE(STATUS "LuxCoreWheel - Python NOT FOUND")
endif()

SET(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "Embedded")
CMAKE_POLICY(SET CMP0141 NEW)

SET(CMAKE_BUILD_TYPE "Release")


# Replaces Dependencies.cmake
find_package(TIFF REQUIRED)
include_directories(BEFORE SYSTEM ${TIFF_INCLUDE_DIR})
find_package(JPEG REQUIRED)
include_directories(BEFORE SYSTEM ${JPEG_INCLUDE_DIR})
find_package(PNG REQUIRED)
include_directories(BEFORE SYSTEM ${PNG_PNG_INCLUDE_DIR})
find_package(Threads REQUIRED)

find_program(PYSIDE_UIC NAMES pyside-uic pyside2-uic pyside6-uic
		HINTS "${Python3_INCLUDE_DIRS}/../Scripts"
		PATHS "c:/Program Files/Python${PYTHON_V}/Scripts")
# Find Boost
set(Boost_USE_STATIC_LIBS       ON)
set(Boost_USE_MULTITHREADED     ON)
set(Boost_USE_STATIC_RUNTIME    OFF)
set(BOOST_ROOT                  "${BOOST_SEARCH_PATH}")
#set(Boost_DEBUG                 ON)
set(Boost_MINIMUM_VERSION       "1.56.0")

# For Windows builds, PYTHON_V must be defined as "3x" (x=Python minor version, e.g. "35")
# For other platforms, specifying python minor version is not needed
set(LUXRAYS_BOOST_COMPONENTS thread program_options filesystem serialization iostreams regex system python${PYTHON_V} chrono serialization numpy${PYTHON_V})
find_package(Boost ${Boost_MINIMUM_VERSION} COMPONENTS ${LUXRAYS_BOOST_COMPONENTS})
if (NOT Boost_FOUND)
        # Try again with the other type of libs
        if(Boost_USE_STATIC_LIBS)
                set(Boost_USE_STATIC_LIBS OFF)
        else()
                set(Boost_USE_STATIC_LIBS ON)
        endif()
        # The following line is necessary with CMake 3.18.0 to find static libs on Windows
        unset(Boost_LIB_PREFIX)
        message(STATUS "Re-trying with link static = ${Boost_USE_STATIC_LIBS}")
        find_package(Boost ${Boost_MINIMUM_VERSION} COMPONENTS ${LUXRAYS_BOOST_COMPONENTS})
endif()

if (Boost_FOUND)
	include_directories(BEFORE SYSTEM ${Boost_INCLUDE_DIRS})
	link_directories(${Boost_LIBRARY_DIRS})
	# Don't use old boost versions interfaces
	ADD_DEFINITIONS(-DBOOST_FILESYSTEM_NO_DEPRECATED)
	if (Boost_USE_STATIC_LIBS)
		ADD_DEFINITIONS(-DBOOST_STATIC_LIB)
		ADD_DEFINITIONS(-DBOOST_PYTHON_STATIC_LIB)
	endif()
endif ()


# OpenGL
find_package(OpenGL)

if (OPENGL_FOUND)
	include_directories(BEFORE SYSTEM ${OPENGL_INCLUDE_PATH})
endif ()

find_package(OpenMP)
if (OPENMP_FOUND)
        MESSAGE(STATUS "OpenMP found - compiling with")
        set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
        set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
else()
        MESSAGE(WARNING "OpenMP not found - compiling without")
endif()

# Blosc
find_package(Blosc)
if (Blosc_FOUND)
  MESSAGE(STATUS "Blosc found - compiling with (${Blosc_INCLUDE_DIR})")
  set(BLOSC_FOUND "True")
  include_directories(${Blosc_INCLUDE_DIR})
else()
  MESSAGE(WARNING "Blosc not found")
endif()

## Conan
#find_package(TBB)
#find_package(minizip)
#find_package(OpenMP)
#find_package(spdlog)
#find_package(OpenImageIO)
#find_package(PNG)
#find_package(OpenColorIO)
#find_package(embree)
#find_package(Blosc)
#find_package(OPENEXR)
#find_package(oidn)
#find_package(Boost_python)
#find_package(Boost_atomic)
#find_package(Boost_chrono)
#find_package(Boost_system)
#find_package(Boost_filesystem)
#find_package(Boost_container)
#find_package(Boost_date_time)
#find_package(Boost_iostreams)
#find_package(Boost_program_options)
#find_package(Boost_random)
#find_package(Boost_serialization)
#find_package(Boost_thread)
#find_package(Boost)

## Includes
#include_directories(${OpenColorIO_INCLUDE_DIR})
