cmake_minimum_required(VERSION 3.30.0)
project(cmake_wrapper)

enable_language(C)
enable_language(CXX)
set (CMAKE_CXX_STANDARD 17)

add_subdirectory(LuxCore)

if(WIN32)
  message(STATUS "LuxCoreWheel - Add conan targets")
  target_link_libraries(pyluxcore PRIVATE
    slg-core slg-film slg-kernels luxrays bcd opensubdiv openvdb
    TBB::TBB MINIZIP::minizip llvm-openmp::llvm-openmp spdlog::spdlog
    openimageio::openimageio PNG::PNG OpenColorIO::OpenColorIO embree
    c-blosc::c-blosc openexr::openexr oidn::oidn Boost::python Boost::atomic
    Boost::chrono Boost::system Boost::filesystem Boost::container
    Boost::date_time Boost::iostreams Boost::program_options Boost::random
    Boost::serialization Boost::thread boost::boost
  )
endif(WIN32)
