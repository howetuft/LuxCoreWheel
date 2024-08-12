import os
import shutil
from conan.tools.files import get, copy
from conan import ConanFile


class OidnConan(ConanFile):
    name = "oidn"
    version = "2.3.0"
    settings = "os", "arch"

    def build(self):
        url = f"https://github.com/RenderKit/oidn/releases/download/v{version}/oidn-{version}.x64.windows.zip"
        get(self, url)

    def package(self):
        shutil.copytree(
            self.build_folder,
            self.package_folder
        )

    def package_info(self):
        self.cpp_info.libs = ["oidn"]
