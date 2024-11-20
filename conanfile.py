# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from conan import ConanFile

from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.system.package_manager import Brew, Yum
from conan.tools.env import VirtualBuildEnv
import random

random.seed(0)

import os
import io

_boost_version = os.environ["BOOST_VERSION"]
_ocio_version = os.environ["OCIO_VERSION"]

class LuxCore(ConanFile):
    name = "LuxCoreWheels"


    requires = [
        f"opencolorio/{_ocio_version}",
        "minizip-ng/4.0.3",
        "libpng/1.6.42",
        "spdlog/1.14.1",
        # "openimageio/2.2.13.1@luxcorewheels/luxcorewheels",  # TODO
        "openimageio/2.5.16.0@luxcorewheels/luxcorewheels",
        "c-blosc/1.21.5",
        f"boost/{_boost_version}",
        f"boost-python/{_boost_version}@luxcorewheels/luxcorewheels",
        "openvdb/9.1.0",
        "oidn/2.3.0@luxcorewheels/luxcorewheels",
        "eigen/3.4.0",
    ]

    default_options = {
        # TODO
        "fmt/*:header_only": True,
        "spdlog/*:header_only": True,
        # "spdlog/*:use_std_fmt": True,
        "openimageio/*:with_ffmpeg": False,
        "openimageio/*:with_ptex": False,
        "embree3/*:neon": True,
    }

    settings = "os", "compiler", "build_type", "arch"


    def requirements(self):
        self.requires(
            "onetbb/2021.12.0",
            override=True,
            libs=True,
            transitive_libs=True,
        )  # For oidn
        self.requires("imath/3.1.9", override=True)
        self.requires("openexr/3.1.9", override=True)

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

        if self.settings.os == "Linux":
            self.cpp.package.libs = [
                "pyluxcore",
                "libtbb.so.12",
                "libtbbmalloc_proxy.so.2",
                "libtbbmalloc.so.2",
            ]
        self.folders.build_folder_vars = ["const.luxcore"]

    def package_info(self):
        self.conf_info.define("cmake.build:verbosity", "debug")

        self.conf_info.define("tools.build:sharedlinkflags", ["-VERBOSE"])
        self.conf_info.define("tools.build:exelinkflags", ["-VERBOSE"])
        self.conf_info.define("tools.build:verbosity", "verbose")
        if self.settings.os == "Linux":
            self.cpp_info.libs = [
                "pyluxcore",
                "libtbb.so.12",
                "libtbbmalloc_proxy.so.2",
                "libtbbmalloc.so.2",
            ]

    def package_id(self):
        # We clear everything in order to have a constant package_id and use the cache
        self.info.clear()
