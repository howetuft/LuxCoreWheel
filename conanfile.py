# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from conan import ConanFile

from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.system.package_manager import Brew, Yum
from conan.tools.env import VirtualBuildEnv

import os
import io

_boost_version = os.environ["BOOST_VERSION"]
_oiio_version = os.environ["OIIO_VERSION"]

class LuxCore(ConanFile):
    name = "LuxCoreWheels"


    requires = [
        "onetbb/2020.3",
        "opencolorio/2.3.1",
        "minizip-ng/4.0.3",
        # "libpng/1.6.42",
        "spdlog/1.14.1",
        f"openimageio/{_oiio_version}@luxcorewheels/luxcorewheels",
        "c-blosc/1.21.5",
        "openexr/3.2.3",
    ]

    default_options = {
        # "fmt/*:header_only": True,
        "spdlog/*:header_only": True,
        "spdlog/*:use_std_fmt": True,
        "embree3/*:neon": True,
    }

    settings = "os", "compiler", "build_type", "arch"


    def requirements(self):
        self.requires(f"boost/{_boost_version}", force=True)
        self.requires(f"boost-python/{_boost_version}@luxcorewheels/luxcorewheels")
        self.requires(f"fmt/10.2.1", override=True)
        if self.settings.os == "Linux":
            self.requires("oidn/1.2.4@luxcorewheels/luxcorewheels")
        else:
            self.requires("oidn/2.3.0@luxcorewheels/luxcorewheels")
        if self.settings.os == "Macos":
            self.requires("llvm-openmp/18.1.8")
        if self.settings.os == "Windows":
            self.tool_requires("winflexbison/2.5.25")

        if self.settings.os == "Macos" and self.settings.arch == "armv8":
            self.requires("embree3/3.13.1@luxcorewheels/luxcorewheels")
        else:
            self.requires("embree3/3.13.1")


    def generate(self):
        tc = CMakeToolchain(self)
        tc.absolute_paths = True
        tc.preprocessor_definitions["OIIO_STATIC_DEFINE"] = True
        tc.preprocessor_definitions["SPDLOG_FMT_EXTERNAL"] = True
        tc.variables["CMAKE_COMPILE_WARNING_AS_ERROR"] = False

        if self.settings.os == "Macos" and "arm" in self.settings.arch:
            tc.cache_variables["CMAKE_OSX_ARCHITECTURES"] = "arm64"

        if self.settings.os == "Macos":
            buildenv = VirtualBuildEnv(self)

            bisonbrewpath = io.StringIO()
            self.run("brew --prefix bison", stdout=bisonbrewpath)
            bison_root = os.path.join(bisonbrewpath.getvalue().rstrip(),"bin")
            buildenv.environment().define("BISON_ROOT", bison_root)

            flexbrewpath = io.StringIO()
            self.run("brew --prefix flex", stdout=flexbrewpath)
            flex_root = os.path.join(flexbrewpath.getvalue().rstrip(),"bin")
            buildenv.environment().define("FLEX_ROOT", flex_root)

            buildenv.generate()
            tc.presets_build_environment = buildenv.environment()

        tc.generate()

        cd = CMakeDeps(self)

        # Alternative filenames
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
