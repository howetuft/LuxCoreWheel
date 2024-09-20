# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

import traceback
import os
import re

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import *

from boost_data import DEPENDENCIES, LIBRARIES

BOOST_VERSION = "1.78.0"


def source(self):
    print(f"BoostMeta -- Source {self.module}")
    get(
        self,
        f"https://github.com/boostorg/{self.module}/archive/refs/tags/boost-{self.version}.zip",
        strip_root=True,
    )
    if self.boost_post_source:
        self.boost_post_source()


def _math_post_source(self):
    print(f"BoostMeta -- Post source {self.module}")
    # Remove test build
    cmakelists_file = os.path.join(self.source_folder, "CMakeLists.txt")
    with open(cmakelists_file, encoding="utf-8") as f:
        read_data = f.read()

    write_data = re.sub(r"(add_subdirectory\(test\))", "", read_data)
    write_data = re.sub(r"(include\(CTest\))", "", write_data)

    with open(cmakelists_file, "w", encoding="utf-8") as f:
        f.write(write_data)


def _property_tree_post_source(self):
    print(f"BoostMeta -- Post source {self.module}")
    # Remove test build
    cmakelists_file = os.path.join(self.source_folder, "CMakeLists.txt")
    with open(cmakelists_file, encoding="utf-8") as f:
        read_data = f.read()

    with open(cmakelists_file, "w", encoding="utf-8") as f:
        f.write(f'set(BOOST_SUPERPROJECT_VERSION "{self.version}")\n')
        f.write(read_data)


def requirements(self):
    self.requires("zlib/[>=1.2.11 <2]")
    boost_deps = DEPENDENCIES.get(self.module, [])
    boost_deps += self._boost_deps
    for dep in boost_deps:
        self.requires(
            f"boost-{dep}/{self.version}@luxcorewheels/luxcorewheels",
            transitive_headers=True,
        )

def config_options(self):
    if self.settings.os == "Windows":
        self.options.rm_safe("fPIC")



def configure(self):
    if self.options.shared:
        self.options.rm_safe("fPIC")


def layout(self):
    build_type = self.settings.get_safe("build_type", default="Release")
    cmake_layout(self)
    if self.libs:
        print(f"BoostMeta -- {self.module}: libs = {self.libs}")

    # Set folders
    self.folders.source = "."
    self.folders.build = os.path.join("build", build_type)
    self.folders.generators = os.path.join(self.folders.build, "generators")

    # Describe package
    libs = self.libs + LIBRARIES.get(self.module, [])
    self.cpp.package.libs = libs
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
    deps.generate()

    boost_deps = self.boost_deps + DEPENDENCIES.get(self.module, [])

    # Generate also luxcore.cmake
    tc = CMakeToolchain(self)
    luxcore = ['message(STATUS "BoostMeta -- find packages")\n']
    luxcore.append("cmake_policy(SET CMP0167 NEW)\n")  # Remove cmake FindBoost
    luxcore.append("enable_language(CXX)\n")
    luxcore += [
        f"find_package(Boost_{dep} REQUIRED)\ninclude_directories(${{Boost_{dep}_INCLUDE_DIRS}})\n"
        for dep in boost_deps
        if dep != "boost"
    ]
    # luxcore.append("find_package(Boost)\n")  # TODO
    luxcore.append("find_package(ZLIB)\n")
    luxcore.append("unset(ZLIB_FIND_QUIETLY)\n")
    luxcore.append("include_directories(${ZLIB_INCLUDE_DIRS})\n")
    luxcore.append('message(STATUS "Zlib include: ${ZLIB_INCLUDE_DIRS}")\n')
    filepath = os.path.join(self.source_folder, "luxcore.cmake")
    with open(filepath, "w+") as f:
        f.writelines(luxcore)
    tc.cache_variables["CMAKE_PROJECT_INCLUDE"] = filepath
    tc.extra_sharedlinkflags=["/VERBOSE"]
    tc.cache_variables["CMAKE_VERBOSE_MAKEFILE"] = "TRUE"
    tc.preprocessor_definitions["BOOST_ALL_NO_LIB"] = None  # No automagic linking

    tc.generate()


def build(self):
    _cli_args = ["--trace-expand"] if self.module in [] else None
    cmake = CMake(self)
    cmake.configure(cli_args=_cli_args)
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
    self.cpp_info.bindirs = []
    self.cpp_info.libdirs = []
    # self.cpp_info.libs = [f"boost_{self.module}"]
    self.cpp_info.set_property("cmake_file_name", f"Boost_{self.module}")
    self.cpp_info.set_property("cmake_target_name", f"Boost::{self.module}")
    self.cpp_info.set_property("cmake_target_aliases", [f"boost::{self.module}"])
    # self.cpp_info.set_property("cmake_target_aliases", [f"Boost::{self.module}"])
    self.cpp_info.set_property("cmake_find_mode", "both")
    self.cpp_info.libs = self.libs + LIBRARIES.get(self.module, [])

    self.conf_info.define("boost:magic_autolink", False)


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
        if module == "math":
            boost_post_source = _math_post_source
        elif module == "property_tree":
            boost_post_source = _property_tree_post_source
        else:
            boost_post_source = None

        # requires = [f"boost/{boost_version}"]

        if module in LIBRARIES:
            package_type = "static-library"
        else:
            package_type = "header-library"

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
            user="luxcorewheels",
            channel="luxcorewheels",
            revision_mode="scm_folder",
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
