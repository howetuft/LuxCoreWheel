# CMake variable injection for Windows

# Conan defines OpenImageIO_FOUND, whereas LuxCore
# expects OPENIMAGEIO_FOUND. We will lure LuxCore:
find_package(OpenImageIO REQUIRED)
if (OpenImageIO_FOUND)
  set(OPENIMAGEIO_FOUND "TRUE")
  MESSAGE(VERBOSE "LuxCoreWheel - OpenImageIO_INCLUDE_PATH: ${OIIO_INCLUDE_DIR}")
  include_directories(${OpenImageIO_INCLUDE_DIR})
endif()

find_package(Embree REQUIRED)
if (EMBREE_FOUND)
  set(EMBREE_FOUND "TRUE")
  MESSAGE(VERBOSE "LuxCoreWheel - Embree: ${EMBREE_INCLUDE_DIR}")
  include_directories(${EMBREE_INCLUDE_DIR})
endif()

set(OIDN_FOUND "TRUE")
