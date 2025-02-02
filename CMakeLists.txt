# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.30.0)
project(luxcore_wrapper NONE)

include(CMakePrintHelpers)
cmake_print_variables(CMAKE_BUILD_TYPE)
cmake_print_variables(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT)
cmake_print_variables(CMAKE_CXX_FLAGS)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -w")
set(CMAKE_INSTALL_NAME_DIR "$ENV{CMAKE_INSTALL_NAME_DIR}")

# Set options
set(BUILD_LUXCORE_DLL ON)
set(LUXCORE_PYLUXCORE ON)
set(LUXRAYS_ENABLE_OPENCL TRUE)
set(LUXRAYS_ENABLE_CUDA TRUE)
set(LUXRAYS_ENABLE_OPTIX TRUE)


# Add LuxCore
add_subdirectory(LuxCore)


# Add sanitizer (optional - only for Linux)
if ((DEFINED ENV{SANITIZE}) AND LINUX)
  message(STATUS "Linking with asan")
  add_library(asan SHARED IMPORTED)
  set_property(TARGET asan PROPERTY
    IMPORTED_LOCATION
    $ENV{ASAN_PATH}
  )
  set(HAVE_SANITIZER TRUE)
endif()

target_link_libraries(pyluxcore PRIVATE $<$<BOOL:${HAVE_SANITIZER}>:asan>)
target_link_options(pyluxcore PRIVATE $<$<BOOL:${HAVE_SANITIZER}>:-fsanitize=address>)

# Installation

# Pyluxcore
INSTALL(TARGETS pyluxcore DESTINATION pyluxcore)


# oidnDenoise (much more work...)
add_executable(oidn-denoise IMPORTED)
set_property(TARGET oidn-denoise PROPERTY IMPORTED_LOCATION "${LUX_OIDN_DENOISE_PATH}")

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

  # Delvewheel doesn't handle executables, however we need to delocate oidnDenoise.
  # Therefore we had to let Delvewheel believe oidnDenoise is a lib, and now
  # we have to make it an executable again...
  message(STATUS "oidnDenoise suffix back to pyd")
  INSTALL(CODE "file(RENAME \"${CMAKE_INSTALL_PREFIX}/pyluxcore.libs/oidnDenoise.exe\" \"${CMAKE_INSTALL_PREFIX}/pyluxcore.libs/oidnDenoise.pyd\")")

endif(WIN32)
