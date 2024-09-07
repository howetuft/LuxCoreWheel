# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "assert",
    "config",
    "core",
    "intrusive",
    "move",
    "static_assert",
    "type_traits",
    "winapi",
]

class BoostContainer(ConanFile, metaclass=BoostMeta, module="container", boost_deps=DEPS, libs=["boost_container"]):
    pass
