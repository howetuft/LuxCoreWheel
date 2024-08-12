# CMake variable injection for Windows

# Conan defines OpenImageIO_FOUND, whereas LuxCore
# expects OPENIMAGEIO_FOUND. We will lure LuxCore:
find_package(OpenImageIO REQUIRED)
if (OpenImageIO_FOUND)
  set(OPENIMAGEIO_FOUND "TRUE")
  MESSAGE(VERBOSE "LuxCoreWheel - OpenImageIO_INCLUDE_PATH: ${OpenImageIO_INCLUDE_PATH}")
  include_directories(${OpenImageIO_INCLUDE_PATH})
endif()

find_package(Embree REQUIRED)
if (Embree_FOUND)
  set(EMBREE_FOUND "TRUE")
  MESSAGE(VERBOSE "LuxCoreWheel - Embree: ${Embree_INCLUDE_PATH}")
  include_directories(${Embree_INCLUDE_PATH})
endif()

set(OIDN_FOUND "TRUE")
