import os
import shutil
from conan.tools.files import get, copy
from conan import ConanFile


class OidnConan(ConanFile):
    name = "oidn"
    version = "2.3.0"
    settings = "os", "arch", "compiler", "build_type"
    user = "luxcorewheels"
    channel = "luxcorewheels"
    revision_mode = "scm_folder"

    def build(self):
        url = f"https://github.com/RenderKit/oidn/releases/download/v{self.version}/oidn-{self.version}.x64.windows.zip"
        get(self, url)

    def package(self):
        for subfolder in ("bin", "include", "lib"):
            shutil.copytree(
                os.path.join(
                    self.build_folder, f"oidn-{self.version}.x64.windows", subfolder
                ),
                os.path.join(self.package_folder, subfolder),
            )

    def package_info(self):
        self.cpp_info.libs = ["OpenImageDenoise", "OpenImageDenoise_core"]

    def package_id(self):
        # We clear everything in order to have a constant package_id and use the cache
        self.info.clear()
