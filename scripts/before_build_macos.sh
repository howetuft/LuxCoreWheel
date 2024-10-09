# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

set -o pipefail

echo "CIBW_BEFORE_BUILD: pip"
pip install conan
pip install "numpy < 2.0"
conan profile detect --force  # TODO

echo "CIBW_BEFORE_BUILD: Boost Python"
boost_python=$GITHUB_WORKSPACE/externals/windows/boost-python
conan editable add ${boost_python}
conan source ${boost_python} &

echo "CIBW_BEFORE_BUILD: OIIO"
oiio=$GITHUB_WORKSPACE/externals/windows/openimageio
conan editable add ${oiio}
conan source ${oiio} &

echo "CIBW_BEFORE_BUILD: OIDN"
oidn=$GITHUB_WORKSPACE/externals/windows/oidn
conan editable add ${oidn}
conan install ${oidn} --profile=conan_profile_macos -s build_type=Release # For self.settings to be set
conan source ${oidn} &

wait

# TODO In oidn conanfile?
mkdir $GITHUB_WORKSPACE/libs
cp -rv $GITHUB_WORKSPACE/externals/windows/oidn/oidn-2.3.0.x64.windows/bin/. $GITHUB_WORKSPACE/libs/

echo "CIBW_BEFORE_BUILD: LuxCore"
conan editable add $GITHUB_WORKSPACE --name=LuxCoreWheels --version=2.6.0 --user=LuxCoreWheels --channel=LuxCoreWheels
unset CI  # Otherwise OIIO passes -Werror to compiler!
conan install \
  --requires=LuxCoreWheels/2.6.0@LuxCoreWheels/LuxCoreWheels \
  --profile=conan_profile_macos \
  --build=editable \
  --build=missing \
  --deployer=runtime_deploy \
  --deployer-folder=$GITHUB_WORKSPACE/libs \
  -s build_type=Release
