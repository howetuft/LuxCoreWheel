import os
import shutil
from conan.tools.files import get, copy, rename
from conan import ConanFile


class Embree3Conan(ConanFile):
    name = "embree4"
    version = "4.3.1"  # This is the 1st version with precompiled bins for Macos ARM...
    settings = "os", "arch", "compiler", "build_type"
    user = "luxcorewheels"
    channel = "luxcorewheels"

    def layout(self):
        build_type = self.settings.get_safe("build_type", default="Release")
        # Define project folder structure
        # We directly download binaries, so it's a very simplified layout
        # (no build)...

        self.folders.source = "."
        self.folders.build = os.path.join("build", build_type)
        self.folders.generators = os.path.join(self.folders.build, "generators")

        ## cpp.source and cpp.build information is specifically designed
        # for editable packages:
        # this information is relative to the source folder
        self.cpp.source.libs = [ "embree4", "embree4.4" ]
        self.cpp.source.includedirs = ["include"]
        self.cpp.source.libdirs = ["lib"]
        self.cpp.source.bindirs = ["bin"]

    def source(self):
        url = f"https://github.com/RenderKit/embree/releases/download/v{self.version}/embree-{self.version}.arm64.macosx.zip"
        get(self, url)
        rename(self, "include/embree4", "include/embree3")
