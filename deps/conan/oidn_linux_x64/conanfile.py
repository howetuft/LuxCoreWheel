import os
import shutil
from conan.tools.files import get, copy, rmdir, rename, rm
from conan.tools.files.symlinks import absolute_to_relative_symlinks
from conan import ConanFile

_oidn_version = os.environ["OIDN_VERSION"]

class OidnConan(ConanFile):
    name = "oidn_linux_x64"
    version = _oidn_version
    settings = "os", "arch", "compiler", "build_type"
    user = "luxcorewheels"
    channel = "luxcorewheels"
    package_type = "unknown"
    package_id_unknown_mode = "revision_mode"

    # Nota: do not embed tbbbind: useless for CPU
    # _libs = [
        # f"libOpenImageDenoise_core.so.{_oidn_version}",
        # f"libOpenImageDenoise_device_cpu.so.{_oidn_version}",
        # f"libOpenImageDenoise.so.{_oidn_version}",
        # "libOpenImageDenoise.so",
        # "libOpenImageDenoise.so.2",
        # "libtbb.so.12.12",
        # "libtbbmalloc.so.2.12",
        # "libtbbmalloc_proxy.so.2.12",
        # "libtbb.so",
        # "libtbb.so.12",
        # "libtbbmalloc.so",
        # "libtbbmalloc.so.2",
        # "libtbbmalloc_proxy.so",
        # "libtbbmalloc_proxy.so.2",
    # ]
    _libs = [
        "libOpenImageDenoise_core.so",
        "libOpenImageDenoise_device_cpu.so",
        "libOpenImageDenoise.so",
        "libtbb.so",
        "libtbbmalloc.so",
        "libtbbmalloc_proxy.so",
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
        base_oidn = f"oidn-{self.version}.x86_64.linux"
        copy(
            self,
             "*",
             src=os.path.join(self.build_folder, base_oidn, "include"),
             dst=os.path.join(self.package_folder, "include"),
        )
        copy(
            self,
            "*",
            src=os.path.join(self.build_folder, base_oidn, "bin"),
            dst=os.path.join(self.package_folder, "bin"),
        )
        copy(
            self,
            "*.so*",
            src=os.path.join(self.build_folder, base_oidn, "lib"),
            dst=os.path.join(self.package_folder, "lib"),
        )
        # TODO
        # cmake = CMake(self)
        # cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.libs = self._libs

        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
        self.cpp_info.bindirs = ['bin']  # Directories where executables and shared libs can be found

    def _swap(self, lib1, lib2):
        path1 = os.path.join(self.build_folder, lib1)
        path2 = os.path.join(self.build_folder, lib2)
        temp = os.path.join(self.build_folder, "__temp__")

        copy(path1, temp)
        rename(path1, path2)
        rename(path2, temp)
        rm(temp)

    def _lib_path(self, name):
        return os.path.join(
            self.build_folder,
            f"oidn-{self.version}.x86_64.linux",
            "lib",
            name,
        )

    def _link(self, libname):
        rename(
            self,
            self._lib_path(f"{libname}.{self.version}"),
            self._lib_path(libname),
        )
        os.symlink(
            self._lib_path(libname),
            self._lib_path(f"{libname}.{self.version}"),
        )


    def build(self):
        url = f"https://github.com/RenderKit/oidn/releases/download/v{self.version}/oidn-{self.version}.x86_64.linux.tar.gz"
        get(self, url)
        rm(
            self,
            "libOpenImageDenoise.so",
            os.path.join(self.build_folder, f"oidn-{self.version}.x86_64.linux", "lib"),
        )
        self._link("libOpenImageDenoise_core.so")
        self._link("libOpenImageDenoise_device_cpu.so")
        self._link("libOpenImageDenoise.so")
        # rename(
            # self,
            # self._lib_path(f"libOpenImageDenoise_core.so.{self.version}"),
            # self._lib_path("libOpenImageDenoise_core.so"),
        # )
        # os.symlink(
            # self._lib_path("libOpenImageDenoise_core.so"),
            # self._lib_path(f"libOpenImageDenoise_core.so.{self.version}"),
        # )
        absolute_to_relative_symlinks(
            self,
            os.path.join(self.build_folder, f"oidn-{self.version}.x86_64.linux", "lib"),
        )


        url = f"https://github.com/oneapi-src/oneTBB/releases/download/v2021.12.0/oneapi-tbb-2021.12.0-lin.tgz"
        get(self, url)
