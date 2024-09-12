# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

#!/bin/bash

# For local debug, run this before:
# rm ~/.conan2/editable_packages.json
# rm -rf ~/.boost_conan

#deps=(
  #random
  #python
  #atomic
  #chrono
  #filesystem
  #container
  #date_time
  #iostreams
  #program_options
  #serialization
  #thread
#)



deps=(
  exception
  atomic
  container
  date_time
  random
  math
  chrono
  iostreams
  thread
  serialization
  property_tree
  filesystem
  graph
  program_options
  python
  boost
)

conan_create_recipe() {
  local destdir=~/.boost_conan/${1}
  cp -R boost-${1} ${destdir}
  conan editable add "${destdir}"
  echo "LuxCoreWheels - Module ${1} created in ${destdir} (editable)"
}


conan_source_recipe() {
  local destdir=~/.boost_conan/${1}


  # Install/source/build
  #
  # Keep install before source, otherwise settings.build_type won't be set
  # when running layout()
  #conan install "${destdir}" --build=editable -s build_type=Release
  conan source "${destdir}"
  #conan build "${destdir}" -s build_type=Release

  echo "LuxCoreWheels - Module ${1} sourced in ${destdir}"

}


set -eo pipefail

echo ""
echo "*******************************************"
echo "*          Boost lib dependencies         *"
echo "*******************************************"
echo ""

#conan install --requires fftw/3.3.10

# Put in editable mode (warning: conan not thread-safe, do not parallelize)
pids=()
for i in ${!deps[@]}; do
  dep=${deps[$i]}
  conan_create_recipe $dep &
  pids[${i}]=$!
done
#
# Wait for all treatments to finish
for pid in ${pids[*]}; do
    wait $pid
done

pids=()
for i in ${!deps[@]}; do
  dep=${deps[$i]}
  echo "LuxCoreWheels - Sourcing '${dep}'"
  #conan_build_recipe $dep &
  conan_source_recipe $dep &
  pids[${i}]=$!
done

# Wait for all treatments to finish
for pid in ${pids[*]}; do
    wait $pid
done

echo "LuxCoreWheels - BUILDING BOOST"

conan install ~/.boost_conan/boost --build=editable -s build_type=Release
conan build ~/.boost_conan/boost -s build_type=Release


echo "     Boost lib dependencies: done"
echo "*******************************************"
echo "*******************************************"
