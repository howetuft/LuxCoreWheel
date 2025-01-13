# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from conan import ConanFile

from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.system.package_manager import Brew, Yum
from conan.tools.env import VirtualBuildEnv
from conan.tools.files import get, copy, rmdir, rename, rm, save

import os
import io
import shutil
from pathlib import Path

_boost_version = os.environ["BOOST_VERSION"]
_ocio_version = os.environ["OCIO_VERSION"]
_oiio_version = os.environ["OIIO_VERSION"]
_oidn_version = os.environ["OIDN_VERSION"]
_openexr_version = os.environ["OPENEXR_VERSION"]
_blender_version = os.environ["BLENDER_VERSION"]
_openvdb_version = os.environ["OPENVDB_VERSION"]
_tbb_version = os.environ["TBB_VERSION"]
_spdlog_version = os.environ["SPDLOG_VERSION"]
_embree3_version = os.environ["EMBREE3_VERSION"]
_fmt_version = os.environ["FMT_VERSION"]

class LuxCore(ConanFile):
    name = "luxcorewheels"
    version = "2.9alpha1"
    user = "luxcorewheels"
    channel = "luxcorewheels"


    requires = [
        f"opencolorio/{_ocio_version}",
        "minizip-ng/4.0.3",
        "libpng/1.6.42",
        f"spdlog/{_spdlog_version}",
        f"openimageio/{_oiio_version}@luxcorewheels/luxcorewheels",
        "c-blosc/1.21.5",
        f"boost/{_boost_version}",
        f"boost-python/{_boost_version}@luxcorewheels/luxcorewheels",
        f"openvdb/{_openvdb_version}",
        "eigen/3.4.0",
        f"embree3/{_embree3_version}",
        "tsl-robin-map/1.2.1",
        f"blender-types/{_blender_version}@luxcorewheels/luxcorewheels",
        f"oidn/{_oidn_version}@luxcorewheels/luxcorewheels",
    ]

    default_options = {
        "fmt/*:header_only": True,
        "spdlog/*:header_only": True,
        "openimageio/*:with_ffmpeg": False,
        "embree3/*:neon": True,
    }

    settings = "os", "compiler", "build_type", "arch"

    # Note: LuxCoreRender is sourced by Github action (see Checkout LuxCoreRender)

    def requirements(self):
        self.requires(
            f"onetbb/{_tbb_version}",
            override=True,
            libs=True,
            transitive_libs=True,
        )  # For oidn
        self.requires("imath/3.1.9", override=True)
        self.requires(f"fmt/{_fmt_version}", override=True)

        if self.settings.os == "Macos":
            self.requires("llvm-openmp/18.1.8")

        if self.settings.os == "Windows":
            self.tool_requires("winflexbison/2.5.25")

    def build_requirements(self):
       self.tool_requires("cmake/*")
       self.tool_requires("meson/*")
       self.tool_requires("ninja/*")
       self.tool_requires("pkgconf/*")
       self.tool_requires("yasm/*")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.absolute_paths = True
        tc.preprocessor_definitions["OIIO_STATIC_DEFINE"] = True
        tc.preprocessor_definitions["SPDLOG_FMT_EXTERNAL"] = True
        tc.variables["CMAKE_COMPILE_WARNING_AS_ERROR"] = False

        # OIDN denoiser executable
        oidn_info = self.dependencies["oidn"].cpp_info
        oidn_bindir = Path(oidn_info.bindirs[0])
        if self.settings.os == "Windows":
            denoise_path = oidn_bindir / "oidnDenoise.exe"
        else:
            denoise_path = oidn_bindir / "oidnDenoise"
        tc.variables["LUX_OIDN_DENOISE_PATH"] = denoise_path.as_posix()

        # OIDN denoiser cpu (for Linux)
        oidn_libdir = Path(oidn_info.libdirs[0])
        tc.variables["LUX_OIDN_DENOISE_LIBS"] = oidn_libdir.as_posix()
        tc.variables["LUX_OIDN_DENOISE_BINS"] = oidn_bindir.as_posix()
        tc.variables["LUX_OIDN_VERSION"] = _oidn_version
        if self.settings.os == "Linux":
            denoise_cpu = oidn_libdir / f"libOpenImageDenoise_device_cpu.so.{_oidn_version}"
        elif self.settings.os == "Windows":
            denoise_cpu = oidn_bindir / "OpenImageDenoise_device_cpu.dll"
        elif self.settings.os == "Macos":
            denoise_cpu = oidn_libdir / f"OpenImageDenoise_device_cpu.{_oidn_version}.pylib"
        tc.variables["LUX_OIDN_DENOISE_CPU"] = denoise_cpu.as_posix()

        if self.settings.os == "Macos" and self.settings.arch == "armv8":
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

    def package(self):
        # Just to ensure package is not empty
        save(self, os.path.join(self.package_folder, "dummy.txt"), "Hello World")

    def layout(self):
        cmake_layout(self)

    def package_info(self):

        if self.settings.os == "Linux":
            self.cpp_info.libs = ["pyluxcore"]
        elif self.settings.os == "Windows":
            self.cpp_info.libs = [
                "pyluxcore.pyd",
                "tbb12.dll",
            ]
