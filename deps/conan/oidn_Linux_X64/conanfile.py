import os
import shutil
from conan.tools.files import get, copy
from conan import ConanFile


class OidnConan(ConanFile):
    name = "oidn"
    # version = "1.2.4" TODO
    version = "2.3.0"
    settings = "os", "arch", "compiler", "build_type"
    user = "luxcorewheels"
    channel = "luxcorewheels"

    def layout(self):
        build_type = self.settings.get_safe("build_type", default="Release")
        # Define project folder structure
        # We directly download binaries, so it's a very simplified layout
        # (no build)...

        self.folders.source = "."
        base = f"oidn-{self.version}.x86_64.linux"
        base_tbb = "oneapi-tbb-2021.12.0"
        self.folders.build = os.path.join("build", build_type)
        self.folders.generators = os.path.join(self.folders.build, "generators")

        # Nota: do not embed tbbbind: useless for CPU
        libs = [
            f"libOpenImageDenoise_core.so.{self.version}",
            f"libOpenImageDenoise_device_cpu.so.{self.version}",
            f"libOpenImageDenoise.so.{self.version}",
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

        ## cpp.source and cpp.build information is specifically designed
        # for editable packages:
        # this information is relative to the source folder
        self.cpp.source.libs = libs
        self.cpp.source.includedirs = [os.path.join(base, "include")]
        self.cpp.source.libdirs = [
            os.path.join(base, "lib"),
            os.path.join(base_tbb, "lib", "intel64", "gcc4.8"),
        ]
        self.cpp.source.bindirs = [
            os.path.join(base, "bin"),
        ]

        # package, for deployment
        self.cpp.package.libs = libs
        self.cpp.package.libdirs = [
            os.path.join(base, "lib"),
            os.path.join(base_tbb, "lib", "intel64", "gcc4.8"),
        ]
        self.cpp.package.bindirs = [
            os.path.join(base, "bin"),
        ]

    def package_info(self):
        print("OIDN PACKAGE_INFO")

    def source(self):
        url = f"https://github.com/RenderKit/oidn/releases/download/v{self.version}/oidn-{self.version}.x86_64.linux.tar.gz"
        get(self, url)
        url = f"https://github.com/oneapi-src/oneTBB/releases/download/v2021.12.0/oneapi-tbb-2021.12.0-lin.tgz"
        get(self, url)
