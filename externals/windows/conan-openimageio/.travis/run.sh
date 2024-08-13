#!/bin/bash

set -e
set -x

export CONAN_UPLOAD="https://api.bintray.com/conan/ppodsiadly/conan"
python3 build.py
