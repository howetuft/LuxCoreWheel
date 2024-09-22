echo "CIBW_BEFORE_BUILD: Boost"
source $GITHUB_WORKSPACE/externals/windows/boost-create-base-deps.sh

echo "CIBW_BEFORE_BUILD: OIIO"
oiio=$GITHUB_WORKSPACE/externals/windows/openimageio
conan editable add ${oiio} --output-folder=build
conan source ${oiio}
conan install ${oiio} --profile=conan_profile -s build_type=Release
conan build ${oiio} --build=editable -s build_type=Release

echo "CIBW_BEFORE_BUILD: OIDN"
oidn=$GITHUB_WORKSPACE/externals/windows/oidn
conan source ${oidn}
conan editable add ${oidn}
conan install ${oidn} -s build_type=Release
conan build ${oidn} --build=editable -s build_type=Release

#echo "CIBW_BEFORE_BUILD: LuxCore"
#conan editable add $GITHUB_WORKSPACE --name=LuxCoreWheels --version=2.6.0
#conan install $GITHUB_WORKSPACE --profile=conan_profile -s build_type=Release
#conan source $GITHUB_WORKSPACE
#conan build $GITHUB_WORKSPACE --build=editable -s build_type=Release
