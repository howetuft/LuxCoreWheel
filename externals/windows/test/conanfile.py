# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from conan import ConanFile

from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout

class Test(ConanFile):
    name = "LuxCoreWheels"

    requires = [
        "oidn/2.3.0@luxcorewheels/luxcorewheels",
        "openimageio/2.2.13.1@luxcorewheels/luxcorewheels",
    ]

    default_options = {
    }

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

        cd = CMakeDeps(self)
        cd.generate()

    settings = "os", "compiler", "build_type", "arch"


    def package_info(self):
        self.conf_info.define("cmake.build:verbosity", "debug")

    def package_id(self):
        # We clear everything in order to have a constant package_id and use the cache
        self.info.clear()
