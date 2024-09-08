# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "atomic",
    "assert",
    "config",
    "container_hash",
    "core",
    "detail",
    "io",
    "iterator",
    "smart_ptr",
    "system",
    "type_traits",
    "predef",
    "winapi",
]

class BoostFilesystem(ConanFile, metaclass=BoostMeta, module="filesystem", boost_deps=DEPS, libs=["boost_filesystem"]):
    pass
