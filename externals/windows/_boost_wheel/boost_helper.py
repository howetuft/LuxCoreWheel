# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

import traceback
import os

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import *

BOOST_VERSION = "1.78.0"

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
    for dep in self._boost_deps:
        self.requires(
            f"boost-{dep}/{self.version}@luxcorewheels/luxcorewheels",
            transitive_headers=True
        )
    for dep in self._other_deps:
        self.requires(dep)


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

    # Generate also luxcore.cmake
    tc = CMakeToolchain(self)
    finds = ['message(STATUS "BoostMeta -- find packages")\n']
    finds.append("enable_language(CXX)\n")
    finds += [
        f"find_package(Boost_{dep})\ninclude_directories(${{Boost_{dep}_INCLUDE_DIRS}})\n"
        for dep in self.boost_deps if dep != "boost"
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
