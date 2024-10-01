cmake_minimum_required(VERSION 3.30.0)
project(luxcore_wrapper)

enable_language(C)
enable_language(CXX)
set (CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -w")


if(WIN32)
  message(STATUS "LuxCoreWheel - Add conan targets")
  find_package(TBB REQUIRED)
  find_package(minizip REQUIRED)
  find_package(spdlog REQUIRED)
  find_package(openimageio REQUIRED)
  find_package(PNG REQUIRED)
  find_package(OpenColorIO REQUIRED)
  find_package(OpenEXR)
  find_package(embree REQUIRED)
  find_package(Blosc REQUIRED)
  find_package(oidn REQUIRED)
  find_package(Boost_python REQUIRED)
  find_package(Boost REQUIRED)

  # Python
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
  include_directories(${ZLIB_INCLUDE_DIR})
  include_directories(${oidn_INCLUDE_DIR})
  include_directories(${fmt_INCLUDE_DIR})
  include_directories(${Blosc_INCLUDE_DIR})

  SET(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "Embedded")
  CMAKE_POLICY(SET CMP0141 NEW)
endif(WIN32)


if(UNIX)
  MESSAGE(STATUS "LuxCoreWheel: using Linux settings")

  # TODO Harmonize with WIN32?
  find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)
  include_directories(${Python3_INCLUDE_DIRS})

  set(OpenGL_GL_PREFERENCE "LEGACY")
  set(BOOST_LIBRARYDIR "/usr/lib64/boost1.78;/usr/lib64" CACHE PATH "" FORCE)
  set(BOOST_INCLUDEDIR "/usr/include/boost1.78;/usr/lib64" CACHE PATH "" FORCE)
  set(Boost_NO_SYSTEM_PATHS ON CACHE BOOL "" FORCE)
  set(PYTHON_V "36")
  set(EMBREE_SEARCH_PATH "/usr/lib64")
  SET(CMAKE_INCLUDE_PATH "${LuxRays_SOURCE_DIR}/../target-64-sse2/include;${LuxRays_SOURCE_DIR}/../target-64-sse2")
  SET(CMAKE_LIBRARY_PATH "${LuxRays_SOURCE_DIR}/../target-64-sse2/lib;${LuxRays_SOURCE_DIR}/../target-64-sse2")
  SET(Blosc_USE_STATIC_LIBS   "ON")
  SET(CMAKE_BUILD_TYPE "Release")
endif(UNIX)

# Add LuxCore
add_subdirectory(LuxCore)

# Add deps targets to LuxCore libs
if(WIN32)

  target_link_libraries(bcd PRIVATE boost::boost)
  target_link_libraries(openvdb PRIVATE boost::boost)
  target_link_libraries(opensubdiv PRIVATE boost::boost)
  target_link_libraries(slg-core PRIVATE boost::boost OpenColorIO::OpenColorIO)
  target_link_libraries(slg-kernels PRIVATE boost::boost)
  target_link_libraries(slg-film PRIVATE boost::boost OpenColorIO::OpenColorIO)
  target_link_libraries(pyluxcore PRIVATE
    slg-core slg-film slg-kernels luxrays bcd opensubdiv openvdb
    TBB::TBB MINIZIP::minizip spdlog::spdlog_header_only
    openexr::openexr
    OpenEXR::IlmImfConfig
    IlmBase::IlmBaseConfig
    IlmBase::Half
    IlmBase::Iex
    IlmBase::IexMath
    IlmBase::IlmThread
    IlmBase::IMath
    OpenEXR::IlmImf
    openexr::ilmbase_conan_pkgconfig
    OpenEXR::IlmImfUtil
    embree openimageio::openimageio PNG::PNG
    c-blosc::c-blosc oidn::oidn Boost::python Boost::atomic
    Boost::chrono Boost::system Boost::filesystem Boost::container
    Boost::date_time Boost::iostreams Boost::program_options Boost::random
    Boost::serialization Boost::thread boost::boost
    OpenColorIO::OpenColorIO
  )
endif(WIN32)

if(UNIX)
  set(BOOST_INCLUDEDIR "/usr/include/boost1.78" CACHE PATH "" FORCE)
endif(UNIX)

install(TARGETS pyluxcore LIBRARY DESTINATION lib)

