# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from conan import ConanFile

class LuxCore(ConanFile):
    name = "LuxCoreWheels"

    requires = [
        "opencolorio/2.3.1",
        "minizip-ng/4.0.3",
        "libpng/1.6.42",
        "ffmpeg/6.1",
        "boost/1.84.0",
        "openimageio/2.5.14.0",
    ]

    default_options = {
        "boost/*:without_python": False
    }

    generators = "CMakeDeps", "CMakeToolchain"

    settings = "os", "compiler", "build_type", "arch"

    def package_info(self):
        self.conf_info.define("tools.build:verbosity", "debug")