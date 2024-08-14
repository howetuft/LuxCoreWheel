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

find_package(onetbb REQUIRED)
if (onetbb_FOUND)
  set(TBB_FOUND "TRUE")
  MESSAGE(STATUS "LuxCoreWheel - Onetbb: ${onetbb_INCLUDE_DIR}")
  include_directories(${onetbb_INCLUDE_DIR})
else()
  MESSAGE(STATUS "LuxCoreWheel - Onetbb NOT FOUND")
endif()

set(OIDN_FOUND "TRUE")

SET(CMAKE_BUILD_TYPE "Release")
