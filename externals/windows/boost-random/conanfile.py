# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "array",
    "assert",
    "config",
    "core",
    "dynamic_bitset",
    "integer",
    "io",
    "predef",
    "range",
    "static_assert",
    "system",
    "throw_exception",
    "type_traits",
    "utility",
    "winapi",
]

class BoostRandom(ConanFile, metaclass=BoostMeta, module="random", boost_deps=DEPS, libs=["boost_random"]):
    pass
