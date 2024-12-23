# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

import os
import shutil
from pathlib import Path
from conan.tools.files import get, copy, rmdir, rename, rm
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan import ConanFile
from conan.tools.scm import Git

_oidn_version = os.environ["OIDN_VERSION"]
_tbb_version = os.environ["TBB_VERSION"]

class OidnConan(ConanFile):
    name = "oidn"
    version = _oidn_version
    user = "luxcorewheels"
    channel = "luxcorewheels"
    settings = "os", "arch", "compiler", "build_type"
    package_type = "library"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_device_cpu": [True, False],
        "with_device_sycl": [True, False],
        "with_device_sycl_aot": [True, False],
        "with_device_cuda": [True, False],
        "device_cuda_api": ["Driver", "RuntimeStatic", "RuntimeShared"],
        "with_device_hip": [True, False],
        "with_device_metal": [True, False],
        "with_filter_rt": [True, False],
        "with_filter_rtlightmap": [True, False],
        "with_apps": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "with_device_cpu": True,
        "with_device_sycl": False,
        "with_device_sycl_aot": True,
        "with_device_cuda": False,
        "device_cuda_api": "Driver",
        "with_device_hip": False,
        "with_device_metal": False,
        "with_filter_rt": True,
        "with_filter_rtlightmap": True,
        "with_apps": True,
    }

    def requirements(self):
        # TODO
        # if self.settings.os == "Linux":
            # self.requires("level-zero/1.17.39")
        self.requires(f"onetbb/{_tbb_version}")

    def source(self):
        git = Git(self)
        res = git.run("lfs install")
        print(res)
        git.clone(
            "https://github.com/OpenImageDenoise/oidn.git",
            args=["--recursive", f"--branch v{_oidn_version}"],
            target=Path(self.source_folder) / "oidn"
        )

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["OIDN_STATIC_LIB"] = not self.options.shared

        tc.variables["OIDN_DEVICE_CPU"] = self.options.with_device_cpu
        tc.variables["OIDN_DEVICE_SYCL"] = self.options.with_device_sycl
        tc.variables["OIDN_DEVICE_SYCL_AOT"] = self.options.with_device_sycl_aot
        tc.variables["OIDN_DEVICE_CUDA"] = self.options.with_device_cuda
        tc.variables["OIDN_DEVICE_CUDA_API"] = self.options.device_cuda_api
        tc.variables["OIDN_DEVICE_HIP"] = self.options.with_device_hip
        tc.variables["OIDN_DEVICE_METAL"] = self.options.with_device_metal
        tc.variables["OIDN_FILTER_RT"] = self.options.with_filter_rt
        tc.variables["OIDN_FILTER_RTLIGHTMAP"] = self.options.with_filter_rtlightmap
        tc.variables["OIDN_APPS"] = self.options.with_apps
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(cli_args=[], build_script_folder=Path(self.folders.source) / "oidn")
        cmake.build(cli_args=["--verbose", "--clean-first"])

    def package(self):
        copy(
            self,
            "LICENSE.txt",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "licenses"),
        )
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "cmake"))
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "share"))

    def package_info(self):
        if self.options.shared:
            # Shared
            if self.settings.os == "Linux":
                self.cpp_info.libs = [
                    "OpenImageDenoise",
                    f"libOpenImageDenoise_device_cpu.so.{_oidn_version}",
                    f"libOpenImageDenoise_core.so.{_oidn_version}",
                ]
            elif self.settings.os == "Windows":
                self.cpp_info.libs = [
                    "OpenImageDenoise",
                    "OpenImageDenoise_core",
                ]
        else:
            # Static
            # Warning: library order matters!
            self.cpp_info.libs = [
                "OpenImageDenoise",
                "OpenImageDenoise_device_cpu",
                "OpenImageDenoise_core",
            ]
