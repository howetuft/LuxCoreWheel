function escape_sed() {
  # Escape '/' to make string usable in sed
  # Arg #1: string to escape
  local param="$1"
  echo ${param/\//\\/}
}


function replace_anywhere() {
  # Replace a string by another in all files of the tree
  # Arg #1: string to search
  # Arg #2: string to replace with
  local search=$(escape_sed "${1}")
  local replace=$(escape_sed "${2}")
  grep -rl "${1}" . --exclude-dir=.git | xargs $SED -i "s/${search}/${replace}/g"
}

function remove_containing_line() {
  # Remove all lines containing a string from a given file
  # Arg #1: string to search
  # Arg #2: file
  local content=$(escape_sed "$1")
  $SED -i "/${content}/d" "${2}"
}

# Script starts here


cd $GITHUB_WORKSPACE/LuxCore

echo "Find sed"
if [[ $RUNNER_OS == "macOS" ]]; then
  brew install gnu-sed
  echo "SED=gsed" >> $GITHUB_ENV
  SED=gsed
else
  echo "SED=sed" >> $GITHUB_ENV
  SED=sed
fi


echo "Bump version"
replace_anywhere "LUXCORE_VERSION_MINOR 6" "LUXCORE_VERSION_MINOR 9a1"
replace_anywhere "LUXRAYS_VERSION_MINOR 6" "LUXRAYS_VERSION_MINOR 9a1"


echo "Remove all local Find*.cmake"
rm -vf $GITHUB_WORKSPACE/LuxCore/cmake/Packages/Find*.cmake


echo "Remove Demos, Tests and Samples targets"
useless_targets=(
  luxcoredemo
  luxcorescenedemo
  luxcoreimplserializationdemo
  luxcoreconsole
  luxcoreui
  pyunittests
  samples
)
for target in "${useless_targets[@]}"
do
  echo "Removing ${target}"
  remove_containing_line "${target}" CMakeLists.txt
done


echo "Remove duplicate embedded libraries"
for lib in opencolorio yaml expat spdlog openvdb eigen
do
  echo "LuxCoreWheel - Removing '${lib}'"
  remove_containing_line "deps/${lib}" src/slg/CMakeLists.txt
  remove_containing_line "add_library(${lib}" src/slg/CMakeLists.txt
  remove_containing_line "target_compile_definitions(${lib}" src/slg/CMakeLists.txt
  remove_containing_line "deps/${lib}" CMakeLists.txt
  rm -rf deps/${lib}*
done


echo "OpenEXR 3.x (replace OpenEXR/half.h by Imath/half.h)"
replace_anywhere "<OpenEXR/half.h>" "<Imath/half.h>"


echo "Remove luxcore target_link_libraries"
remove_containing_line "target_link_libraries(luxcore" src/luxcore/CMakeLists.txt


echo "Remove pyluxcore target_link_libraries"
remove_containing_line "target_link_libraries(pyluxcore" src/luxcore/CMakeLists.txt


echo "Remove GTK3"
remove_containing_line "GTK3" cmake/Dependencies.cmake


echo "Switch CMAKE_SOURCE_DIR to PROJECT_SOURCE_DIR"
replace_anywhere "CMAKE_SOURCE_DIR" "PROJECT_SOURCE_DIR"


echo "Remove CMAKE_CXX_STANDARD from CMakeLists.txt"
remove_containing_line "CMAKE_CXX_STANDARD" CMakeLists.txt


echo "Add missing code for {fmt} Camera"
snippet='
template <>
struct fmt::formatter<luxcore::Camera::CameraType> {
    formatter() { std::cout << "formatter<luxcore::Camera::CameraType>()\n"; }

    constexpr auto parse(fmt::format_parse_context& ctx) {
        return ctx.begin();
    }

    auto format(const luxcore::Camera::CameraType& cam, fmt::format_context& ctx) const {
        return fmt::format_to(ctx.out(), "{}", int(cam));
    }
};'
echo "" >> src/luxcore/luxcoreimpl.cpp
echo $snippet >> src/luxcore/luxcoreimpl.cpp


echo "Adapt to Boost > 1.79"
$SED -i '1s/^/#include <boost\/filesystem\/fstream.hpp> /' src/luxrays/utils/cuda.cpp
$SED -i '1s/^/#include <boost\/filesystem\/fstream.hpp> /' src/luxrays/utils/ocl.cpp


echo "Macos - Remove Platform Specifics and Configuration"
if [[ $RUNNER_OS == "macOS" ]]; then
  remove_containing_line "INCLUDE(PlatformSpecific)" CMakeLists.txt
  remove_containing_line "INCLUDE(Configuration)" CMakeLists.txt
fi


echo "Windows - Remove /TP compiler flag"
if [[ $RUNNER_OS == "Windows" ]]; then
  $SED -i "s/\/TP//g" cmake/PlatformSpecific.cmake
fi