#!/bin/bash
rm ~/.conan2/editable_packages.json
rm -rf ~/.boost_conan
source boost-create-base-deps.sh
source boost-create-lib-deps.sh
rm conanbuildenv-release-x86_64.sh  conanbuild.sh  conanrunenv-release-x86_64.sh  conanrun.sh deactivate_conanbuild.sh  deactivate_conanrun.sh
