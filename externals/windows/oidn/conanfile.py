import os
import shutil
from conan.tools.files import get, copy
from conan import ConanFile
from conan.tools.cmake import cmake_layout


class OidnConan(ConanFile):
    name = "oidn"
    version = "2.3.0"
    settings = "os", "arch", "compiler", "build_type"
    user = "luxcorewheels"
    channel = "luxcorewheels"
    revision_mode = "hash"

    def layout(self):
        ## define project folder structure

        self.folders.source = "."
        base = f"oidn-{self.version}.x64.windows"
        self.folders.build = os.path.join("build", str(self.settings.build_type))
        self.folders.generators = os.path.join(self.folders.build, "generators")

        ## cpp.source and cpp.build information is specifically designed
        # for editable packages:
        # this information is relative to the source folder
        self.cpp.source.libs = ["OpenImageDenoise", "OpenImageDenoise_core"]
        self.cpp.source.includedirs = [os.path.join(base, "include")]
        self.cpp.source.libdirs = [os.path.join(base, "lib")]
        self.cpp.source.bindirs = [os.path.join(base, "bin")]

        # ## cpp.package information is for consumers to find the package contents
        # # in the Conan cache
        # self.cpp.package.libs = ["OpenImageDenoise", "OpenImageDenoise_core"]
        # self.cpp.package.includedirs = ["include"] # includedirs is already set to 'include' by
                                                   # # default, but declared for completion
        # self.cpp.package.libdirs = ["lib"]         # libdirs is already set to 'lib' by
                                                   # # default, but declared for completion

        # ## cpp.package information is for consumers to find the package contents in the Conan cache

        # self.cpp.package.libs = ["oidn"]
        # self.cpp.package.includedirs = ["include"] # includedirs is already set to 'include' by
                                                   # # default, but declared for completion
        # self.cpp.package.libdirs = ["lib"]         # libdirs is already set to 'lib' by
                                                   # # default, but declared for completion

        # ## cpp.source and cpp.build information is specifically designed for editable packages:

        # # this information is relative to the source folder that is '.'
        # self.cpp.source.includedirs = ["include"] # maps to ./include

        # # this information is relative to the build folder that is './build/<build_type>', so it will
        # self.cpp.build.libdirs = ["."]  # map to ./build/<build_type> for libdirs

    def source(self):
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

