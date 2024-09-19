cd $GITHUB_WORKSPACE

echo "CIBW_BEFORE_BUILD: Boost"
source externals/windows/boost-create-base-deps.sh

echo "CIBW_BEFORE_BUILD: OIIO"
oiio=./externals/windows/openimageio
conan editable add ${oiio}
conan install ${oiio} -s build_type=Release
conan source ${oiio}

echo "CIBW_BEFORE_BUILD: OIDN"
oidn=./externals/windows/oidn
conan editable add ${oidn}
conan install ${oidn} -s build_type=Release
conan source ${oidn}

echo "CIBW_BEFORE_BUILD: LuxCore"
conan install . -s build_type=Release --build=missing