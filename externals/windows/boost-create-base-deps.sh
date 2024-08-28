# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

#!/bin/bash

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

conan_treatment() {
  conan create "boost-$1"
}

# Prerequisite
conan install --requires boost/1.78.0

# Launch parallel treatments
pids=()
N=4
for i in ${!deps[@]}; do
  ((j=j%N)); ((j++==0)) && wait  # N process batches
  dep=${deps[$i]}
  conan_treatment $dep &
  pids[${i}]=$!
done

# Wait for all treatments to finish
for pid in ${pids[*]}; do
    wait $pid
done

echo "Boost base dependencies: done"
