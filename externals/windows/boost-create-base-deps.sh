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
  bind
  concept_check
  config
  container_hash
  conversion
  core
  detail
  dynamic_bitset
  exception
  foreach
  function
  graph
  integer
  intrusive
  io
  iterator
  lexical_cast
  move
  mpl
  numeric_conversion
  optional
  parameter
  predef
  preprocessor
  property_map
  range
  ratio
  regex
  smart_ptr
  spirit
  static_assert
  system
  throw_exception
  tokenizer
  tuple
  type_traits
  type_index
  typeof
  unordered
  utility
  variant
  winapi
)

conan_create_recipe() {

  # Create recipe
  local destdir=~/.boost_conan/${1}
  echo "Creating ${destdir}"
  mkdir -p ${destdir}

  sed "s/MODULE/$1/" boost-base-dep-template.txt > ${destdir}/conanfile.py

  # Put in editable mode, install and source
  #
  # Keep install before source, otherwise settings.build_type won't be set
  # when running layout()
  conan editable add $destdir
}

conan_build_recipe() {
  local destdir=~/.boost_conan/${1}

  conan install "${destdir}" -s build_type=Release
  conan source "${destdir}"
  #conan build "${destdir}"

  echo "LuxCoreWheels - Module ${1} created in ${destdir}"

}

echo ""
echo "*******************************************"
echo "*         Boost base dependencies         *"
echo "*******************************************"
echo ""

# Prerequisite
#conan install --requires boost/1.78.0
conan install --requires "zlib/[>=1.2.11 <2]"

# Put in editable mode (warning: conan not thread-safe, do not parallelize)
#cd ~/.boost_conan
for dep in ${deps[@]}; do
  conan_create_recipe $dep
done

# Launch parallel build
pids=()
for i in ${!deps[@]}; do
  dep=${deps[$i]}
  conan_build_recipe $dep &
  pids[${i}]=$!
done

# Wait for all treatments to finish
for pid in ${pids[*]}; do
    wait $pid
done


echo "Boost base dependencies: done"
