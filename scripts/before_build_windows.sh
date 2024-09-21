echo "CIBW_BEFORE_BUILD: Boost"
source $GITHUB_WORKSPACE/externals/windows/boost-create-base-deps.sh

echo "CIBW_BEFORE_BUILD: OIIO"
oiio=$GITHUB_WORKSPACE/externals/windows/openimageio
conan editable add ${oiio}
conan install ${oiio} -s build_type=Release
conan source ${oiio}
conan build ${oiio} --build=editable -s build_type=Release

echo "CIBW_BEFORE_BUILD: OIDN"
oidn=$GITHUB_WORKSPACE/externals/windows/oidn
conan editable add ${oidn}
conan install ${oidn} -s build_type=Release
conan source ${oidn}
conan build ${oidn} --build=editable -s build_type=Release

echo "CIBW_BEFORE_BUILD: LuxCore"
conan editable add $GITHUB_WORKSPACE --name=LuxCoreWheels --version=2.6.0
conan install $GITHUB_WORKSPACE -s build_type=Release --build=missing --build=editable
