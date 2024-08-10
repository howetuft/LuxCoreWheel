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

    _boost_all_options = (
    "atomic",
    "charconv",
    "chrono",
    "cobalt",
    "container",
    "context",
    "contract",
    "coroutine",
    "date_time",
    "exception",
    "fiber",
    "filesystem",
    "graph",
    "graph_parallel",
    "iostreams",
    "json",
    "locale",
    "log",
    "math",
    "mpi",
    "nowide",
    "program_options",
    "python",
    "random",
    "regex",
    "serialization",
    "stacktrace",
    "system",
    "test",
    "thread",
    "timer",
    "type_erasure",
    "url",
    "wave",
)

    _boost_required_options = {
        "thread",
        "program_options",
        "filesystem",
        "serialization",
        "iostreams",
        "regexs",
        "system",
        "python",
        "chrono",
        "serialization",
        "numpy",
    }

    default_options = {
        f"boost/*:without_{option}": option not in LuxCore._boost_required_options
        for option in LuxCore._boost_all_options
    }

    generators = "CMakeDeps", "CMakeToolchain"

    settings = "os", "compiler", "build_type", "arch"

    def package_info(self):
        self.conf_info.define("tools.build:verbosity", "debug")