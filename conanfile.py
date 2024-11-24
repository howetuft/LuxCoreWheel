# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from conan import ConanFile

from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.system.package_manager import Brew, Yum
from conan.tools.env import VirtualBuildEnv
from conan.tools.files import get, copy, rmdir, rename, rm, save
import random

random.seed(0)

import os
import io

_boost_version = os.environ["BOOST_VERSION"]
_ocio_version = os.environ["OCIO_VERSION"]
_oiio_version = os.environ["OIIO_VERSION"]
_oidn_version = os.environ["OIDN_VERSION"]
_openexr_version = os.environ["OPENEXR_VERSION"]

class LuxCore(ConanFile):
    name = "luxcorewheels"
    version = "2.6.0"
    user = "luxcorewheels"
    channel = "luxcorewheels"


    requires = [
        f"opencolorio/{_ocio_version}",
        "minizip-ng/4.0.3",
        "libpng/1.6.42",
        "spdlog/1.14.1",
        f"openimageio/{_oiio_version}@luxcorewheels/luxcorewheels",
        "c-blosc/1.21.5",
        f"boost/{_boost_version}",
        f"boost-python/{_boost_version}@luxcorewheels/luxcorewheels",
        "openvdb/9.1.0",
        "eigen/3.4.0",
        "embree3/3.13.1",
    ]

    default_options = {
        "fmt/*:header_only": True,
        "spdlog/*:header_only": True,
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

        if self.settings.os == "Macos":
            self.requires("llvm-openmp/18.1.8")

        if self.settings.os == "Windows":
            self.tool_requires("winflexbison/2.5.25")

        self.requires(f"oidn/{_oidn_version}@luxcorewheels/luxcorewheels")
        # TODO
        # if self.settings.os == "Macos" and self.settings.arch == "armv8":
            # self.requires("embree3/3.13.1@luxcorewheels/luxcorewheels")
        # else:
            # self.requires("embree3/3.13.1")


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


    def package(self):
        # Just to ensure package is not empty
        save(self, os.path.join(self.package_folder, "dummy.txt"), "Hello World")

    def package_info(self):
        self.conf_info.define("cmake.build:verbosity", "debug")

        self.conf_info.define("tools.build:sharedlinkflags", ["-VERBOSE"])
        self.conf_info.define("tools.build:exelinkflags", ["-VERBOSE"])
        self.conf_info.define("tools.build:verbosity", "verbose")
        if self.settings.os == "Linux":
            self.cpp_info.libs = [
                "pyluxcore",
                "libtbbmalloc_proxy.so.2",
                "libtbbmalloc.so.2",
                "libtbb.so.12",
                "libOpenImageDenoise_core.so.2.3.0",
                "libOpenImageDenoise_device_cpu.so.2.3.0",
                "libOpenImageDenoise.so.2",
            ]
        elif self.settings.os == "Windows":
            self.cpp_info.libs = [
                "pyluxcore.pyd",
                "tbb12.dll",
            ]
