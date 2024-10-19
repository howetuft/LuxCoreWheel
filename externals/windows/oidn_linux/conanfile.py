import os
import shutil
from conan.tools.files import get, copy
from conan import ConanFile


class OidnConan(ConanFile):
    name = "oidn"
    version = "1.2.4"
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
        self.cpp.source.libs = [
            "libOpenImageDenoise.so",
            "libOpenImageDenoise.so.0",
            f"libOpenImageDenoise.so.{self.version}",
            # f"libOpenImageDenoise_core.so.{self.version}",
            # f"libOpenImageDenoise_device_cpu.so.{self.version}",
            # f"libOpenImageDenoise_device_cuda.so.{self.version}",
            # f"libOpenImageDenoise_device_hip.so.{self.version}",
            # f"libOpenImageDenoise_device_sycl.so.{self.version}",
            # "pi_level_zero",
            # "libsycl.so.7",
            # "libsycl.so.7.1.0-8",
            "libtbb.so.2",
            "libtbbmalloc.so.2",
            # "libtbbbind.so.3",
            # "libtbbbind.so.3.12",
            # "libtbbbind_2_0.so.3",
            # "libtbbbind_2_0.so.3.12",
            # "libtbbbind_2_5.so.3",
            # "libtbbbind_2_5.so.3.12",
        ]
        self.cpp.source.includedirs = [os.path.join(base, "include")]
        self.cpp.source.libdirs = [os.path.join(base, "lib")]
        self.cpp.source.bindirs = [os.path.join(base, "bin")]

    def source(self):
        url = f"https://github.com/RenderKit/oidn/releases/download/v{self.version}/oidn-{self.version}.x86_64.linux.tar.gz"
        get(self, url)
