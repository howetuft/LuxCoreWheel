echo "CIBW_BEFORE_BUILD: pip"
pip install conan
pip install delvewheel

echo "CIBW_BEFORE_BUILD: Boost Python"
boost_python=$GITHUB_WORKSPACE/externals/windows/boost-python
conan editable add ${boost_python}
conan source ${boost_python}
#source $GITHUB_WORKSPACE/externals/windows/boost-create-base-deps.sh

# https://github.com/conan-io/conan/issues/13400
echo "CIBW_BEFORE_BUILD: OIIO"
oiio=$GITHUB_WORKSPACE/externals/windows/openimageio
conan editable add ${oiio}
conan source ${oiio}

echo "CIBW_BEFORE_BUILD: OIDN"
oidn=$GITHUB_WORKSPACE/externals/windows/oidn
conan editable add ${oidn}
conan source ${oidn}

echo "CIBW_BEFORE_BUILD: LuxCore"
conan editable add $GITHUB_WORKSPACE --name=LuxCoreWheels --version=2.6.0 --user=LuxCoreWheels --channel=LuxCoreWheels
conan install \
  --requires=LuxCoreWheels/2.6.0@LuxCoreWheels/LuxCoreWheels \
  --profile=conan_profile \
  --build=editable \
  --deployer=runtime_deploy \
  --deployer-folder=$GITHUB_WORKSPACE/libs \
  -s build_type=Release
