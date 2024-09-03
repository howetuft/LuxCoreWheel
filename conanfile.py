# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from conan import ConanFile

from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout

class LuxCore(ConanFile):
    name = "LuxCoreWheels"

    requires = [
        "eigen/3.3.7",
        "openvdb/8.0.1",
        "opensubdiv/3.4.4",
        "onetbb/2020.3",
        "opencolorio/2.1.0",
        "minizip-ng/4.0.3",
        "libpng/1.6.42",
        "llvm-openmp/18.1.8",
        "spdlog/1.8.5",
        "openimageio/2.2.13.1@luxcorewheels/luxcorewheels",
        "embree3/3.13.1",
        "c-blosc/1.21.5",
        "openexr/2.5.7",
        "oidn/2.3.0@luxcorewheels/luxcorewheels",
        "boost/1.78.0",
        "boost-python/1.78.0",
        "boost-atomic/1.78.0",
        "boost-chrono/1.78.0",
        "boost-system/1.78.0",
        "boost-filesystem/1.78.0",
        "boost-container/1.78.0",
        "boost-date_time/1.78.0",
        "boost-iostreams/1.78.0",
        "boost-program_options/1.78.0",
        "boost-random/1.78.0",
        "boost-serialization/1.78.0",
        "boost-thread/1.78.0",
    ]

    default_options = {
        "fmt/*:header_only": True,
    }

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

        cd = CMakeDeps(self)
        cd.set_property("openexr", "cmake_file_name", "OPENEXR")
        cd.set_property("c-blosc", "cmake_file_name", "Blosc")
        cd.generate()

    settings = "os", "compiler", "build_type", "arch"


    def package_info(self):
        self.conf_info.define("cmake.build:verbosity", "debug")

    def package_id(self):
        # We clear everything in order to have a constant package_id and use the cache
        self.info.clear()
