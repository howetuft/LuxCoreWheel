# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

set -o pipefail

echo "CIBW_BEFORE_BUILD: pip"
pip install conan
pip install ninja
pip install "numpy < 2.0" &

conan_path=$WORKSPACE/deps/conan

echo "CIBW_BEFORE_BUILD: Boost Python"
boost_python=$conan_path/boost-python
conan editable add ${boost_python}
conan source ${boost_python} &

echo "CIBW_BEFORE_BUILD: OIIO"
unset CI  # Otherwise OIIO passes -Werror to compiler (MacOS)!
oiio=$conan_path/openimageio
conan editable add ${oiio}
conan source ${oiio} &

echo "CIBW_BEFORE_BUILD: OIDN"
oidn=$conan_path/oidn_${RUNNER_OS}_${RUNNER_ARCH}
conan editable add ${oidn}
conan source ${oidn} &

wait

echo "CIBW_BEFORE_BUILD: LuxCore"
conan editable add $WORKSPACE --name=LuxCoreWheels --version=2.6.0 --user=LuxCoreWheels --channel=LuxCoreWheels
conan install \
  --requires=LuxCoreWheels/2.6.0@LuxCoreWheels/LuxCoreWheels \
  --profile:all=$WORKSPACE/conan_profiles/conan_profile_${RUNNER_OS}_${RUNNER_ARCH} \
  --build=editable \
  --build=missing \
  --deployer=runtime_deploy \
  --deployer-folder=$WORKSPACE/libs \
  -s build_type=Release

if [[ $RUNNER_OS == "Linux" ]]; then
    oidn_version=1.2.4
    cp -rv $oidn/oidn-${oidn_version}.x86_64.linux/bin/. $WORKSPACE/libs/
    cp -rv $oidn/oidn-${oidn_version}.x86_64.linux/lib/. $WORKSPACE/libs/
elif [[ $RUNNER_OS == "Windows" ]]; then
    oidn_version=2.3.0
    cp -rv $oidn/oidn-${oidn_version}.x64.windows/bin/. $WORKSPACE/libs/
elif [[ $RUNNER_OS == "macOS" && $RUNNER_ARCH == "X64" ]]; then
    oidn_version=2.3.0
    cp -rv $oidn/oidn-${oidn_version}.x86_64.macos/bin/. $WORKSPACE/libs/
    cp -rv $oidn/oidn-${oidn_version}.x86_64.macos/lib/. $WORKSPACE/libs/
elif [[ $RUNNER_OS == "macOS" && $RUNNER_ARCH == "ARM64" ]]; then
      oidn_version=2.3.0
      cp -rv $oidn/oidn-${oidn_version}.arm64.macos/bin/. $WORKSPACE/libs/
      cp -rv $oidn/oidn-${oidn_version}.arm64.macos/lib/. $WORKSPACE/libs/
 else
      echo "ERROR: unhandled runner os/arch '${RUNNER_OS}/${RUNNER_ARCH}'"
      exit 64
 fi

