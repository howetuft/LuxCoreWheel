# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

import os
from sys import version_info as vi

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import get, copy, replace_in_file

PYTHON_MINOR = os.environ["PYTHON_MINOR"]

BOOST_VERSION = os.environ["BOOST_VERSION"]

BOOST_PYTHON_DEPS = [
    "align",
    "bind",
    "config",
    "conversion",
    "core",
    "detail",
    "foreach",
    "function",
    "iterator",
    "lexical_cast",
    "mpl",
    "mp11",
    "numeric_conversion",
    "preprocessor",
    "smart_ptr",
    "static_assert",
    "tuple",
    "type_traits",
    "utility",
    # Private
    "graph",
    "integer",
    "property_map",
]

BOOST_LIBRARIES = {
    "atomic",
    "chrono",
    "container",
    "context",
    "coroutine",
    "date_time",
    "filesystem",
    "graph",
    "iostreams",
    "program_options",
    "python",
    "random",
    "serialization",
    "stacktrace",
    "thread",
}


class BoostPythonConan(ConanFile):
    name = "boost-python"
    version = BOOST_VERSION
    user = "luxcorewheels"
    channel = "luxcorewheels"

    settings = ("os", "compiler", "build_type", "arch")
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    exports_sources = ("CMakeLists.txt", "src/*", "include/*")
    _libs = [f"boost_python{vi.major}{vi.minor}", f"boost_numpy{vi.major}{vi.minor}"]

    def source(self):
        get(
            self,
            f"https://github.com/boostorg/python/archive/refs/tags/boost-{self.version}.zip",
            strip_root=True,
        )
        replace_in_file(
            self,
            os.path.join(self.source_folder, "CMakeLists.txt"),
            "find_package(Python REQUIRED COMPONENTS Development OPTIONAL_COMPONENTS NumPy)",
            "find_package(Python REQUIRED COMPONENTS Development.Module OPTIONAL_COMPONENTS NumPy)",
        )

        # Numpy >= 2.0
        # https://github.com/boostorg/python/pull/432/commits/33ac06ca59a68266d3d26edf08205d31ddab4a6c
        numpy2_replacement = """\
int dtype::get_itemsize() const {
#if NPY_ABI_VERSION < 0x02000000
  return reinterpret_cast<PyArray_Descr*>(ptr())->elsize;
#else
  return PyDataType_ELSIZE(reinterpret_cast<PyArray_Descr*>(ptr()));
#endif
}
"""
        numpy2_replaced = """\
int dtype::get_itemsize() const { return reinterpret_cast<PyArray_Descr*>(ptr())->elsize;}"""
        replace_in_file(
            self,
            os.path.join(self.source_folder, "src", "numpy", "dtype.cpp"),
            numpy2_replaced,
            numpy2_replacement,
        )

        # Another replacement for numpy >= 2.0
        numpy2_replacement = """  return a == b;\n"""
        # Nota: DO NOT remove trailing space
        numpy2_replaced = """\
    // On Windows x64, the behaviour described on 
    // http://docs.scipy.org/doc/numpy/reference/c-api.array.html for
    // PyArray_EquivTypes unfortunately does not extend as expected:
    // "For example, on 32-bit platforms, NPY_LONG and NPY_INT are equivalent".
    // This should also hold for 64-bit platforms (and does on Linux), but not
    // on Windows. Implement an alternative:
#ifdef _MSC_VER
    if (sizeof(long) == sizeof(int) &&
        // Manually take care of the type equivalence.
        ((a == dtype::get_builtin<long>() || a == dtype::get_builtin<int>()) &&
         (b == dtype::get_builtin<long>() || b == dtype::get_builtin<int>()) ||
         (a == dtype::get_builtin<unsigned int>() || a == dtype::get_builtin<unsigned long>()) &&
         (b == dtype::get_builtin<unsigned int>() || b == dtype::get_builtin<unsigned long>()))) {
        return true;
    } else {
        return PyArray_EquivTypes(
            reinterpret_cast<PyArray_Descr*>(a.ptr()),
            reinterpret_cast<PyArray_Descr*>(b.ptr())
        );
    }
#else
    return PyArray_EquivTypes(
        reinterpret_cast<PyArray_Descr*>(a.ptr()),
        reinterpret_cast<PyArray_Descr*>(b.ptr())
    );
#endif
"""
        replace_in_file(
            self,
            os.path.join(self.source_folder, "src", "numpy", "dtype.cpp"),
            numpy2_replaced,
            numpy2_replacement,
        )


    def requirements(self):
        self.requires("zlib/[>=1.2.11 <2]")
        self.requires(f"boost/{self.version}")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        build_type = self.settings.get_safe("build_type", default="Release")
        cmake_layout(self)

        # Set folders
        self.folders.source = "."
        self.folders.build = os.path.join("build", build_type)
        self.folders.generators = os.path.join(self.folders.build, "generators")

        # Describe package
        self.cpp.package.libs = self._libs
        self.cpp.package.includedirs = ["include"]
        self.cpp.package.libdirs += [
            self.folders.build,
            os.path.join(self.folders.build, "lib"),
        ]

        # Describe what changes between package and editable
        #
        # cpp.source and cpp.build information is specifically designed for
        # editable packages:
        # this information is relative to the source folder that is '.'
        self.cpp.source.includedirs = ["include"]

        # this information is relative to the build folder that is
        # './build/<build_type>', so it will map to ./build/<build_type> for libdirs
        self.cpp.build.libdirs = ["."]

    def generate(self):
        deps = CMakeDeps(self)
        deps.set_property("python", "cmake_find_mode", "config")  # TODO
        deps.generate()

        # Generate also luxcore.cmake
        tc = CMakeToolchain(self)
        luxcore = ['message(STATUS "BoostMeta -- find packages")\n']
        luxcore.append("cmake_policy(SET CMP0167 NEW)\n")  # Remove cmake FindBoost
        luxcore.append("enable_language(CXX)\n")
        luxcore.append("find_package(Boost REQUIRED)\n")  # TODO
        luxcore += [
            f"find_package(Boost COMPONENTS {dep} REQUIRED)\n"
            for dep in BOOST_PYTHON_DEPS
        ]
        luxcore += [
            f"add_library(Boost::{dep} ALIAS boost::boost)\n"
            for dep in BOOST_PYTHON_DEPS
            if dep not in BOOST_LIBRARIES
        ]
        luxcore.append("include_directories(${Boost_INCLUDE_DIRS})\n")
        luxcore.append("find_package(ZLIB)\n")
        luxcore.append("unset(ZLIB_FIND_QUIETLY)\n")
        luxcore.append("include_directories(${ZLIB_INCLUDE_DIRS})\n")
        luxcore.append('message(STATUS "Zlib include: ${ZLIB_INCLUDE_DIRS}")\n')
        filepath = os.path.join(self.source_folder, "luxcore.cmake")
        with open(filepath, "w+", encoding="utf-8") as f:
            f.writelines(luxcore)
        tc.cache_variables["CMAKE_PROJECT_INCLUDE"] = filepath
        tc.extra_sharedlinkflags = ["/VERBOSE"]
        tc.cache_variables["CMAKE_VERBOSE_MAKEFILE"] = True
        # tc.cache_variables["CMAKE_FIND_DEBUG_MODE"] = True  # For debugging
        tc.preprocessor_definitions["BOOST_ALL_NO_LIB"] = None  # No automagic linking
        tc.preprocessor_definitions["BOOST_NO_CXX98_FUNCTION_BASE"] = None  # No deprecated functions (C++17)
        tc.preprocessor_definitions["BOOST_NO_AUTO_PTR"] = None  # No auto_ptr
        # if PYTHON_MINOR == "8":
            # tc.preprocessor_definitions["Py_LIMITED_API"] = True
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        copy(
            self,
            "*.h",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "include"),
        )
        copy(
            self,
            "*.hpp",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "include"),
        )
        copy(
            self,
            "*.lib",
            src=self.build_folder,
            dst=os.path.join(self.package_folder, "lib"),
            keep_path=False,
        )
        copy(
            self,
            "*.a",
            src=self.build_folder,
            dst=os.path.join(self.package_folder, "lib"),
            keep_path=False,
        )
        copy(
            self,
            "*.cmake",
            src=self.build_folder,
            dst=os.path.join(self.package_folder, "lib", "cmake"),
            keep_path=False,
        )

    def package_info(self):
        # self.cpp_info.libs = [f"boost_{self.module}"]
        self.cpp_info.set_property("cmake_file_name", "Boost_python")
        self.cpp_info.set_property("cmake_target_name", "Boost::python")
        self.cpp_info.set_property("cmake_target_aliases", ["boost::python"])
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.libs = self._libs

        self.conf_info.define("boost:magic_autolink", False)

    def package_id(self):
        # We clear everything in order to have a constant package_id and use the cache
        self.info.clear()
