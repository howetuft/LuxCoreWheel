# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

#!/bin/bash

# For local debug, run this before:
# rm ~/.conan2/editable_packages.json

deps=(
  algorithm
  align
  any
  array
  assert
  asio
  atomic
  bimap
  bind
  chrono
  concept_check
  config
  container
  container_hash
  context
  conversion
  core
  coroutine
  date_time
  describe
  detail
  dynamic_bitset
  endian
  exception
  filesystem
  foreach
  format
  function
  function_types
  fusion
  graph
  integer
  intrusive
  io
  iostreams
  iterator
  lambda
  lexical_cast
  math
  move
  mpl
  mp11
  multi_index
  numeric_conversion
  optional
  parameter
  phoenix
  pool
  predef
  preprocessor
  program_options
  property_map
  property_tree
  proto
  python
  random
  range
  ratio
  rational
  regex
  serialization
  smart_ptr
  spirit
  stacktrace
  static_assert
  system
  thread
  throw_exception
  tokenizer
  tti
  tuple
  type_traits
  type_index
  typeof
  unordered
  utility
  variant
  variant2
  winapi
  xpressive
)

conan_create_recipe() {

  # Create recipe
  local destdir=~/.boost_conan/${1}
  echo "Creating ${destdir}"
  mkdir -p ${destdir}

  sed "s/MODULE/$1/" boost-base-dep-template.txt > ${destdir}/conanfile.py

  conan source "${destdir}"
}

conan_build_recipe() {
  local destdir=~/.boost_conan/${1}

  conan editable add $destdir
  #conan install "${destdir}" -s build_type=Release
  #conan build "${destdir}"

  echo "LuxCoreWheels - Module ${1} created in ${destdir}"

}

set -eo pipefail

echo ""
echo "*******************************************"
echo "*            Boost dependencies           *"
echo "*******************************************"
echo ""

# Prerequisite
#conan install --requires boost/1.78.0
conan install --requires "zlib/[>=1.2.11 <2]"

# Launch parallel build
pids=()
for i in ${!deps[@]}; do
  dep=${deps[$i]}
  conan_create_recipe $dep &
  pids[${i}]=$!
done

# Wait for all treatments to finish
for pid in ${pids[*]}; do
    wait $pid
done

# Put in editable mode (warning: conan not thread-safe, do not parallelize)
#cd ~/.boost_conan
for dep in ${deps[@]}; do
  conan_build_recipe $dep
done

echo "LuxCoreWheels - BUILDING BOOST"

# Create boost package
boost_destdir=~/.boost_conan/boost
cp -R boost-boost ${boost_destdir}
conan editable add ${boost_destdir}
conan install ${boost_destdir} --build=editable -s build_type=Release
conan build ${boost_destdir} -s build_type=Release


echo "*******************************************"
echo "*        Boost dependencies: done         *"
echo "*******************************************"
