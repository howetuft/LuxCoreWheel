# TODO License

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import get

class BoostTemplate(ConanFile):
    package_type = "library"

    # Optional metadata
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of boost-python package here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*", "include/*"

    requires = []

    def source(self):
        get(
            self,
            "https://github.com/boostorg/{self.module}/archive/refs/tags/boost-{self.version}.zip",
            strip_root=True
        )

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = [f"boost-{self.module}"]


def BoostModule(module, boost_version, boost_deps=[]):
    module = str(module)
    boost_version = str(boost_version)
    boost_deps = list(boost_deps)
    print(f"Boost - Generating recipe for {module} {boost_version}")
    new_instance = BoostTemplate()
    new_instance.module = f"boost-{module}"
    new_instance.name = f"boost-{module}"
    new_instance.version = boost_version
    requires = [f"boost/{boost_version}"]
    for dep in boost_deps:
        requires.append(f"boost-{dep}/{boost_version}@LuxCoreWheel/LuxCoreWheel")
    new_instance.requires = requires
    return new_instance


