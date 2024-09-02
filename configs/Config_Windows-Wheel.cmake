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
