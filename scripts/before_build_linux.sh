# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

set -o pipefail

GITHUB_WORKSPACE="/project"

echo "CIBW_BEFORE_BUILD: pip"
pip install conan
pip install ninja
pip install "numpy < 2.0" &

echo "CIBW_BEFORE_BUILD: Boost Python"
boost_python=$GITHUB_WORKSPACE/externals/windows/boost-python
conan editable add ${boost_python}
conan source ${boost_python} &

echo "CIBW_BEFORE_BUILD: OIIO"
oiio=$GITHUB_WORKSPACE/externals/windows/openimageio
conan editable add ${oiio}
conan source ${oiio} &

echo "CIBW_BEFORE_BUILD: OIDN"
oidn=$GITHUB_WORKSPACE/externals/windows/oidn_linux
conan editable add ${oidn}
conan source ${oidn} &

wait

# TODO In oidn conanfile?
mkdir $GITHUB_WORKSPACE/libs
oidn_version=1.2.4
cp -rv $GITHUB_WORKSPACE/externals/windows/oidn_linux/oidn-${oidn_version}.x86_64.linux/bin/. $GITHUB_WORKSPACE/libs/
cp -rv $GITHUB_WORKSPACE/externals/windows/oidn_linux/oidn-${oidn_version}.x86_64.linux/lib/. $GITHUB_WORKSPACE/libs/

echo "CIBW_BEFORE_BUILD: LuxCore"
conan editable add $GITHUB_WORKSPACE --name=LuxCoreWheels --version=2.6.0 --user=LuxCoreWheels --channel=LuxCoreWheels
conan install \
  --requires=LuxCoreWheels/2.6.0@LuxCoreWheels/LuxCoreWheels \
  --profile:all=conan_profile_${RUNNER_OS}_${RUNNER_ARCH} \
  --build=editable \
  --deployer=runtime_deploy \
  --deployer-folder=$GITHUB_WORKSPACE/libs \
  -s build_type=Release
