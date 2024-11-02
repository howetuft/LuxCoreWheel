from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, export_conandata_patches, copy, get, rm, rmdir, replace_in_file
from conan.tools.microsoft import is_msvc, is_msvc_static_runtime
from conan.tools.scm import Version
from conan.errors import ConanInvalidConfiguration
import os
from pathlib import PurePosixPath

required_conan_version = ">=1.53.0"

BOOST_VERSION = os.environ["BOOST_VERSION"]
OIIO_VERSION = os.environ["OIIO_VERSION"]

class OpenImageIOConan(ConanFile):
    name = "openimageio"
    description = (
        "OpenImageIO is a library for reading and writing images, and a bunch "
        "of related classes, utilities, and applications. There is a "
        "particular emphasis on formats and functionality used in "
        "professional, large-scale animation and visual effects work for film."
    )
    topics = ("vfx", "image", "picture")
    license = "Apache-2.0", "BSD-3-Clause"
    homepage = "http://www.openimageio.org/"
    version = OIIO_VERSION  # Reminder, previous version: "2.2.13.1"
    user = "luxcorewheels"
    channel = "luxcorewheels"
    # revision_mode = "scm_folder"

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "with_libjpeg": ["libjpeg", "libjpeg-turbo"],
        "with_libpng": [True, False],
        "with_freetype": [True, False],
        "with_hdf5": [True, False],
        "with_opencolorio": [True, False],
        "with_opencv": [True, False],
        "with_tbb": [True, False],
        "with_dicom": [True, False],
        "with_ffmpeg": [True, False],
        "with_giflib": [True, False],
        "with_libheif": [True, False],
        "with_raw": [True, False],
        "with_openjpeg": [True, False],
        "with_openvdb": [True, False],
        "with_ptex": [True, False],
        "with_libwebp": [True, False],
    }
    default_options = {
        "shared": False,
        "with_libjpeg": "libjpeg",
        "with_libpng": True,
        "with_freetype": True,
        "with_hdf5": False,
        "with_opencolorio": True,
        "with_opencv": False,
        "with_tbb": False,
        "with_dicom": False,  # Heavy dependency, disabled by default
        "with_ffmpeg": False,
        "with_giflib": True,
        "with_libheif": True,
        "with_raw": False,  # libraw is available under CDDL-1.0 or LGPL-2.1, for this reason it is disabled by default
        "with_openjpeg": True,
        "with_openvdb": False,  # FIXME: broken on M1
        "with_ptex": True,
        "with_libwebp": True,
        "fmt/*:header_only": True,
        "openexr/*:shared": False
    }

    tool_requires = [
        "yasm/1.3.0",
    ]

    def export_sources(self):
        export_conandata_patches(self)

    def requirements(self):
        # Required libraries
        self.requires("zlib/[>=1.2.11 <2]")
        self.requires(f"boost/{BOOST_VERSION}")  # Modified
        self.requires("libtiff/4.6.0")
        self.requires("imath/3.1.9", transitive_headers=True)
        self.requires("openexr/3.2.3")
        if self.options.with_libjpeg == "libjpeg":
            self.requires("libjpeg/9e")
        elif self.options.with_libjpeg == "libjpeg-turbo":
            self.requires("libjpeg-turbo/3.0.2")
        self.requires("pugixml/1.14")
        self.requires("libsquish/1.15")
        self.requires("tsl-robin-map/1.2.1")
        if Version(self.version) >= "2.4.17.0":
            self.requires("fmt/10.2.1", transitive_headers=True)
        else:
            self.requires("fmt/9.1.0", transitive_headers=True)

        # Optional libraries
        if self.options.with_libpng:
            self.requires("libpng/1.6.42")
        if self.options.with_freetype:
            self.requires("freetype/2.13.2")
        if self.options.with_hdf5:
            self.requires("hdf5/1.14.3")
        if self.options.with_opencolorio:
            self.requires("opencolorio/2.3.1")
        if self.options.with_opencv:
            self.requires("opencv/4.8.1")
        if self.options.with_tbb:
            self.requires("onetbb/2021.10.0")
        if self.options.with_dicom:
            self.requires("dcmtk/3.6.7")
        if self.options.with_ffmpeg:
            self.requires("ffmpeg/6.1")
        # TODO: Field3D dependency
        if self.options.with_giflib:
            self.requires("giflib/5.2.1")
        if self.options.with_libheif:
            self.requires("libheif/1.16.2")
        if self.options.with_raw:
            self.requires("libraw/0.21.2")
        if self.options.with_openjpeg:
            self.requires("openjpeg/2.5.2")
        if self.options.with_openvdb:
            self.requires("openvdb/8.0.1")
        if self.options.with_ptex:
            self.requires("ptex/2.4.2")
        if self.options.with_libwebp:
            self.requires("libwebp/1.3.2")

    def validate(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, 11)
        if is_msvc(self) and is_msvc_static_runtime(self) and self.options.shared:
            raise ConanInvalidConfiguration(
                "Building shared library with static runtime is not supported!"
            )

    def layout(self):
        build_type = self.settings.get_safe("build_type", default="Release")
        cmake_layout(self)
        print("OIIO LAYOUT")

        # Set folders
        self.folders.source = "."
        self.folders.build = PurePosixPath("build", build_type)
        self.folders.generators = PurePosixPath("build", build_type, "generators")

        # Main
        self.cpp.package.libs = ["OpenImageIO", "OpenImageIO_Util"]
        self.cpp.package.includedirs = [PurePosixPath("src", "include")] # maps to ./include
        self.cpp.package.libdirs += [
            self.folders.build,
            PurePosixPath(self.folders.build, "lib"),
        ]

        # Describe what changes between package and editable
        #
        # cpp.source and cpp.build information is specifically designed for
        # editable packages:
        # this information is relative to the source folder that is '.'
        self.cpp.source.includedirs = [PurePosixPath("src", "include")]

        # this information is relative to the build folder that is
        # './build/<build_type>', so it will map to ./build/<build_type> for libdirs
        self.cpp.build.libdirs = ["lib"]
        self.cpp.build.includedirs = ["include"]

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        rm(self, "conanfile.txt", ".")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.absolute_paths = True

        # CMake options
        tc.cache_variables["BUILD_SHARED_LIBS"] = False
        tc.variables["CMAKE_DEBUG_POSTFIX"] = ""  # Needed for 2.3.x.x+ versions
        tc.cache_variables["OIIO_BUILD_TOOLS"] = False
        tc.cache_variables["OIIO_BUILD_TESTS"] = False
        tc.cache_variables["BUILD_DOCS"] = False
        tc.cache_variables["INSTALL_DOCS"] = False
        tc.cache_variables["INSTALL_FONTS"] = False
        tc.cache_variables["INSTALL_CMAKE_HELPER"] = False
        tc.cache_variables["EMBEDPLUGINS"] = True  # Modified (to cache variable)
        tc.cache_variables["USE_OPENEXR"] = True  # Added
        tc.cache_variables["USE_PYTHON"] = False
        tc.cache_variables["USE_EXTERNAL_PUGIXML"] = True
        tc.cache_variables["BUILD_MISSING_FMT"] = False
        tc.cache_variables["USE_Qt5"] = False
        tc.cache_variables["VERBOSE"] = True
        tc.cache_variables["USE_Libsquish"] = False
        # tc.cache_variables["CMAKE_CXX_STANDARD"] = str(self.settings.compiler.cppstd)  # TODO
        tc.cache_variables["LINKSTATIC"] = True


        # Conan is normally not used for testing, so fixing this option to not build the tests
        tc.cache_variables["BUILD_TESTING"] = False

        # OIIO CMake files are patched to check USE_* flags to require or not use dependencies
        tc.variables["USE_JPEGTURBO"] = (
            self.options.with_libjpeg == "libjpeg-turbo"
        )
        tc.variables[
            "USE_JPEG"
        ] = True  # Needed for jpeg.imageio plugin, libjpeg/libjpeg-turbo selection still works
        tc.variables["USE_HDF5"] = self.options.with_hdf5
        tc.variables["USE_OPENCOLORIO"] = self.options.with_opencolorio
        tc.variables["USE_OPENCV"] = self.options.with_opencv
        tc.variables["USE_TBB"] = self.options.with_tbb
        tc.variables["USE_DCMTK"] = self.options.with_dicom
        tc.variables["USE_FFMPEG"] = self.options.with_ffmpeg
        tc.variables["USE_FIELD3D"] = False
        tc.variables["USE_GIF"] = self.options.with_giflib
        tc.variables["USE_LIBHEIF"] = self.options.with_libheif
        tc.variables["USE_LIBRAW"] = self.options.with_raw
        tc.variables["USE_OPENVDB"] = self.options.with_openvdb
        tc.variables["USE_PTEX"] = self.options.with_ptex
        tc.variables["USE_R3DSDK"] = False
        tc.variables["USE_NUKE"] = False
        tc.variables["USE_OPENGL"] = False
        tc.variables["USE_LIBPNG"] = self.options.with_libpng
        tc.variables["USE_FREETYPE"] = self.options.with_freetype
        tc.variables["USE_LIBWEBP"] = self.options.with_libwebp
        tc.variables["USE_OPENJPEG"] = self.options.with_openjpeg

        tc.preprocessor_definitions["BOOST_NO_CXX98_FUNCTION_BASE"] = None  # No deprecated functions (C++17)
        tc.cache_variables["STOP_ON_WARNING"] = False
        tc.cache_variables["USE_STD_REGEX"] = True

        tc.generate()

        cd = CMakeDeps(self)
        if self.options.with_libwebp:
            cd.set_property("libwebp::webp", "cmake_target_name", "WebP::webp")
            cd.set_property("libwebp::webpdemux", "cmake_target_name", "WebP::webpdemux")
        if self.options.with_freetype:
            cd.set_property("freetype", "cmake_find_mode", "module")

        cd.generate()

        # Copy fmt files
        print("Copy fmt files")
        fmt = self.dependencies["fmt"]
        fmt_includes = fmt.cpp_info.includedirs
        destination = PurePosixPath(
            self.source_folder, "src", "include", "OpenImageIO", "detail", "fmt"
        )

        for origin in fmt_includes:
            copied = copy(
                self,
                pattern="*.h",
                src=origin,
                dst=destination,
                keep_path=False,
            )
            print(f"Copied '{copied}' from '{origin}' to '{destination}'...")



    def build(self):
        print("Building OIIO")
        apply_conandata_patches(self)
        replace_in_file(
            self,
            os.path.join(self.source_folder, "src", "cmake", "externalpackages.cmake"),
            "fmt::fmt",
            "fmt::fmt-header-only",
        )
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        print("Packaging OIIO")
        copy(self, "LICENSE*.md", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()
        copy(
            self,
            "*.h",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "include"),
        )
        copy(
            self,
            "*.hpp",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "include"),
        )
        copy(
            self,
            "*.lib",
            src=self.build_folder,
            dst=os.path.join(self.package_folder, "lib"),
            keep_path=False,
        )
        copy(
            self,
            "*.a",
            src=self.build_folder,
            dst=os.path.join(self.package_folder, "lib"),
            keep_path=False,
        )
        copy(
            self,
            "*.cmake",
            src=self.build_folder,
            dst=os.path.join(self.package_folder, "lib", "cmake"),
            keep_path=False,
        )

        rmdir(self, os.path.join(self.package_folder, "share"))
        if self.settings.os == "Windows":
            for vc_file in ("concrt", "msvcp", "vcruntime"):
                rm(self, f"{vc_file}*.dll", os.path.join(self.package_folder, "bin"))
        # rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        # rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_id(self):
        # We clear everything in order to have a constant package_id and use the cache
        self.info.clear()

    @staticmethod
    def _conan_comp(name):
        return f"openimageio_{name.lower()}"

    def _add_component(self, name):
        component = self.cpp_info.components[self._conan_comp(name)]
        component.set_property("cmake_target_name", f"OpenImageIO::{name}")
        component.set_property("cmake_file_name", name)
        return component

    # def package_info(self):
        # self.cpp_info.set_property("cmake_file_name", "OpenImageIO")
        # self.cpp_info.set_property("cmake_target_name", "openimageio::openimageio")
        # self.cpp_info.libs = ["OpenImageIO", "OpenImageIO_Util"]
        # self.cpp_info.libdirs = [os.path.join("build", "Release", "lib")]
        # if not self.options.shared:
            # self.cpp_info.defines.append("OIIO_STATIC_DEFINE")

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "OpenImageIO")
        self.cpp_info.set_property("pkg_config_name", "OpenImageIO")

        self.cpp_info.set_property("cmake_target_name", "openimageio::openimageio")

        self.cpp_info.names["cmake_find_package"] = "OpenImageIO"
        self.cpp_info.names["cmake_find_package_multi"] = "OpenImageIO"

        self.cpp_info.libs = ["OpenImageIO", "OpenImageIO_Util"]
        self.cpp_info.libdirs = [os.path.join("build", "Release", "lib")]
