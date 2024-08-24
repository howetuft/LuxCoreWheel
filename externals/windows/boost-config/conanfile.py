# # TODO Licence
import windows.boost_template

Boost_Python_Recipe = BoostModule("config", "1.78.0")

# from conan import ConanFile
# from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
# from conan.tools.files import get


# class boost_moduleRecipe(ConanFile):
    # _module = "config"
    # version = "1.78.0"
    # requires = ["boost/1.78.0", "boost-config/1.78.0"]

    # name = f"boost-{_module}"
    # package_type = "library"

    # # Optional metadata
    # license = "<Put the package license here>"
    # author = "<Put your name here> <And your email here>"
    # url = "<Package recipe repository url here, for issues about the package>"
    # description = "<Description of boost-module package here>"
    # topics = ("<Put some tag here>", "<here>", "<and here>")

    # # Binary configuration
    # settings = "os", "compiler", "build_type", "arch"
    # options = {"shared": [True, False], "fPIC": [True, False]}
    # default_options = {"shared": False, "fPIC": True}

    # # Sources are located in the same place as this recipe, copy them to the recipe
    # exports_sources = "CMakeLists.txt", "src/*", "include/*"


    # def source(self):
        # get(
            # self,
            # f"https://github.com/boostorg/{self._module}/archive/refs/tags/boost-{self.version}.zip",
            # strip_root=True
        # )

    # def config_options(self):
        # if self.settings.os == "Windows":
            # self.options.rm_safe("fPIC")

    # def configure(self):
        # if self.options.shared:
            # self.options.rm_safe("fPIC")

    # def layout(self):
        # cmake_layout(self)

    # def generate(self):
        # deps = CMakeDeps(self)
        # deps.generate()
        # tc = CMakeToolchain(self)
        # tc.generate()

    # def build(self):
        # cmake = CMake(self)
        # cmake.configure()
        # cmake.build()

    # def package(self):
        # cmake = CMake(self)
        # cmake.install()

    # def package_info(self):
        # self.cpp_info.libs = [f"boost-{self._module}"]

