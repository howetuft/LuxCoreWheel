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
  circular_buffer
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
  heap
  integer
  interprocess
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
  uuid
  unordered
  utility
  variant
  variant2
  winapi
  xpressive
)

origdir=`cygpath -u $GITHUB_WORKSPACE`/externals/windows

conan_create_recipe() {

  # Create recipe
  local destdir=~/.boost_conan/${1}
  echo "Creating ${destdir}"
  mkdir -p ${destdir}

  sed "s/MODULE/$1/" ${origdir}/boost-base-dep-template.txt > ${destdir}/conanfile.py

  conan source "${destdir}"

}

set -eo pipefail

echo ""
echo "*******************************************"
echo "*            Boost dependencies           *"
echo "*******************************************"
echo ""


# Prerequisite
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
for dep in ${deps[@]}; do
  conan editable add ~/.boost_conan/$dep
done

echo "LuxCoreWheels - BUILDING BOOST"

# Create boost package
boost_destdir=~/.boost_conan/boost
cp -R $origdir/boost-boost ${boost_destdir}
conan source ${boost_destdir}  # Create CMakeLists
conan editable add ${boost_destdir}


echo "*******************************************"
echo "*        Boost dependencies: done         *"
echo "*******************************************"
