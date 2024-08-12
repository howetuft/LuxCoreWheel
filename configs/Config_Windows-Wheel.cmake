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
  MESSAGE(VERBOSE "LuxCoreWheel - OpenImageIO_INCLUDE_DIR: ${OpenImageIO_INCLUDE_DIR}")
  include_directories(${OpenImageIO_INCLUDE_DIR})
else()
  MESSAGE(VERBOSE "LuxCoreWheel - OpenImageIO NOT FOUND")
endif()

find_package(embree REQUIRED)
if (embree_FOUND)
  set(EMBREE_FOUND "TRUE")
  MESSAGE(VERBOSE "LuxCoreWheel - Embree: ${embree_INCLUDE_DIR}")
  include_directories(${embree_INCLUDE_DIR})
else()
  MESSAGE(VERBOSE "LuxCoreWheel - Embree NOT FOUND")
endif()

set(OIDN_FOUND "TRUE")

SET(CMAKE_BUILD_TYPE "Release")
