import os
import shutil
from conan.tools.files import get, copy, rmdir, rename, rm
from conan.tools.files.symlinks import absolute_to_relative_symlinks
from conan import ConanFile

_oidn_version = os.environ["OIDN_VERSION"]

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

    # TODO
    # def layout(self):
        # build_type = self.settings.get_safe("build_type", default="Release")
        # # Define project folder structure
        # # We directly download binaries, so it's a very simplified layout
        # # (no build)...

        # self.folders.source = "."
        # base = f"oidn-{self.version}.x86_64.linux"
        # base_tbb = "oneapi-tbb-2021.12.0"
        # self.folders.build = os.path.join("build", build_type)
        # self.folders.generators = os.path.join(self.folders.build, "generators")


        # ## cpp.source and cpp.build information is specifically designed
        # # for editable packages:
        # # this information is relative to the source folder
        # self.cpp.source.libs = self._libs
        # self.cpp.source.includedirs = [os.path.join(base, "include")]
        # self.cpp.source.libdirs = [
            # os.path.join(base, "lib"),
            # os.path.join(base_tbb, "lib", "intel64", "gcc4.8"),
        # ]
        # self.cpp.source.bindirs = [
            # os.path.join(base, "bin"),
        # ]

        # # package, for deployment
        # self.cpp.package.libs = self._libs
        # self.cpp.package.libdirs = [
            # os.path.join(base, "lib"),
            # os.path.join(base_tbb, "lib", "intel64", "gcc4.8"),
        # ]
        # self.cpp.package.bindirs = [
            # os.path.join(base, "bin"),
        # ]

    # https://docs.conan.io/2/tutorial/creating_packages/other_types_of_packages/package_prebuilt_binaries.html

    def package(self):
        if self.settings.os == "Linux":
            base_oidn = os.path.join(
                self.build_folder,
                f"oidn-{self.version}.x86_64.linux",
            )
            base_tbb = os.path.join(
                self.build_folder,
                "oneapi-tbb-2021.12.0",
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
                "*.so*",
                src=os.path.join(base_oidn, "lib"),
                dst=os.path.join(self.package_folder, "lib"),
            )

            # Tbb
            copy(
                self,
                "*.so*",
                src=os.path.join(base_tbb, "lib", "intel64", "gcc4.8"),
                dst=os.path.join(self.package_folder, "lib"),
            )

            rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

        elif self.settings.os == "Windows":
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
                "*.lib",
                src=os.path.join(base_oidn, "lib"),
                dst=os.path.join(self.package_folder, "lib"),
            )
            rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        if self.settings.os == "Linux":
            self.cpp_info.libs = self._libs_linux
        elif self.settings.os == "Windows":
            self.cpp_info.libs = self._libs_windows


        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
        self.cpp_info.bindirs = ['bin']  # Directories where executables and shared libs can be found


    def build(self):
        if self.settings.os == "Linux":
            url_oidn = f"https://github.com/RenderKit/oidn/releases/download/v{self.version}/oidn-{self.version}.x86_64.linux.tar.gz"
            url_tbb = f"https://github.com/oneapi-src/oneTBB/releases/download/v2021.12.0/oneapi-tbb-2021.12.0-lin.tgz"
            get(self, url_oidn)
            get(self, url_tbb)

        elif self.settings.os == "Windows":
            url = f"https://github.com/RenderKit/oidn/releases/download/v{self.version}/oidn-{self.version}.x64.windows.zip"
            get(self, url)
