# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

import os
import pathlib
import argparse
import tempfile
import shutil
import re
import binascii

from wheel.wheelfile import WheelFile
from wheel.cli.unpack import unpack
from wheel.cli.pack import pack
import zipfile

def create_link(wheel, target, linkname):
    zip_info = zipfile.ZipInfo(linkname)
    zip_info.create_system = 3
    zip_info.external_attr |= 0xA0000000
    wheel.writestr(zip_info, target)

def demangle_libname(libname):
    pattern = r"(?P<base>[A-Za-z_]*)-(?P<tag>.*)\.so\.(?P<version>[0-9]*\.[0-9]*\.[0-9]*)"
    # TODO
    # pattern = (
        # r"(?P<base>[A-Za-z_]*)"
        # r"-(?P<tag>?.*)\.so\."
        # r"(?P<version>[0-9]*\.[0-9]*\.[0-9]*)"
    # )
    match = re.fullmatch(pattern, libname)
    base = match["base"]
    tag = match["tag"]
    ver = match["version"]
    return base, tag, ver

def libpath(root_path, startswith):
    "Get a full library path for a library name starting with 'startswith'"
    # Library path
    libfolder = root_path / "pyluxcore.libs/"

    libs = (
        l
        for l in libfolder.iterdir()
        if l.name.startswith(startswith)
    )
    path = next(libs)
    path = str(path)
    path = pathlib.Path(path)
    return path


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("wheelpath", type=pathlib.Path)
    args = parser.parse_args()

    wheel_path = args.wheelpath
    wheel_folder = wheel_path.parents[0]

    print(f"Recomposing {wheel_path}")

    with tempfile.TemporaryDirectory(delete=False) as tmpdir:  # Working space
        # Unpack wheel
        unpack(path=args.wheelpath, dest=tmpdir)

        # Compute unpacked wheel path
        with WheelFile(args.wheelpath) as wf:
            namever = wf.parsed_filename.group("namever")
            unpacked_wheel_path = pathlib.Path(tmpdir) / namever


        # Find device_cpu lib tag
        device_cpu_path = libpath(unpacked_wheel_path, "libOpenImageDenoise_device_cpu")
        _, tag, _ = demangle_libname(device_cpu_path.name)
        print(f"Device cpu library tag: {tag}")
        replacement = f"-{tag}.so".encode()

        # Update core
        core_path = libpath(unpacked_wheel_path, "libOpenImageDenoise_core")
        replaced = b"-reserved.so"
        assert len(replacement) == len(replaced)
        print(f"Updating {core_path}")

        content = core_path.read_bytes()
        content = content.replace(replaced, replacement)
        core_path.write_bytes(content)


        # Repack wheel
        pack(
            directory=unpacked_wheel_path,
            dest_dir=wheel_folder,
            build_number=None
        )

    # with WheelFile(args.wheelpath, mode="a") as wf:
        # # Update core with device_cpu tag
        # libs = [
            # l.name
            # for l in zipfile.Path(wf, at="pyluxcore.libs/").iterdir()
            # if l.name.startswith("libOpenImageDenoise_device_")
        # ]
        # for lib in libs:
            # create_link(
                # wf,
                # os.path.join(lib),
                # os.path.join("pyluxcore.libs", unmangle_libname(lib)),
            # )

    # TODO
    # with tempfile.TemporaryDirectory() as tmpdir:  # Working space
        # # Unpack wheel
        # unpack(path=args.wheelpath, dest=tmpdir)
        # with WheelFile(args.wheelpath) as wf:
            # namever = wf.parsed_filename.group("namever")
            # unpacked_wheel_path = Path(tmpdir) / namever

        # # Create links to libraries for oidnDenoise
        # print("Create lib links for oidnDenoise")
        # lib_path = unpacked_wheel_path / "pyluxcore.libs"
        # libs = [
            # l.name
            # for l in os.scandir(lib_path)
            # if l.name.startswith("libOpenImageDenoise_device_")
        # ]
        # oidn_path = unpacked_wheel_path / "pyluxcore"
        # for lib in libs:
            # # Unmangle lib
            # pattern = (
                # r"libOpenImageDenoise_device_"
                # r"(?P<device>[a-z]*)"
                # r"(?:-.*)"
                # r"\.so\."
                # r"(?P<version>[0-9]*\.[0-9]*\.[0-9]*)"
            # )
            # match = re.fullmatch(pattern, lib)
            # dev = match["device"]
            # ver = match["version"]
            # unmangled_lib = f"libOpenImageDenoise_device_{dev}.so.{ver}"

            # # Create symlink in libs location
            # target_path = os.path.relpath(lib_path / lib, start=lib_path)
            # dest_path = lib_path / unmangled_lib
            # print(f"{dest_path} -> {target_path}")
            # os.symlink(target_path, dest_path)

        # # Repack wheel
        # pack(
            # directory=unpacked_wheel_path,
            # dest_dir=wheel_folder,
            # build_number=None
        # )


if __name__ == "__main__":
    main()
