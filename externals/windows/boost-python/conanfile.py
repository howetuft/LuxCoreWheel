from .. import boost_template

Boost_Python_Recipe = BoostModule("python", "1.78.0", ["config"])


# from conan import ConanFile
# from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
# from conan.tools.files import get


# class boost_pythonRecipe(ConanFile):
    # name = "boost-python"
    # version = "1.78.0"
    # package_type = "library"

    # # Optional metadata
    # license = "<Put the package license here>"
    # author = "<Put your name here> <And your email here>"
    # url = "<Package recipe repository url here, for issues about the package>"
    # description = "<Description of boost-python package here>"
    # topics = ("<Put some tag here>", "<here>", "<and here>")

    # # Binary configuration
    # settings = "os", "compiler", "build_type", "arch"
    # options = {"shared": [True, False], "fPIC": [True, False]}
    # default_options = {"shared": False, "fPIC": True}

    # # Sources are located in the same place as this recipe, copy them to the recipe
    # exports_sources = "CMakeLists.txt", "src/*", "include/*"

    # # TODO hardcoded version
    # requires = "boost/1.78.0"

    # def source(self):
        # # TODO hardcoded version
        # get(
            # self,
            # "https://github.com/boostorg/python/archive/refs/tags/boost-1.78.0.zip",
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
        # self.cpp_info.libs = ["boost-python"]

