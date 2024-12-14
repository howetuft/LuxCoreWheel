# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

import os
import shutil
from conan.tools.files import get, copy, rmdir, rename, rm
from conan.tools.files.symlinks import absolute_to_relative_symlinks
from conan import ConanFile

_oidn_version = os.environ["OIDN_VERSION"]
_tbb_version = os.environ["TBB_VERSION"]

class OidnConan(ConanFile):
    name = "oidn"
    version = _oidn_version
    user = "luxcorewheels"
    channel = "luxcorewheels"
    settings = "os", "arch", "compiler", "build_type"
    package_type = "unknown"
    package_id_unknown_mode = "revision_mode"

    # Nota: do not embed tbbbind: useless for CPU
    _libs_linux = [
        f"libOpenImageDenoise_core.so.{_oidn_version}",
        f"libOpenImageDenoise_device_cpu.so.{_oidn_version}",
        f"libOpenImageDenoise.so.{_oidn_version}",
        "libOpenImageDenoise.so",
        "libOpenImageDenoise.so.2",
        "libtbb.so.12.12",
        "libtbbmalloc.so.2.12",
        "libtbbmalloc_proxy.so.2.12",
        "libtbb.so",
        "libtbb.so.12",
        "libtbbmalloc.so",
        "libtbbmalloc.so.2",
        "libtbbmalloc_proxy.so",
        "libtbbmalloc_proxy.so.2",
    ]

    _libs_windows = [
        "OpenImageDenoise_core",
        "OpenImageDenoise",
    ]

    _libs_macos13 = [
        f"OpenImageDenoise.{_oidn_version}",
        "OpenImageDenoise.2",
        "OpenImageDenoise",
        f"OpenImageDenoise_core.{_oidn_version}",
        f"OpenImageDenoise_device_cpu.{_oidn_version}",
    ]

    _libs_macos14 = [
        f"OpenImageDenoise.{_oidn_version}",
        "OpenImageDenoise.2",
        "OpenImageDenoise",
        f"OpenImageDenoise_core.{_oidn_version}",
        f"OpenImageDenoise_device_cpu.{_oidn_version}",
        f"OpenImageDenoise_device_metal.{_oidn_version}",
    ]

    # https://docs.conan.io/2/tutorial/creating_packages/other_types_of_packages/package_prebuilt_binaries.html

    def _package_linux(self):
        base_oidn = os.path.join(
            self.build_folder,
            f"oidn-{self.version}.x86_64.linux",
        )
        base_tbb = os.path.join(
            self.build_folder,
            f"oneapi-tbb-{_tbb_version}",
        )

        # Oidn
        copy(
            self,
             "*",
             src=os.path.join(base_oidn, "include"),
             dst=os.path.join(self.package_folder, "include"),
        )
        copy(
            self,
            "*",
            src=os.path.join(base_oidn, "bin"),
            dst=os.path.join(self.package_folder, "bin"),
        )
        copy(
            self,
            "*",
            src=os.path.join(base_oidn, "lib"),
            dst=os.path.join(self.package_folder, "lib"),
        )

        # Tbb
        copy(
            self,
            "*",
            src=os.path.join(base_tbb, "lib", "intel64", "gcc4.8"),
            dst=os.path.join(self.package_folder, "lib"),
        )


    def _package_windows(self):
        base_oidn = os.path.join(
            self.build_folder,
            f"oidn-{self.version}.x64.windows",
        )
        # Oidn
        copy(
            self,
             "*",
             src=os.path.join(base_oidn, "include"),
             dst=os.path.join(self.package_folder, "include"),
        )
        copy(
            self,
            "*",
            src=os.path.join(base_oidn, "bin"),
            dst=os.path.join(self.package_folder, "bin"),
        )
        copy(
            self,
            "*",
            src=os.path.join(base_oidn, "lib"),
            dst=os.path.join(self.package_folder, "lib"),
        )

    def _package_macos13(self):
        base_oidn = os.path.join(
            self.build_folder,
            f"oidn-{self.version}.x86_64.macos",
        )
        copy(
            self,
             "*",
             src=os.path.join(base_oidn, "include"),
             dst=os.path.join(self.package_folder, "include"),
        )
        copy(
            self,
            "*",
            src=os.path.join(base_oidn, "bin"),
            dst=os.path.join(self.package_folder, "bin"),
        )
        copy(
            self,
            "*",
            src=os.path.join(base_oidn, "lib"),
            dst=os.path.join(self.package_folder, "lib"),
        )
        rm(self, "libtbb.12.12.dylib", os.path.join(self.package_folder, "lib"))

    def _package_macos14(self):
        base_oidn = os.path.join(
            self.build_folder,
            f"oidn-{self.version}.arm64.macos",
        )
        copy(
            self,
             "*",
             src=os.path.join(base_oidn, "include"),
             dst=os.path.join(self.package_folder, "include"),
        )
        copy(
            self,
            "*",
            src=os.path.join(base_oidn, "bin"),
            dst=os.path.join(self.package_folder, "bin"),
        )
        copy(
            self,
            "*",
            src=os.path.join(base_oidn, "lib"),
            dst=os.path.join(self.package_folder, "lib"),
        )
        rm(self, "libtbb.12.12.dylib", os.path.join(self.package_folder, "lib"))

    def package(self):
        os_ = self.settings.os  # Beware: potential name collision with module os
        arch = self.settings.arch
        if os_ == "Linux":
            self._package_linux()
        elif os_ == "Windows":
            self._package_windows()
        elif os_ == "Macos" and arch == "x86_64":
            self._package_macos13()
        elif os_ == "Macos" and arch == "armv8":
            self._package_macos14()
        else:
            raise ValueError("Unhandled os/arch")
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        os_ = self.settings.os  # Beware: potential name collision with module os
        arch = self.settings.arch
        if os_ == "Linux":
            self.cpp_info.libs = self._libs_linux
        elif os_ == "Windows":
            self.cpp_info.libs = self._libs_windows
        elif os_ == "Macos" and arch == "x86_64":
            self.cpp_info.libs = self._libs_macos13
        elif os_ == "Macos" and arch == "armv8":
            self.cpp_info.libs = self._libs_macos14
        else:
            raise ValueError("Unhandled os/arch")

        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
        self.cpp_info.bindirs = ['bin']  # Directories where executables and shared libs can be found
        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bin_path))
        self.env_info.PATH.append(bin_path)

    def build(self):
        os_ = self.settings.os  # Beware: potential name collision with module os
        arch = self.settings.arch
        version = self.version
        base = "https://github.com/RenderKit/oidn/releases/download"

        # For all: get oidn
        if os_ == "Linux":
            url = f"{base}/v{version}/oidn-{version}.x86_64.linux.tar.gz"
        elif os_ == "Windows":
            url = f"{base}/v{version}/oidn-{version}.x64.windows.zip"
        elif os_ == "Macos" and arch == "x86_64":
            url = f"{base}/v{version}/oidn-{version}.x86_64.macos.tar.gz"
        elif os_ == "Macos" and arch == "armv8":
            url = f"{base}/v{version}/oidn-{version}.arm64.macos.tar.gz"
        else:
            raise ValueError("Unhandled os/arch")

        get(self, url)

        # For Linux: get tbb
        if os_ == "Linux":
            base = "https://github.com/oneapi-src/oneTBB/releases/download"
            url_tbb = f"{base}/v{_tbb_version}/oneapi-tbb-{_tbb_version}-lin.tgz"
            get(self, url_tbb)
