# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from conan import ConanFile

from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout

_boost_version = "1.78.0"

class LuxCore(ConanFile):
    name = "LuxCoreWheels"


    requires = [
        "onetbb/2020.3",
        "opencolorio/2.1.0",
        "minizip-ng/4.0.3",
        "libpng/1.6.42",
        "spdlog/1.8.5",
        "openimageio/2.2.13.1@luxcorewheels/luxcorewheels",
        "embree3/3.13.1",
        "c-blosc/1.21.5",
        "oidn/2.3.0@luxcorewheels/luxcorewheels",
        "openexr/2.5.7",
        f"boost/{_boost_version}@luxcorewheels/luxcorewheels",
    ]

    default_options = {
        "fmt/*:header_only": True,
        "spdlog/*:header_only": True,
    }

    settings = "os", "compiler", "build_type", "arch"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.absolute_paths = True
        tc.preprocessor_definitions["OIIO_STATIC_DEFINE"] = True
        tc.preprocessor_definitions["SPDLOG_FMT_EXTERNAL"] = True
        tc.generate()

        cd = CMakeDeps(self)
        # Alternative filenames
        cd.set_property("openexr", "cmake_file_name", "OPENEXR")
        cd.set_property("c-blosc", "cmake_file_name", "Blosc")

        cd.generate()

    def layout(self):
        cmake_layout(self)



    def package_info(self):
        self.conf_info.define("cmake.build:verbosity", "debug")

        self.conf_info.define("tools.build:sharedlinkflags", ["-VERBOSE"])
        self.conf_info.define("tools.build:exelinkflags", ["-VERBOSE"])
        self.conf_info.define("tools.build:verbosity", "verbose")

    def package_id(self):
        # We clear everything in order to have a constant package_id and use the cache
        self.info.clear()
