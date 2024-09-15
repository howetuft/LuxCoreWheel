# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from conan import ConanFile

from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout

class LuxCore(ConanFile):
    name = "LuxCoreWheels"

    _boost_version = "1.78.0"

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
        # f"boost/{_boost_version}",
        f"boost/{_boost_version}@luxcorewheels/luxcorewheels",
        f"boost-interprocess/{_boost_version}@luxcorewheels/luxcorewheels",
        f"boost-python/{_boost_version}@luxcorewheels/luxcorewheels",
        f"boost-atomic/{_boost_version}@luxcorewheels/luxcorewheels",
        f"boost-chrono/{_boost_version}@luxcorewheels/luxcorewheels",
        f"boost-system/{_boost_version}@luxcorewheels/luxcorewheels",
        f"boost-filesystem/{_boost_version}@luxcorewheels/luxcorewheels",
        f"boost-container/{_boost_version}@luxcorewheels/luxcorewheels",
        f"boost-date_time/{_boost_version}@luxcorewheels/luxcorewheels",
        f"boost-iostreams/{_boost_version}@luxcorewheels/luxcorewheels",
        f"boost-program_options/{_boost_version}@luxcorewheels/luxcorewheels",
        f"boost-random/{_boost_version}@luxcorewheels/luxcorewheels",
        f"boost-serialization/{_boost_version}@luxcorewheels/luxcorewheels",
        f"boost-thread/{_boost_version}@luxcorewheels/luxcorewheels",
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
