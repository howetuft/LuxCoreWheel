# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

set -o pipefail

echo "CIBW_BEFORE_BUILD: pip"
pip install conan
pip install ninja
pip install "numpy" &

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


if [[ $RUNNER_OS == "macOS" && $RUNNER_ARCH == "ARM64" ]]; then
    echo "CIBW_BEFORE_BUILD: EMBREE3"
    embree3=$conan_path/embree3
    conan editable add ${embree3}
    conan source ${embree3} &
fi

if [[ $RUNNER_OS == "macOS" ]]; then
  echo "CIBW_BEFORE_BUILD: OCIO"
  OCIO_VERSION=2.3.1
  conan download opencolorio/${OCIO_VERSION} -r conancenter -m "*"
  folder=$(conan cache path opencolorio/${OCIO_VERSION})
  cp -rv $folder/../es/patches/ $folder/
  conan editable add $folder \
    --name=opencolorio \
    --version=${OCIO_VERSION}
  conan source $folder
fi

if [[ $RUNNER_OS == "macOS" ]]; then
  echo "CIBW_BEFORE_BUILD: MINIZIP-NG"
  conan download minizip-ng/4.0.3 --r conancenter
  conan editable add $(conan cache path minizip-ng/4.0.3) \
    --name=minizip-ng \
    --version=4.0.3
fi

# TODO
#if [[ $RUNNER_OS == "macOS" ]]; then
  #echo "CIBW_BEFORE_BUILD: OCIO"
  #ocio=$conan_path/opencolorio
  #conan editable add ${ocio}
  #conan source ${ocio} &
#fi

wait

echo "CIBW_BEFORE_BUILD: LuxCore"
conan editable add $WORKSPACE --name=LuxCoreWheels --version=2.6.0 --user=LuxCoreWheels --channel=LuxCoreWheels

conan install \
  --requires=LuxCoreWheels/2.6.0@LuxCoreWheels/LuxCoreWheels \
  --profile:all=$WORKSPACE/conan_profiles/conan_profile_${RUNNER_OS}_${RUNNER_ARCH} \
  --build=editable \
  --deployer=runtime_deploy \
  --deployer-folder=$WORKSPACE/libs \
  -s build_type=Release

oidn_version=2.1.0
if [[ $RUNNER_OS == "Linux" ]]; then
    cp -rv $oidn/oidn-${oidn_version}.x86_64.linux/bin/. $WORKSPACE/libs/
    cp -rv $oidn/oidn-${oidn_version}.x86_64.linux/lib/. $WORKSPACE/libs/
    ln -s $WORKSPACE/libs/libtbbmalloc.so $WORKSPACE/libs/libtbbmalloc.so.2
    ln -s $WORKSPACE/libs/libtbbmalloc_proxy.so $WORKSPACE/libs/libtbbmalloc_proxy.so.2
elif [[ $RUNNER_OS == "Windows" ]]; then
    cp -rv $oidn/oidn-${oidn_version}.x64.windows/bin/. $WORKSPACE/libs/
elif [[ $RUNNER_OS == "macOS" && $RUNNER_ARCH == "X64" ]]; then
    cp -rv $oidn/oidn-${oidn_version}.x86_64.macos/bin/. $WORKSPACE/libs/
    cp -rv $oidn/oidn-${oidn_version}.x86_64.macos/lib/. $WORKSPACE/libs/
elif [[ $RUNNER_OS == "macOS" && $RUNNER_ARCH == "ARM64" ]]; then
     cp -rv $oidn/oidn-${oidn_version}.arm64.macos/bin/. $WORKSPACE/libs/
     cp -rv $oidn/oidn-${oidn_version}.arm64.macos/lib/. $WORKSPACE/libs/
else
     echo "ERROR: unhandled runner os/arch '${RUNNER_OS}/${RUNNER_ARCH}'"
     exit 64
fi

echo "::group::Deployed"
find $WORKSPACE/libs
echo "::endgroup::"
