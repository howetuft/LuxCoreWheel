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

target_link_libraries(boost
  INTERFACE
    Boost::algorithm
    Boost::align
    Boost::any
    Boost::array
    Boost::assert
    Boost::bimap
    Boost::bind
    Boost::concept_check
    Boost::config
    Boost::container
    Boost::container_hash
    Boost::conversion
    Boost::core
    Boost::describe
    Boost::detail
    Boost::dynamic_bitset
    Boost::foreach
    Boost::format
    Boost::function
    Boost::fusion
    Boost::integer
    Boost::intrusive
    Boost::io
    Boost::iterator
    Boost::lexical_cast
    Boost::move
    Boost::mpl
    Boost::mp11
    Boost::multi_index
    Boost::numeric_conversion
    Boost::optional
    Boost::parameter
    Boost::predef
    Boost::preprocessor
    Boost::property_map
    Boost::proto
    Boost::range
    Boost::ratio
    Boost::regex
    Boost::smart_ptr
    Boost::spirit
    Boost::static_assert
    Boost::system
    Boost::throw_exception
    Boost::tokenizer
    Boost::tti
    Boost::tuple
    Boost::type_traits
    Boost::type_index
    Boost::typeof
    Boost::unordered
    Boost::utility
    Boost::variant
    Boost::winapi
    Boost::xpressive
)
