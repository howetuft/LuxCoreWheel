# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

import traceback

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import get

BOOST_VERSION = "1.78.0"

def source(self):
    print(f"Source {self.module}")
    get(
        self,
        f"https://github.com/boostorg/{self.module}/archive/refs/tags/boost-{self.version}.zip",
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
    copy(self, "*.h", src=self.source_folder,
         dst=join(self.package_folder, "include"))
    copy(self, "*.lib", src=self.build_folder,
         dst=join(self.package_folder, "lib"), keep_path=False)
    copy(self, "*.a", src=self.build_folder,
         dst=join(self.package_folder, "lib"), keep_path=False)

def package_info(self):
    self.cpp_info.libs = [f"boost-{self.module}"]
    self.cpp_info.set_property("cmake_target_name", f"Boost::{self.module}")


class BoostMeta(type):
    """Metaclass to create the ConanFile class."""
    # Sources are located in the same place as this recipe, copy them to the recipe

    data_cache = dict()

    def __new__(cls, name, bases, attrs, **kwargs):
        # We cache kwargs as conan sometimes erases attributes...
        if name in BoostMeta.data_cache and kwargs:
            raise ValueError(f"'{name}' already in cache")
        if name in BoostMeta.data_cache:
            # Retrieve kwargs
            kwargs = BoostMeta.data_cache[name]
        else:
            BoostMeta.data_cache[name] = kwargs
        # print(f"'{name}' creation requested")
        # traceback.print_stack()

        # Attributes
        module = str(kwargs["module"])
        boost_version = BOOST_VERSION
        boost_deps = list(kwargs.get("boost_deps", []))
        requires = [f"boost/{boost_version}"]
        for dep in boost_deps:
            requires.append(f"boost-{dep}/{boost_version}")
        package_type = kwargs.get("package_type", "library")

        new_attrs = dict(
            package_type=package_type,
            settings=("os", "compiler", "build_type", "arch"),
            options={"shared": [True, False], "fPIC": [True, False]},
            default_options={"shared": False, "fPIC": True},
            exports_sources=("CMakeLists.txt", "src/*", "include/*"),
            module=module,
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
        attrs.update(new_attrs)

        # Instantiate
        # print(f"Boost - Generating recipe {name} for ('{module}', '{boost_version}')")
        new_class = super().__new__(cls, name, bases, attrs)
        return new_class
