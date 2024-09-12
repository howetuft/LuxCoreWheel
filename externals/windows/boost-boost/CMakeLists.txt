cmake_minimum_required(VERSION 3.5...3.16)

project(Boost VERSION 1.78.0 LANGUAGES CXX)

add_library(boost INTERFACE)
add_library(Boost ALIAS boost)

target_link_libraries(boost
  INTERFACE
    Boost::thread
    Boost::program_options
    Boost::filesystem
    Boost::iostreams
    Boost::regex
    Boost::system
    Boost::python
    Boost::chrono
    Boost::serialization
)

