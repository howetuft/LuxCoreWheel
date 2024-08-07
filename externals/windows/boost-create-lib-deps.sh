# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

#!/bin/bash

# For local debug, run this before:
# rm ~/.conan2/editable_packages.json
# rm -rf ~/.boost_conan


deps=(
)

conan_create_recipe() {
  local destdir=~/.boost_conan/${1}
  cp -R boost-${1} ${destdir}
  conan source "${destdir}"
  echo "LuxCoreWheels - Module ${1} created in ${destdir} (editable)"
}

set -eo pipefail

echo ""
echo "*******************************************"
echo "*          Boost lib dependencies         *"
echo "*******************************************"
echo ""

# Create
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

# Put in editable mode
for dep in ${deps[@]}; do
  destdir=~/.boost_conan/${dep}
  conan editable add "${destdir}"
  conan install "${destdir}" -s build_type=Release
done

echo "LuxCoreWheels - BUILDING BOOST"

conan_create_recipe "boost"
conan editable add ~/.boost_conan/boost
conan install ~/.boost_conan/boost --build=editable -s build_type=Release
conan build ~/.boost_conan/boost -s build_type=Release


echo "*******************************************"
echo "     Boost lib dependencies: done"
echo "*******************************************"
