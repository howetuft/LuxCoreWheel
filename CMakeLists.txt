cmake_minimum_required(VERSION 3.30.0)
project(cmake_wrapper)

enable_language(C)
enable_language(CXX)
set (CMAKE_CXX_STANDARD 14)

add_subdirectory(LuxCore)

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
  find_package(Boost_atomic REQUIRED)
  find_package(Boost_chrono REQUIRED)
  find_package(Boost_system REQUIRED)
  find_package(Boost_filesystem REQUIRED)
  find_package(Boost_container REQUIRED)
  find_package(Boost_date_time REQUIRED)
  find_package(Boost_iostreams REQUIRED)
  find_package(Boost_program_options REQUIRED)
  find_package(Boost_random REQUIRED)
  find_package(Boost_serialization REQUIRED)
  find_package(Boost_thread REQUIRED)
  find_package(Boost_interprocess REQUIRED)
  find_package(Boost REQUIRED)
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
