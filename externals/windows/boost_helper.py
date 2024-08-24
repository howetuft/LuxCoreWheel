# TODO License

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import get


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


class BoostTemplate(type):
    """Metaclass to create the ConanFile class."""
    # Sources are located in the same place as this recipe, copy them to the recipe


    def __new__(cls, module, boost_version, boost_deps=[]):
        module = str(module)
        boost_version = str(boost_version)
        boost_deps = list(boost_deps)
        print(f"Boost - Generating recipe for {module} {boost_version}")
        requires = [f"boost/{boost_version}"]
        for dep in boost_deps:
            requires.append(f"boost-{dep}/{boost_version}@LuxCoreWheel/LuxCoreWheel")

        attrs = dict(
            package_type="library",
            settings=("os", "compiler", "build_type", "arch"),
            options={"shared": [True, False], "fPIC": [True, False]},
            default_options={"shared": False, "fPIC": True},
            exports_sources=("CMakeLists.txt", "src/*", "include/*"),
            module=f"boost-{module}",
            name=f"boost-{module}",
            version=boost_version,
            requires=requires,
            source=source,
            config_options=config_options,
            configure=configure,
            layout=layout,
            generate=generate,
            build=build,
            package=package,
            package_info=package_info,
        )

        new_class = type("BoostTemplate", [ConanFile], attrs)
        return new_class
