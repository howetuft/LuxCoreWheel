#!/bin/bash

cd boost-config
conan create .

cd ../boost-align
conan create .

cd ../boost-bind
conan create .

cd ../boost-config
conan create .

cd ../boost-conversion
conan create .

cd ../boost-core
conan create .

cd ../boost-detail
conan create .

cd ../boost-foreach
conan create .

cd ../boost
conan create .

cd ../boost-function
conan create .

cd ../boost-iterator
conan create .

cd ../boost-lexical_cast
conan create .

cd ../boost-mpl
conan create .

cd ../boost-numeric_conversion
conan create .

cd ../boost-preprocessor
conan create .

cd ../boost-smart_ptr
conan create .

cd ../boost-static_assert
conan create .

cd ../boost-tuple
conan create .

cd ../boost-type_traits
conan create .

cd ../boost-utility
conan create .

#####################""

cd ../boost-python
conan create .
