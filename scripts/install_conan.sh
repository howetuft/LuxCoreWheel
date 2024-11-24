# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

function conan_create_install() {
  name=$(echo "$1" | tr '[:upper:]' '[:lower:]')  # Package name in lowercase
  version=$2

  conan create $WORKSPACE/deps/conan/$name \
    --profile:all=$WORKSPACE/conan_profiles/conan_profile_${RUNNER_OS}_${RUNNER_ARCH} \
    --build=missing \
    -s build_type=Release
  conan install --requires=$name/$version@luxcorewheels/luxcorewheels \
    --profile:all=$WORKSPACE/conan_profiles/conan_profile_${RUNNER_OS}_${RUNNER_ARCH} \
    --build=missing \
    -vverbose \
    -s build_type=Release
}


# Script starts here

set -o pipefail
if [[ $RUNNER_OS == "Linux" ]]; then
  cache_dir=/conan_cache
else
  cache_dir=$WORKSPACE/conan_cache
fi

echo "::group::CIBW_BEFORE_BUILD: pip"
pip install conan
pip install ninja
if [[ $PYTHON_MINOR == "8" ]]; then
  pip install "numpy < 2"
else
  pip install "numpy >= 2"
fi
echo "::endgroup::"

echo "::group::CIBW_BEFORE_BUILD: restore conan cache"
# Restore conan cache (add -vverbose to debug)
conan cache restore $cache_dir/conan_cache_save.tgz
echo "::endgroup::"

echo "::group::CIBW_BEFORE_BUILD: Boost Python"
# Private boost-python is patched to be compatible with numpy 2
conan_create_install boost-python $BOOST_VERSION
echo "::endgroup::"

echo "::group::CIBW_BEFORE_BUILD: OIIO"
# Private OIIO uses fmt as header-only
unset CI  # Otherwise OIIO passes -Werror to compiler (MacOS)!
conan_create_install openimageio $OIIO_VERSION
echo "::endgroup::"

echo "::group::CIBW_BEFORE_BUILD: OIDN"
conan remove -c "oidn_linux_x64/*"  # TODO
#conan_create_install oidn_${RUNNER_OS}_${RUNNER_ARCH} $OIDN_VERSION  # TODO
conan_create_install oidn $OIDN_VERSION
#oidn=$WORKSPACE/deps/conan/oidn_${RUNNER_OS}_${RUNNER_ARCH}
#conan editable add ${oidn}
#conan source ${oidn}
echo "::endgroup::"


# TODO
#if [[ $RUNNER_OS == "macOS" && $RUNNER_ARCH == "ARM64" ]]; then
    #echo "CIBW_BEFORE_BUILD: EMBREE3"
    #embree3=$conan_path/embree3
    #conan editable add ${embree3}
    #conan source ${embree3} &
#fi

if [[ $RUNNER_OS == "Windows" ]]; then
  DEPLOY_PATH=$(cygpath "C:\\Users\\runneradmin")
else
  DEPLOY_PATH=$WORKSPACE
fi

echo "::group::CIBW_BEFORE_BUILD: LuxCore"
conan remove -c "luxcorewheels/*"  # TODO
cd $WORKSPACE
conan create $WORKSPACE \
  --profile:all=$WORKSPACE/conan_profiles/conan_profile_${RUNNER_OS}_${RUNNER_ARCH} \
  --build=missing \
  -s build_type=Release

# We use full deployer to get rid of the "strange" paths that Conan uses in
# the cache. Caveat: order between runtime and full matters
conan install $WORKSPACE \
  --profile:all=$WORKSPACE/conan_profiles/conan_profile_${RUNNER_OS}_${RUNNER_ARCH} \
  --build=missing \
  --deployer=full_deploy \
  --deployer-folder=$DEPLOY_PATH \
  -vverbose \
  -s build_type=Release

# TODO
#conan install --requires=luxcorewheels/2.6.0@luxcorewheels/luxcorewheels \
  #--profile:all=$WORKSPACE/conan_profiles/conan_profile_${RUNNER_OS}_${RUNNER_ARCH} \
  #--build=missing \
  #--output-folder $WORKSPACE \
  #--deployer=full_deploy \
  #--deployer-folder=$WORKSPACE \
  #-vverbose \
  #-s build_type=Release
#conan editable add $WORKSPACE --name=LuxCoreWheels --version=2.6.0 --user=LuxCoreWheels --channel=LuxCoreWheels
#conan install \
  #--requires=LuxCoreWheels/2.6.0@LuxCoreWheels/LuxCoreWheels \
  #--profile:all=$WORKSPACE/conan_profiles/conan_profile_${RUNNER_OS}_${RUNNER_ARCH} \
  #--build=editable \
  #--build=missing \
  #--deployer=runtime_deploy \
  #--deployer-folder=$WORKSPACE/libs \
  #-s build_type=Release

echo "::endgroup::"

#echo "::group::Installing oidn"
#if [[ $RUNNER_OS == "Linux" ]]; then
    #oidn_version=2.3.0
    #cp -rv $oidn/oidn-${oidn_version}.x86_64.linux/bin/. $WORKSPACE/libs/
    #cp -rv $oidn/oidn-${oidn_version}.x86_64.linux/lib/. $WORKSPACE/libs/
    #cp -rv $oidn/oneapi-tbb-2021.12.0/lib/intel64/gcc4.8/. $WORKSPACE/libs/
#elif [[ $RUNNER_OS == "Windows" ]]; then
    #oidn_version=2.3.0
    #cp -rv $oidn/oidn-${oidn_version}.x64.windows/bin/. $WORKSPACE/libs/
#elif [[ $RUNNER_OS == "macOS" && $RUNNER_ARCH == "X64" ]]; then
    #oidn_version=2.3.0
    #cp -rv $oidn/oidn-${oidn_version}.x86_64.macos/bin/. $WORKSPACE/libs/
    #cp -rv $oidn/oidn-${oidn_version}.x86_64.macos/lib/. $WORKSPACE/libs/
#elif [[ $RUNNER_OS == "macOS" && $RUNNER_ARCH == "ARM64" ]]; then
      #oidn_version=2.3.0
      #cp -rv $oidn/oidn-${oidn_version}.arm64.macos/bin/. $WORKSPACE/libs/
      #cp -rv $oidn/oidn-${oidn_version}.arm64.macos/lib/. $WORKSPACE/libs/
#else
      #echo "ERROR: unhandled runner os/arch '${RUNNER_OS}/${RUNNER_ARCH}'"
      #exit 64
#fi
#echo "::endgroup::"

echo "::group::Saving dependencies in ${cache_dir}"
conan cache clean "*"  # Clean non essential files
conan cache save -vverbose --file $cache_dir/conan_cache_save.tgz "*/*:*"
echo "::endgroup::"
