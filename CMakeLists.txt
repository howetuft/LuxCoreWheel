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

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -w")
set(CMAKE_INSTALL_NAME_DIR "$ENV{CMAKE_INSTALL_NAME_DIR}")
set(BUILD_LUXCORE_DLL 1)
set(LUXRAYS_ENABLE_OPENCL TRUE)
set(LUXRAYS_ENABLE_CUDA TRUE)
set(LUXRAYS_ENABLE_OPTIX TRUE)
unset(LUXRAYS_DISABLE_OPENCL)
unset(LUXRAYS_DISABLE_CUDA)
unset(LUXRAYS_DISABLE_OPTIX)


# Add LuxCore
add_subdirectory(LuxCore)

# sanitize


# Add deps targets to LuxCore libs
target_link_libraries(luxrays embree openimageio::openimageio boost::boost)
target_link_libraries(bcd PRIVATE boost::boost Eigen3::Eigen)
target_link_libraries(slg-core PRIVATE
    boost::boost
    OpenColorIO::OpenColorIO
    OpenVDB::openvdb
    openexr::openexr
    opensubdiv::opensubdiv
    Imath::Imath
    embree
    openimageio::openimageio
    nlohmann_json::nlohmann_json
    robin_hood::robin_hood
)
target_link_libraries(slg-kernels PRIVATE boost::boost)
target_link_libraries(slg-film PRIVATE
    boost::boost
    OpenColorIO::OpenColorIO
    embree
    oidn::oidn
    openimageio::openimageio
)

if ((DEFINED ENV{SANITIZE}) AND LINUX)
  message(STATUS "Linking with asan")
  add_library(asan SHARED IMPORTED)
  set_property(TARGET asan PROPERTY
    IMPORTED_LOCATION
    $ENV{ASAN_PATH}
  )
  set(HAVE_SANITIZER TRUE)
endif()


if(APPLE)
  target_link_libraries(bcd PRIVATE llvm-openmp::llvm-openmp)
  target_link_libraries(slg-core PRIVATE llvm-openmp::llvm-openmp)
  target_link_libraries(pyluxcore PRIVATE llvm-openmp::llvm-openmp)
else()
  target_link_libraries(bcd PRIVATE OpenMP::OpenMP_CXX)
endif(APPLE)


# oidnDenoise
add_executable(oidn-denoise IMPORTED)
set_property(TARGET oidn-denoise PROPERTY IMPORTED_LOCATION "${LUX_OIDN_DENOISE_PATH}")


# Installation

# Pyluxcore
INSTALL(TARGETS pyluxcore DESTINATION pyluxcore)


# oidnDenoise (much more work...)
if(WIN32)
  # Windows lacks rpath system, so we have to put oidnDenoise in the same
  # folder as the dlls...
  set(OIDN_DESTINATION "pyluxcore.libs")
else()
  # For Macos, reminder: don't put it in pyluxcore/.dylibs, it would prevent
  # other deps' relocation
  set(OIDN_DESTINATION "pyluxcore.oidn")
endif(WIN32)

if(LINUX)
  set_property(
    TARGET oidn-denoise
    PROPERTY INSTALL_RPATH "\\\${ORIGIN}/../pyluxcore.libs"
  )
  install(
    PROGRAMS "${LUX_OIDN_DENOISE_CPU}"
    DESTINATION "pyluxcore.libs"
  )
endif(LINUX)

if(APPLE)
  set_target_properties(
    oidn-denoise PROPERTIES
    INSTALL_RPATH "\\\${ORIGIN}/../pyluxcore/.pylibs"
    BUILD_RPATH ""
  )
endif(APPLE)

INSTALL(
  IMPORTED_RUNTIME_ARTIFACTS oidn-denoise
  DESTINATION ${OIDN_DESTINATION}
  PERMISSIONS
    OWNER_WRITE OWNER_READ OWNER_EXECUTE
    GROUP_READ GROUP_EXECUTE
    WORLD_READ WORLD_EXECUTE
)


if(WIN32)
  # For Win32, we need to add device_cpu
  # device_cpu should first have a pyd extension to be repaired.
  # This will be reverted after repairing
  install(
    PROGRAMS "${LUX_OIDN_DENOISE_BINS}/OpenImageDenoise_device_cpu.dll"
    DESTINATION "pyluxcore.libs"
    RENAME "OpenImageDenoise_device_cpu.pyd"
  )
  # TODO
  #add_library(oidn-device-cpu SHARED IMPORTED)
  #set_target_properties(
    #oidn-device-cpu PROPERTIES
    #IMPORTED_LOCATION "${LUX_OIDN_DENOISE_BINS}/OpenImageDenoise_device_cpu.dll"
    #OUTPUT_NAME "OpenImageDenoise_device_cpu.pyd"
  #)
  #INSTALL(
    #IMPORTED_RUNTIME_ARTIFACTS oidn-device-cpu
    #DESTINATION "pyluxcore.libs"
    #PERMISSIONS
      #OWNER_WRITE OWNER_READ OWNER_EXECUTE
      #GROUP_READ GROUP_EXECUTE
      #WORLD_READ WORLD_EXECUTE
  #)

  # Delvewheel doesn't handle executables, however we need to delocate oidnDenoise.
  # Therefore we had to let Delvewheel believe oidnDenoise is a lib, and now
  # we have to make it an executable again...
  message(STATUS "oidnDenoise suffix back to pyd")
  INSTALL(CODE "file(RENAME \"${CMAKE_INSTALL_PREFIX}/pyluxcore.libs/oidnDenoise.exe\" \"${CMAKE_INSTALL_PREFIX}/pyluxcore.libs/oidnDenoise.pyd\")")

  # TODO
  # device_cpu should have a pyd extension
  #INSTALL(CODE "file(RENAME \"${CMAKE_INSTALL_PREFIX}/pyluxcore.libs/OpenImageDenoise_device_cpu.dll\" \"${CMAKE_INSTALL_PREFIX}/pyluxcore.libs/OpenImageDenoise_device_cpu.pyd\")")
  # This will be reverted after repairing
endif(WIN32)
