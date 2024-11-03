import os
import shutil
from conan.tools.files import get, copy
from conan import ConanFile

VERSION = "2.1.0"

# Specialized libs (device_cuda, device_hip etc.) require additional deps, and
# make wheel repairing fail, so we won't embed them
LIBS = [
    "libOpenImageDenoise.so",
    "libOpenImageDenoise.so.2",
    f"libOpenImageDenoise.so.{VERSION}",
    f"libOpenImageDenoise_core.so.{VERSION}",
    f"libOpenImageDenoise_device_cpu.so.{VERSION}",
    # f"libOpenImageDenoise_device_cuda.so.{VERSION}",
    # f"libOpenImageDenoise_device_hip.so.{VERSION}",
    # f"libOpenImageDenoise_device_sycl.so.{VERSION}",
    # "libpi_level_zero.so",
    # "libsycl.so.7",
    # "libsycl.so.7.0.0-8",
    "libtbb.so",
    "libtbb.so.12",
    "libtbb.so.12.10",
    "libtbbbind.so.3",
    "libtbbbind.so.3.10",
    "libtbbbind_2_0.so.3",
    "libtbbbind_2_0.so.3.10",
    "libtbbbind_2_5.so.3",
    "libtbbbind_2_5.so.3.10",
]


class OidnConan(ConanFile):
    name = "oidn"
    version = VERSION
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
        self.folders.build = os.path.join("build", build_type)
        self.folders.generators = os.path.join(self.folders.build, "generators")

        ## cpp.source and cpp.build information is specifically designed
        # for editable packages:
        # this information is relative to the source folder
        self.cpp.source.libs = LIBS
        self.cpp.source.includedirs = [os.path.join(base, "include")]
        self.cpp.source.libdirs = [os.path.join(base, "lib")]
        self.cpp.source.bindirs = [os.path.join(base, "bin")]

        # package, for deployment
        self.cpp.package.libs = LIBS
        self.cpp.package.libdirs = [os.path.join(base, "lib")]
        self.cpp.package.bindirs = [os.path.join(base, "bin")]

    def package_info(self):
        print("OIDN PACKAGE_INFO")

    def source(self):
        url = f"https://github.com/RenderKit/oidn/releases/download/v{self.version}/oidn-{self.version}.x86_64.linux.tar.gz"
        get(self, url)
