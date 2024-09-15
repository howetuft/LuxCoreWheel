# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

"""Main boost file (bootstrap for others)"""
import os

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import *

from boost_helper import DEPENDENCIES

DEPS = DEPENDENCIES.keys()

class BoostBoost(ConanFile):
    name = "boost"
    version = "1.78.0"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    exports_sources = ("CMakeLists.txt", "src/*", "include/*")
    user = "luxcorewheels"
    channel = "luxcorewheels"
    revision_mode = "scm_folder"
    package_type = "header-library"

    def requirements(self):
        for dep in DEPS:
            self.requires(
                f"boost-{dep}/{self.version}@luxcorewheels/luxcorewheels",
                headers=True,
                libs=True,
            )
            print(f"Boost package: requires {dep}")


    def layout(self):
        cmake_layout(self)

        # Set folders
        self.folders.source = "."
        self.folders.build = os.path.join("build", str(self.settings.build_type))
        self.folders.generators = os.path.join(self.folders.build, "generators")

        # Describe package
        # self.cpp.package.libs = self.libs
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

        tc = CMakeToolchain(self)
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
        self.cpp_info.set_property("cmake_file_name", f"Boost")
        self.cpp_info.set_property("cmake_target_name", f"boost::boost")
        self.cpp_info.set_property("cmake_target_aliases", ["boost", "Boost"])
        # self.cpp_info.set_property("cmake_target_aliases", [f"Boost::{self.module}"])
        self.cpp_info.set_property("cmake_find_mode", "both")

        # Add components
        for dep in DEPENDENCIES:
            component = self.cpp_info.components[dep]
            component.set_property("cmake_target_name", f"boost::{dep}")
            component.set_property("cmake_target_aliases", [f"Boost::{dep}"])
            component.requires = [
                f"boost-{dep}/{self.version}@luxcorewheels/luxcorewheels"
            ]

    def package_id(self):
        # We clear everything in order to have a constant package_id and use the cache
        self.info.clear()


