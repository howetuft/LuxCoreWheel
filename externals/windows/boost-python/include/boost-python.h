#pragma once

#include <vector>
#include <string>


#ifdef _WIN32
  #define BOOST_PYTHON_EXPORT __declspec(dllexport)
#else
  #define BOOST_PYTHON_EXPORT
#endif

BOOST_PYTHON_EXPORT void boost_python();
BOOST_PYTHON_EXPORT void boost_python_print_vector(const std::vector<std::string> &strings);
