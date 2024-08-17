# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from conan import ConanFile

from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout

class LuxCore(ConanFile):
    name = "LuxCoreWheels"

    requires = [
        "onetbb/2020.3",
        "opencolorio/2.1.0",
        "minizip-ng/4.0.3",
        "libpng/1.6.42",
        "boost/1.78.0",
        "llvm-openmp/18.1.8",
        "spdlog/1.8.5",
        "openimageio/2.2.13.1@luxcorewheels/luxcorewheels",
        "embree3/3.13.1",
        "c-blosc/1.21.5",
        "openexr/2.5.7",
        "oidn/2.3.0@luxcorewheels/luxcorewheels",
    ]

    default_options = {
        "boost/*:without_atomic": False,
        "boost/*:without_charconv": True,
        "boost/*:without_chrono": False,
        "boost/*:without_cobalt": True,
        "boost/*:without_container": False,
        "boost/*:without_context": True,
        "boost/*:without_contract": True,
        "boost/*:without_coroutine": True,
        "boost/*:without_date_time": False,
        "boost/*:without_exception": False,
        "boost/*:without_fiber": True,
        "boost/*:without_filesystem": False,
        "boost/*:without_graph": True,
        "boost/*:without_graph_parallel": True,
        "boost/*:without_iostreams": False,
        "boost/*:without_json": True,
        "boost/*:without_locale": True,
        "boost/*:without_log": True,
        "boost/*:without_math": True,
        "boost/*:without_mpi": True,
        "boost/*:without_nowide": True,
        "boost/*:without_program_options": False,
        "boost/*:without_python": False,
        "boost/*:without_random": False,
        "boost/*:without_regex": False,
        "boost/*:without_serialization": False,
        "boost/*:without_stacktrace": True,
        "boost/*:without_system": False,
        "boost/*:without_test": True,
        "boost/*:without_thread": False,
        "boost/*:without_timer": True,
        "boost/*:without_type_erasure": True,
        "boost/*:without_url": True,
        "boost/*:without_wave": True,
        "fmt/*:header_only": True,
    }

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

        cd = CMakeDeps(self)
        cd.set_property("openexr", "cmake_file_name", "OPENEXR")
        cd.generate()

    settings = "os", "compiler", "build_type", "arch"


    def package_info(self):
        self.conf_info.define("cmake.build:verbosity", "debug")

    def package_id(self):
        # We clear everything in order to have a constant package_id and use the cache
        self.info.clear()
