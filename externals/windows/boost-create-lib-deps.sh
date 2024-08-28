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


for dep in ${deps[@]}; do
  echo "Building '${dep}'"
  destdir=boost-${dep}
  conan editable add "${destdir}"
  conan install "${destdir}" -s build_type=Release
  conan source "${destdir}"
  conan build "${destdir}"
done

echo "Boost lib dependencies: done"
