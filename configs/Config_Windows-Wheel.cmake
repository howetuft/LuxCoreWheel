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
  MESSAGE(STATUS "LuxCoreWheel - OIDN: ${OIDN_INCLUDE_DIR} / ${oidn_INCLUDE_DIR}")
  include_directories(${OIDN_INCLUDE_DIR})
else()
  MESSAGE(STATUS "LuxCoreWheel - OIDN NOT FOUND")
endif()

SET(CMAKE_BUILD_TYPE "Release")
