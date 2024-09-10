#!/bin/bash
rm ~/.conan2/editable_packages.json
rm -rf ~/.boost_conan
source boost-create-base-deps.sh
source boost-create-lib-deps.sh
