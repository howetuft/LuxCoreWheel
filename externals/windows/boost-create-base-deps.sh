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
  foreach
  function
  integer
  intrusive
  io
  iterator
  lexical_cast
  move
  mpl
  numeric_conversion
  optional
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
  typeof
  unordered
  utility
  variant
  winapi
)

conan_create() {

  # Create recipe
  local destdir=~/.boost_conan/${1}
  echo "${destdir}"
  mkdir -p ${destdir}

  sed "s/MODULE/$1/" boost-base-dep-template.txt > ${destdir}/conanfile.py

  # Create
  conan install "${destdir}" -s build_type=Release
  conan source "${destdir}"
  conan build "${destdir}"

  echo "Module ${1} created in ${destdir}"

}

# Prerequisite
conan install --requires boost/1.78.0

# Launch parallel treatments
pids=()
for i in ${!deps[@]}; do
  dep=${deps[$i]}
  conan_create $dep & # Here
  pids[${i}]=$!
done

# Wait for all treatments to finish
for pid in ${pids[*]}; do
    wait $pid
done

# Put in editable mode (warning: conan not thread-safe, do not parallelize)
cd ~/.boost_conan
for dep in ${deps[@]}; do
  conan editable add $dep
done

echo "Boost base dependencies: done"
