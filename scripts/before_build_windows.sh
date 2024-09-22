echo "CIBW_BEFORE_BUILD: Boost"
source $GITHUB_WORKSPACE/externals/windows/boost-create-base-deps.sh

echo "CIBW_BEFORE_BUILD: OIIO"
oiio=$GITHUB_WORKSPACE/externals/windows/openimageio
conan install ${oiio} --build=editable -s build_type=Release openimageio/2.2.13.1@LuxCoreWheels/LuxCoreWheels
conan source ${oiio}
conan build ${oiio}
conan editable add ${oiio} openimageio/2.2.13.1@LuxCoreWheels/LuxCoreWheels

#conan install ${oiio} --profile=conan_profile -s build_type=Release
#conan build ${oiio} --build=editable -s build_type=Release

echo "CIBW_BEFORE_BUILD: OIDN"
oidn=$GITHUB_WORKSPACE/externals/windows/oidn
conan editable add ${oidn}
conan source ${oidn}
#conan install ${oidn} -s build_type=Release
#conan build ${oidn} --build=editable -s build_type=Release

echo "CIBW_BEFORE_BUILD: LuxCore"
conan editable add $GITHUB_WORKSPACE --name=LuxCoreWheels --version=2.6.0 --user=LuxCoreWheels --channel=LuxCoreWheels
conan install --requires=LuxCoreWheels/2.6.0@LuxCoreWheels/LuxCoreWheels --profile=conan_profile --build=editable -s build_type=Release
#conan install $GITHUB_WORKSPACE --profile=conan_profile -s build_type=Release
#conan source $GITHUB_WORKSPACE
#conan build $GITHUB_WORKSPACE --build=editable -s build_type=Release
