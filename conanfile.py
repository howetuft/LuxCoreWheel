# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from conan import ConanFile

class LuxCore(ConanFile):
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