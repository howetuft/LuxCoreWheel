# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

import traceback
import os

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import *

BOOST_VERSION = "1.78.0"

DEPENDENCIES = {
    "algorithm": ["array", "assert", "bind", "concept_check", "config", "core", "exception", "function", "iterator", "mpl", "range", "regex", "static_assert", "throw_exception", "tuple", "type_traits", "unordered"],
    "align": ["assert", "config", "core", "static_assert"],
    "any": ["config", "throw_exception", "type_index"],
    "array": ["assert", "config", "core", "static_assert", "throw_exception"],
    "assert": ["config"],
    "bimap": ["concept_check", "config", "container_hash", "core", "iterator", "lambda", "mpl", "multi_index", "preprocessor", "static_assert", "throw_exception", "type_traits", "utility"],
    "bind": ["config", "core"],
    "concept_check": ["config", "preprocessor", "static_assert", "type_traits"],
    "config": [],
    "container_hash": ["config", "describe", "mp11"],
    "conversion": ["assert", "config","smart_ptr"],
    "core": ["assert", "config", "static_assert", "throw_exception"],
    "describe": ["mp11"],
    "detail": ["config", "core", "preprocessor", "static_assert", "type_traits"],
    "dynamic_bitset": ["assert", "config", "container_hash", "core", "integer", "move", "static_assert", "throw_exception"],
    "foreach": ["config", "core", "iterator", "mpl", "range", "type_traits"],
    "format": ["assert", "config", "core", "optional", "smart_ptr", "throw_exception", "utility"],
    "function": ["assert", "bind", "config", "core", "throw_exception"],
    "function_types": ["config", "core", "detail", "mpl", "preprocessor", "type_traits"],
    "fusion": ["config", "container_hash", "core", "function_types", "mpl", "preprocessor", "static_assert", "tuple", "type_traits", "typeof", "utility"],
    "integer": ["assert", "config", "core", "static_assert", "throw_exception", "type_traits"],
    "intrusive": ["assert", "config", "move"],
    "io": ["config"],
    "iterator": ["assert", "concept_check", "config", "core", "detail", "function_types", "fusion", "mpl", "optional", "smart_ptr", "static_assert", "type_traits", "utility"],
    "lambda": ["bind", "config", "core", "detail", "iterator", "mpl", "preprocessor", "tuple", "type_traits", "utility"],
    "lexical_cast": ["config", "container", "core", "throw_exception", "type_traits"],
    "move": ["config"],
    "mpl": ["config", "core", "predef", "preprocessor", "static_assert", "type_traits", "utility"],
    "mp11": [],
    "multi_index": ["assert", "bind", "config", "container_hash", "core", "integer", "iterator", "move", "mpl", "preprocessor", "smart_ptr", "static_assert", "throw_exception", "tuple", "type_traits", "utility"],
    "numeric_conversion": ["config", "conversion", "core", "mpl", "preprocessor", "throw_exception", "type_traits"],
    "optional": ["assert", "config", "core", "move", "static_assert", "throw_exception", "type_traits"],
    "parameter": ["config", "core", "function", "fusion", "mp11", "mpl", "optional", "preprocessor", "type_traits", "utility"],
    # HERE
    "stacktrace": ["array", "config", "container_hash", "core", "predef", "static_assert", "type_traits", "winapi"],
    "static_assert": ["config"],
    "throw_exception": ["assert", "config"],
}

def source(self):
    print(f"BoostMeta -- Source {self.module}")
    get(
        self,
        f"https://github.com/boostorg/{self.module}/archive/refs/tags/boost-{self.version}.zip",
        strip_root=True
    )
    if self.boost_post_source:
        self.boost_post_source()

def requirements(self):
    self.requires("zlib/[>=1.2.11 <2]")
    boost_deps = DEPENDENCIES.get(self.module, [])
    boost_deps += self._boost_deps
    print(self.module, boost_deps)
    for dep in boost_deps:
        self.requires(
            f"boost-{dep}/{self.version}@luxcorewheels/luxcorewheels",
            transitive_headers=True
        )


def config_options(self):
    if self.settings.os == "Windows":
        self.options.rm_safe("fPIC")

def configure(self):
    if self.options.shared:
        self.options.rm_safe("fPIC")

def layout(self):
    cmake_layout(self)
    if self.libs:
        print(f"BoostMeta -- {self.module}: libs = {self.libs}")

    # Set folders
    self.folders.source = "."
    self.folders.build = os.path.join("build", str(self.settings.build_type))
    self.folders.generators = os.path.join(self.folders.build, "generators")

    # Describe package
    self.cpp.package.libs = self.libs
    self.cpp.package.includedirs = ["include"]
    self.cpp.package.libdirs += [
        self.folders.build,
        os.path.join(self.folders.build, "lib")
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
    deps.generate()

    boost_deps = self.boost_deps + DEPENDENCIES.get(self.module, [])

    # Generate also luxcore.cmake
    tc = CMakeToolchain(self)
    finds = ['message(STATUS "BoostMeta -- find packages")\n']
    finds.append("enable_language(CXX)\n")
    finds += [
        f"find_package(Boost_{dep})\ninclude_directories(${{Boost_{dep}_INCLUDE_DIRS}})\n"
        for dep in boost_deps if dep != "boost"
    ]
    finds.append("cmake_policy(SET CMP0167 OLD)\n")
    finds.append("cmake_policy(SET CMP0169 OLD)\n")
    # finds.append("find_package(Boost)\n")  # TODO
    finds.append("find_package(ZLIB)\n")
    finds.append("unset(ZLIB_FIND_QUIETLY)\n")
    finds.append("include_directories(${ZLIB_INCLUDE_DIRS})\n")
    finds.append('message(STATUS "Zlib include: ${ZLIB_INCLUDE_DIRS}")\n')
    filepath = os.path.join(self.source_folder, "luxcore.cmake")
    with open(filepath, "w+") as f:
        f.writelines(finds)
    tc.cache_variables["CMAKE_PROJECT_INCLUDE"] = filepath

    tc.generate()

def build(self):
    cmake = CMake(self)
    cmake.configure()
    cmake.build()

def package(self):
    cmake = CMake(self)
    cmake.install()
    copy(self, "*.h", src=self.source_folder,
         dst=os.path.join(self.package_folder, "include"))
    copy(self, "*.hpp", src=self.source_folder,
         dst=os.path.join(self.package_folder, "include"))
    copy(self, "*.lib", src=self.build_folder,
         dst=os.path.join(self.package_folder, "lib"), keep_path=False)
    copy(self, "*.a", src=self.build_folder,
         dst=os.path.join(self.package_folder, "lib"), keep_path=False)
    copy(self, "*.cmake", src=self.build_folder,
         dst=os.path.join(self.package_folder, "lib", "cmake"), keep_path=False)

def package_info(self):
    self.cpp_info.bindirs = []
    self.cpp_info.libdirs = []
    #self.cpp_info.libs = [f"boost_{self.module}"]
    self.cpp_info.set_property("cmake_file_name", f"Boost_{self.module}")
    self.cpp_info.set_property("cmake_target_name", f"Boost::{self.module}")
    # self.cpp_info.set_property("cmake_target_aliases", [f"Boost::{self.module}"])
    self.cpp_info.set_property("cmake_find_mode", "both")
    self.cpp_info.libs = self.libs


def package_id(self):
    # We clear everything in order to have a constant package_id and use the cache
    self.info.clear()


class BoostMeta(type):
    """Metaclass to create the ConanFile class."""
    # Sources are located in the same place as this recipe, copy them to the recipe

    data_cache = dict()

    def __new__(cls, name, bases, attrs, **kwargs):
        # We cache kwargs as conan sometimes erases attributes...
        if name in BoostMeta.data_cache and kwargs:
            print(f"BoostMeta -- Warning: '{name}' already in cache")
        if name in BoostMeta.data_cache:
            # Retrieve kwargs
            kwargs = BoostMeta.data_cache[name]
        else:
            BoostMeta.data_cache[name] = kwargs
        # print(f"'{name}' creation requested")
        # traceback.print_stack()

        # Attributes
        module = str(kwargs["module"])
        boost_version = BOOST_VERSION
        boost_deps = list(kwargs.get("boost_deps", []))
        other_deps = list(kwargs.get("other_deps", []))
        boost_post_source = kwargs.get("boost_post_source", None)
        # requires = [f"boost/{boost_version}"]

        package_type = kwargs.get("package_type", "library")
        libs = kwargs.get("libs", [])

        new_attrs = dict(
            package_type=package_type,
            settings=("os", "compiler", "build_type", "arch"),
            options={"shared": [True, False], "fPIC": [True, False]},
            default_options={"shared": False, "fPIC": True},
            exports_sources=("CMakeLists.txt", "src/*", "include/*"),
            module=module,
            name=f"boost-{module}",
            version=boost_version,
            boost_deps=boost_deps,
            source=source,
            boost_post_source=boost_post_source,
            config_options=config_options,
            configure=configure,
            layout=layout,
            generate=generate,
            build=build,
            package=package,
            package_info=package_info,
            package_id=package_id,
            user = "luxcorewheels",
            channel = "luxcorewheels",
            revision_mode = "scm_folder",
            libs=libs,
            _boost_deps=boost_deps,
            _other_deps=other_deps,
            requirements=requirements,
        )
        attrs.update(new_attrs)

        # Instantiate
        # print(f"Boost - Generating recipe {name} for ('{module}', '{boost_version}')")
        new_class = super().__new__(cls, name, bases, attrs)
        return new_class
