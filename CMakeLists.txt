cmake_minimum_required(VERSION 3.30.0)
project(luxcore_wrapper)

enable_language(C)
enable_language(CXX)

include(CMakePrintHelpers)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -w")
set(CMAKE_INSTALL_NAME_DIR "$ENV{CMAKE_INSTALL_NAME_DIR}")

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

# Bison/Flex
find_package(BISON REQUIRED)
find_package(FLEX REQUIRED)

# spdlog
find_package(spdlog REQUIRED)
add_definitions(-DSPDLOG_FMT_EXTERNAL=1)
add_definitions(-DSPDLOG_USE_STD_FORMAT=1)
include_directories(${SPDLOG_INCLUDE_DIRS})

# Python
MESSAGE(STATUS "LuxCoreWheel - Python_ROOT_DIR: ${Python_ROOT_DIR}")
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
if (Python_FOUND)
  MESSAGE(STATUS "LuxCoreWheel - Python includes: ${Python_INCLUDE_DIR}")
  include_directories(${Python_INCLUDE_DIR})
  add_definitions(-DBOOST_PYTHON_STATIC_LIB)

  MESSAGE(STATUS "LuxCoreWheel - Python lib dir: ${Python_LIBRARY_DIRS}")
  link_directories(${Python_LIBRARY_DIRS})
else()
  MESSAGE(STATUS "LuxCoreWheel - Python NOT FOUND")
endif()

# If we are here, it means we have found all dependencies
# So let's tell LuxCore all is ok
# and include directories
set(OPENIMAGEIO_FOUND TRUE)
set(EMBREE_FOUND TRUE)
set(OIDN_FOUND TRUE)
set(BLOSC_FOUND TRUE)
include_directories(${OpenImageIO_INCLUDE_DIR})
include_directories(${embree_INCLUDE_DIR})
include_directories(${TBB_INCLUDE_DIR})
set(TBB_LIBRARY "${TBB_LIBRARIES}")  # TBB_LIBRARIES is referenced as TBB_LIBRARY in LuxCore...
set(OPENEXR_LIBRARIES "${OpenEXR_LIBRARIES}")
include_directories(${OpenEXR_INCLUDE_DIR})
include_directories(${ZLIB_INCLUDE_DIR})
include_directories(${oidn_INCLUDE_DIR})
include_directories(${fmt_INCLUDE_DIR})
include_directories(${Blosc_INCLUDE_DIR})

# For caching with MSVC
SET(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT Embedded)
CMAKE_POLICY(SET CMP0141 NEW)

if(APPLE)
  # OpenMP
  find_package(OpenMP REQUIRED)
  include_directories(${OpenMP_CXX_INCLUDE_DIRS})
  include_directories(${OpenMP_C_INCLUDE_DIRS})
  include_directories(${OpenMP_INCLUDE_DIRS})
  cmake_print_variables(OpenMP_CXX_INCLUDE_DIRS OpenMP_C_INCLUDE_DIRS OpenMP_INCLUDE_DIRS)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Xclang -fopenmp")

  include_directories(${OPENEXR_INCLUDE_DIRS})
endif(APPLE)

if(LINUX)
  set(OpenGL_GL_PREFERENCE "LEGACY")
endif(LINUX)

# Add LuxCore
add_subdirectory(LuxCore)

# Add deps targets to LuxCore libs
target_link_libraries(bcd PRIVATE boost::boost Boost::chrono)
target_link_libraries(openvdb PRIVATE boost::boost openexr::openexr)
target_link_libraries(opensubdiv PRIVATE boost::boost)
target_link_libraries(slg-core PRIVATE boost::boost OpenColorIO::OpenColorIO openexr::openexr)
target_link_libraries(slg-kernels PRIVATE boost::boost OpenColorIO::OpenColorIO)
target_link_libraries(slg-film PRIVATE boost::boost OpenColorIO::OpenColorIO)

set(PYLUXCORE_TARGETS
    slg-core slg-film slg-kernels luxrays bcd opensubdiv openvdb
    TBB::TBB MINIZIP::minizip spdlog::spdlog_header_only
    openexr::openexr
    embree openimageio::openimageio PNG::PNG
    c-blosc::c-blosc oidn::oidn Boost::python Boost::atomic
    Boost::chrono Boost::system Boost::filesystem Boost::container
    Boost::date_time Boost::iostreams Boost::program_options Boost::random
    Boost::serialization Boost::thread boost::boost
    OpenColorIO::OpenColorIO
    Python::Module
)
# TODO
    #OpenEXR::IlmImfConfig
    #IlmBase::IlmBaseConfig
    #IlmBase::Half
    #IlmBase::Iex
    #IlmBase::IexMath
    #IlmBase::IlmThread
    #IlmBase::IMath
    #OpenEXR::IlmImf
    #openexr::ilmbase_conan_pkgconfig
    #OpenEXR::IlmImfUtil


if(WIN32 OR LINUX)
  target_link_libraries(pyluxcore PRIVATE ${PYLUXCORE_TARGETS})
endif(WIN32 OR LINUX)


if(APPLE)
  target_link_libraries(pyluxcore ${PYLUXCORE_TARGETS} llvm-openmp::llvm-openmp)
endif(APPLE)

install(TARGETS pyluxcore LIBRARY DESTINATION pyluxcore)
