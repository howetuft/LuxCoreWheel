# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

#!/bin/bash

# For local debug, run this before:
# rm ~/.conan2/editable_packages.json

deps=(
  python
  atomic
  chrono
  container
  filesystem
  container
  date_time
  iostreams
  program_options
  random
  serialization
  thread
)


pids=()
for i in ${!deps[@]}; do
  dep=${deps[$i]}
  echo "Building '${dep}'"
  destdir=~/.boost_conan/${dep}
  cp -R boost-${dep} ${destdir}
  conan install "${destdir}" -s build_type=Release
  conan source "${destdir}"
  conan build "${destdir}"
  pids[${i}]=$!
done

# Wait for all treatments to finish
for pid in ${pids[*]}; do
    wait $pid
done

# Put in editable mode (warning: conan not thread-safe, do not parallelize)
cd ~/.boost_conan
for dep in ${deps[@]}; do
  destdir=~/.boost_conan/${dep}
  conan editable add "${destdir}"
done

echo "Boost lib dependencies: done"
