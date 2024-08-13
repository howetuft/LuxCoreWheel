from conans import ConanFile, CMake, tools
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def test(self):
        if not tools.cross_building(self.settings) or tools.os_info.is_windows:
            bin_path = os.path.join("bin", "test_package")
            if tools.os_info.is_windows:
                bin_path += ".exe"
            self.run(bin_path, run_environment=True)