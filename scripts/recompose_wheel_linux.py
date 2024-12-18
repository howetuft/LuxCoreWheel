# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

import os
from pathlib import Path
import argparse
import tempfile
import shutil
import re

from wheel.wheelfile import WheelFile
from wheel.cli.unpack import unpack
from wheel.cli.pack import pack


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("wheelpath", type=Path)
    args = parser.parse_args()

    wheel_path = args.wheelpath
    wheel_folder = wheel_path.parents[0]

    print(f"Recomposing {wheel_path}")

    with tempfile.TemporaryDirectory() as tmpdir:  # Working space
        # Unpack wheel
        unpack(path=args.wheelpath, dest=tmpdir)
        with WheelFile(args.wheelpath) as wf:
            namever = wf.parsed_filename.group("namever")
            unpacked_wheel_path = Path(tmpdir) / namever

        # Create links to libraries for oidnDenoise
        print("Create lib links for oidnDenoise")
        lib_path = unpacked_wheel_path / "pyluxcore.libs"
        libs = [
            l.name
            for l in os.scandir(lib_path)
            if l.name.startswith("libOpenImageDenoise_device_")
        ]
        oidn_path = unpacked_wheel_path / "pyluxcore"
        for lib in libs:
            # Unmangle lib
            pattern = (
                r"libOpenImageDenoise_device_"
                r"(?P<device>[a-z]*)"
                r"(?:-.*)"
                r"\.so\."
                r"(?P<version>[0-9]*\.[0-9]*\.[0-9]*)"
            )
            match = re.fullmatch(pattern, lib)
            dev = match["device"]
            ver = match["version"]
            unmangled_lib = f"libOpenImageDenoise_device_{dev}.so.{ver}"

            # Create symlink in libs location
            target_path = os.path.relpath(lib_path / lib, start=lib_path)
            dest_path = lib_path / unmangled_lib
            print(f"{dest_path} -> {target_path}")
            os.symlink(target_path, dest_path)

        # Repack wheel
        pack(
            directory=unpacked_wheel_path,
            dest_dir=wheel_folder,
            build_number=None
        )


if __name__ == "__main__":
    main()
