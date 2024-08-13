from conans import ConanFile, tools, CMake
import os

class OpenImageIOConan(ConanFile):

    name = "openimageio"
    version = "2.1.11.2"
    description = "OpenImageIO is a library for reading and writing images, and a bunch of related classes, utilities, and applications."
    topics = ["graphics", "images", "vfx"]
    url = "https://github.com/p-podsiadly/conan-openimageio"
    homepage = "https://github.com/OpenImageIO/oiio"
    license = "BSD-3-Clause"

    settings = "os", "compiler", "build_type", "arch"

    options = {
        "shared": [True, False],
        "with_webp": [True, False],
        "with_jpeg2000": [True, False],
        "with_freetype": [True, False],
        "with_opencolorio": [True, False],
        "with_tools": [True, False]
    }

    default_options = {
        "shared": False,
        "with_webp": True,
        "with_jpeg2000": True,
        "with_freetype": True,
        "with_opencolorio": True,
        "with_tools": False
    }

    generators = "cmake", "cmake_find_package"

    requires = [
        "boost/1.72.0",
        "tsl-robin-map/0.6.2@tessil/stable",
        "openexr/2.4.0",
        "libtiff/4.0.9",
        "libpng/1.6.37",
        "libjpeg-turbo/2.0.4"
    ]

    _source_subfolder = "source_subfolder"

    exports = ["oiio-*.patch"]

    def requirements(self):

        if self.options.with_webp:
            self.requires("libwebp/1.0.3")

        if self.options.with_jpeg2000:
            self.requires("openjpeg/2.3.1")

        if self.options.with_freetype:
            self.requires("freetype/2.10.1")

        if self.options.with_opencolorio:
            self.requires("opencolorio/1.1.1@ppodsiadly/stable")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "oiio-Release-{}".format(self.version)
        os.rename(extracted_dir, self._source_subfolder)

        patch_file = self.conan_data["patches"][self.version]
        tools.patch(base_path=self._source_subfolder, patch_file=patch_file, strip=1)

    def _configure_cmake(self):
        cmake = CMake(self)

        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["USE_OPENGL"] = False
        cmake.definitions["USE_QT"] = False
        cmake.definitions["LINKSTATIC"] = False
        cmake.definitions["OIIO_BUILD_TOOLS"] = self.options.with_tools
        cmake.definitions["OIIO_BUILD_TESTS"] = False
        cmake.definitions["BUILD_DOCS"] = False
        cmake.definitions["INSTALL_FONTS"] = False
        cmake.definitions["USE_PYTHON"] = False

        cmake.definitions["USE_FREETYPE"] = self.options.with_freetype
        cmake.definitions["USE_HDF5"] = False
        cmake.definitions["USE_OPENCOLORIO"] = self.options.with_opencolorio
        cmake.definitions["USE_OPENCV"] = False
        cmake.definitions["USE_TBB"] = False
        cmake.definitions["USE_DCMTK"] = False
        cmake.definitions["USE_FFMPEG"] = False
        cmake.definitions["USE_GIF"] = False
        cmake.definitions["USE_LIBHEIF"] = False
        cmake.definitions["USE_LIBRAW"] = False
        cmake.definitions["USE_OPENJPEG"] = self.options.with_jpeg2000
        cmake.definitions["USE_PTEX"] = False
        cmake.definitions["USE_WEBP"] = self.options.with_webp
        cmake.definitions["USE_NUKE"] = False

        cmake.configure(source_folder=self._source_subfolder)
        
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

        self.copy("LICENSE.md", dst="licenses", src=self._source_subfolder)
        self.copy("LICENSE-THIRD-PARTY.md", dst="licenses", src=self._source_subfolder)

    def package_info(self):

        self.cpp_info.names["cmake_find_package"] = "OpenImageIO"
        self.cpp_info.names["cmake_find_package_multi"] = "OpenImageIO"

        self.cpp_info.libs = ["OpenImageIO", "OpenImageIO_Util"]
        
        if not self.options.shared:
            self.cpp_info.defines.append("OIIO_STATIC_DEFINE")

        if self.settings.os == "Linux":
            self.cpp_info.system_libs.append("dl")